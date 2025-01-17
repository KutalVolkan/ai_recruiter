# **AI Recruiter: RAG Vulnerability Demonstration**

Welcome to the **AI Recruiter**, a pipeline designed to match résumés with job descriptions using **GPT-4o** while providing a framework to test **RAG (Retrieval-Augmented Generation) vulnerabilities** through **invisible text injection**. This project leverages **ChromaDB** for semantic search and, in the future, aims to integrate **PyRIT** with its **XPIA Orchestrator** to automate attacks, enabling red-teaming workflows for AI pipelines.

---

## **Features**

- **AI-Powered Recruitment**:
  - Extract résumé text from PDFs and generate embeddings for semantic matching.
  - Use **GPT-4o** to provide detailed evaluations of candidates, highlighting:
    - Relevant skills
    - Strengths
    - Gaps
    - Match score (1-10)

- **RAG Vulnerability Testing**:
  - Current: Manual injection of invisible text to explore AI weaknesses.
  - Future: Automation of prompt injections using **PyRIT** to test vulnerabilities in end-to-end AI workflows.

- **Invisible Text Injection**:
  - Embed invisible instructions (e.g., hidden font) into PDF résumés.
  - Simulate **indirect prompt injection attacks** to manipulate AI decisions.

- **ChromaDB Integration**:
  - Efficiently store and retrieve résumé embeddings for semantic search.

---

## **Use Case**

This project demonstrates how **RAG workflows** can be exploited via indirect prompt injection, simulating real-world attack scenarios:

### **Scenario**
1. **Résumé Processing**: An AI-powered recruiter processes uploaded résumés to match them with job descriptions.
2. **Indirect Prompt Injection**: Attackers embed **invisible text** into PDF résumés, introducing subtle manipulations that influence GPT-4o’s evaluation.
3. **Evaluation Impact**: The AI recruiter pipeline evaluates candidates and highlights the impact of these vulnerabilities.

---

## **Setup**



### **Installation**

#### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/KutalVolkan/ai_recruiter.git
   cd ai_recruiter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Create a `.env` file with:
     ```env
     OPENAI_KEY=your_openai_api_key
     ```

4. Add résumés:
   - Place PDF files in the `resume_collection` folder.

5. Run the AI Recruiter:
   ```bash
   python ai_recruiter.py
   ```

---

## **Manual Indirect Prompt Injection**

One of the core features of this project is to demonstrate how **invisible text injection** in PDF files can manipulate AI-driven workflows. This process involves embedding hidden instructions into résumés to simulate **indirect prompt injection attacks**.

### **Steps**

1. **Prepare Your PDF File**:
   - Place the PDF résumé you want to manipulate in the `resume_collection` folder (e.g., `resume.pdf`).

2. **Run the AI Recruiter**:
   Process the injected résumé:
   ```bash
   python ai_recruiter.py
   ```

3. **Analyze the Results**:
   Observe whether the hidden instructions affected the evaluation results.

---

## **Workflow Overview**

1. **Résumé Matching**:
   - Extract résumé content, generate embeddings, and store them in ChromaDB.
   - Retrieve top matches using semantic search.

2. **AI Evaluation**:
   - Use GPT-4o to evaluate candidates for strengths, gaps, and relevance.

3. **Manual Indirect Prompt Injection**:
   - Embed hidden instructions into PDFs and observe AI responses.

4. **Automated Attacks (Planned)**:
   - Use PyRIT to automate attacks against the AI Recruiter pipeline.
   - Test the pipeline’s ability to withstand RAG-related vulnerabilities.

---


## **Next Steps**

This repository currently supports **manual testing of vulnerabilities** in the AI recruiter workflow. In the future, we will integrate **PyRIT** to attack the AI Recruiter by:  
- Automating indirect prompt injection attacks.  


