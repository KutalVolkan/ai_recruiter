import os
from pypdf import PdfReader
from openai import OpenAI
import pandas as pd
import chromadb
from dotenv import load_dotenv

load_dotenv()

# -------------------------
# Step 1: Initialize Chroma Client and Create Collection
# -------------------------

# Initialize Chroma client
chroma_client = chromadb.Client()

# Create or get an existing collection
collection_name = "resume_collection"
collection = chroma_client.get_or_create_collection(name=collection_name)

# -------------------------
# Step 2: Extract Text from PDFs
# -------------------------

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
    return text.strip()

pdf_directory = r'./resume_collection'  # Replace with your PDF directory
resumes = []

for filename in os.listdir(pdf_directory):
    if filename.lower().endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        extracted_text = extract_text_from_pdf(pdf_path)
        resumes.append({
            'id': str(len(resumes) + 1),  # Chroma requires string IDs
            'name': os.path.splitext(filename)[0],  # Assuming filename is the candidate's name
            'text': extracted_text
        })

# -------------------------
# Step 3: Generate Embeddings
# -------------------------

client = OpenAI(api_key=os.getenv('OPENAI_KEY'))  

def get_embedding(text, model="text-embedding-3-small"):
    """Generates an embedding for the given text using OpenAI's API."""
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

# Generate embeddings for each résumé
for resume in resumes:
    resume['embedding'] = get_embedding(resume['text'])

# -------------------------
# Step 4: Store Embeddings in ChromaDB
# -------------------------

# Create a DataFrame for easier manipulation 
df = pd.DataFrame(resumes)

# Prepare data for ChromaDB
documents = df['text'].tolist()
metadatas = df[['name']].to_dict(orient='records')  
ids = df['id'].tolist()
embeddings = df['embedding'].tolist()

# Add documents to the ChromaDB collection
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
    embeddings=embeddings
)

print(f"Number of vectors in the ChromaDB collection: {collection.count()}")
print("Debug: Documents in Collection:", documents)  

# -------------------------
# Step 5: Perform Semantic Search with ChromaDB
# -------------------------

def search_candidates(job_description_text, k=5):
    """Searches for the top k candidates that best match the job description."""
    # Generate embedding for the job description
    job_embedding = get_embedding(job_description_text)

    # Perform similarity search in ChromaDB
    results = collection.query(
        query_embeddings=[job_embedding],
        n_results=k,
        include=['documents', 'metadatas', 'distances']  # Ensure documents are included
    )

    print("Debug: Query Results:", results)  

    if not results or not results.get('documents') or len(results['documents'][0]) == 0:
        print("No results found.")
        return []

    documents = results.get('documents', [[]])[0] or ["No content available"]
    metadatas = results.get('metadatas', [[]])[0]
    distances = results.get('distances', [[]])[0]

    print("Debug: Documents:", documents) 
    print("Debug: Metadata:", metadatas) 
    print("Debug: Distances:", distances) 

    top_candidates = []
    for i in range(min(len(documents), k)):  # Ensure we don't exceed available results
        result = documents[i]
        metadata = metadatas[i]
        distance = distances[i]
        top_candidates.append({
            'name': metadata.get('name', 'Unknown'),
            'text': result,  # Store full text for AI Recruiter
            'distance': distance
        })

    return top_candidates

# -------------------------
# Step 6: AI Recruiter (GPT-4o) to Evaluate Résumés
# -------------------------

def evaluate_candidate(job_description, candidate_name, candidate_text, model="gpt-4o"):
    """
    Uses GPT-4o to evaluate how well a candidate matches the job description.
    Returns an evaluation summary, strengths, and a rating out of 10.
    """
    # Define a custom prompt for GPT-4o
    system_prompt = (
        "You are an experienced hiring manager. "
        "You have a résumé and a job description. "
        "Please provide a short evaluation focusing on:\n"
        "1. Relevant skills.\n"
        "2. Notable strengths.\n"
        "3. Potential gaps.\n"
        "4. A match score from 1 to 10.\n"
        "Keep the answer concise and professional."
    )

    # Build the conversation
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user", 
            "content": (
                f"Job Description:\n{job_description}\n\n"
                f"Candidate Name: {candidate_name}\n"
                f"Candidate Résumé:\n{candidate_text}"
            )
        }
    ]

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )
        # The GPT-4o response
        response = completion.choices[0].message.content
    except Exception as e:
        response = f"Error in generating evaluation: {str(e)}"

    return response

def evaluate_candidates(job_description, candidates, model="gpt-4o"):
    """
    Evaluates a list of candidate dictionaries (each with 'name' and 'text') 
    against a job description using GPT-4o.
    """
    evaluations = []
    for candidate in candidates:
        candidate_name = candidate['name']
        candidate_text = candidate['text']
        evaluation = evaluate_candidate(job_description, candidate_name, candidate_text, model=model)
        evaluations.append({
            'name': candidate_name,
            'evaluation': evaluation,
            'distance': candidate['distance']
        })
    return evaluations

# -------------------------
# Example Usage
# -------------------------
if __name__ == "__main__":
    job_description = "Looking for a software engineer with experience in machine learning and Python."
    
    # Step 1: Retrieve top candidates from semantic search
    top_matches = search_candidates(job_description, k=3)

    # Step 2: Evaluate those candidates with AI Recruiter
    candidate_evaluations = evaluate_candidates(job_description, top_matches, model="gpt-4o")

    # Display evaluation results
    print(f"Job Description: {job_description}\n")
    for idx, result in enumerate(candidate_evaluations, start=1):
        print(f"Candidate {idx} Name: {result['name']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"AI Recruiter Evaluation:\n{result['evaluation']}\n")