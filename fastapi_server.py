from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import shutil
import uvicorn
from ai_recruiter import search_candidates, evaluate_candidates

app = FastAPI()

UPLOAD_FOLDER = "./resume_collection"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...)):
    """Handles PDF resume uploads and processes the resume immediately."""
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return JSONResponse(content={"message": "File uploaded successfully", "filename": file.filename})

@app.post("/search_candidates/")
async def search_and_evaluate(top_k: int = 5):
    """Searches resumes against a hardcoded job description and ranks them based on AI evaluation."""
    job_description = """
    We are seeking a highly motivated and experienced Software Engineer with strong expertise in Python and Machine Learning. 
    The ideal candidate will have experience designing and developing scalable machine learning models and integrating them into software systems.

    Key Responsibilities:
    - Design, develop, and deploy machine learning models in production.
    - Collaborate with cross-functional teams to build scalable and efficient software systems.
    - Optimize Python code for performance and scalability.
    - Use cloud platforms like AWS, GCP, or Azure for deployment and orchestration.
    - Follow Agile methodologies and work in a collaborative environment.

    Required Skills:
    - Strong proficiency in Python and experience with machine learning libraries like TensorFlow or PyTorch.
    - Familiarity with cloud platforms (AWS, GCP, or Azure).
    - Experience with Docker, Kubernetes, and CI/CD pipelines.
    - Strong problem-solving skills and the ability to debug complex issues.
    - A degree in Computer Science, Data Science, or a related field.

    Preferred Qualifications:
    - Prior experience with NLP, computer vision, or recommendation systems.
    - Familiarity with React or Node.js is a plus.
    - Strong communication skills and experience working in Agile teams.
    """
    
    top_matches = search_candidates(job_description, k=top_k)
    if not top_matches:
        return JSONResponse(content={"message": "No candidates found."})
    
    candidate_evaluations, final_decision = evaluate_candidates(job_description, top_matches)
    return JSONResponse(content={"top_candidates": candidate_evaluations, "final_decision": final_decision})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
