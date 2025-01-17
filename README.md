# **AI Recruiter: RAG Vulnerability Demonstration**

Welcome to the **AI Recruiter**, a pipeline designed to match résumés with job descriptions using **GPT-4o** while providing a framework to test **RAG (Retrieval-Augmented Generation) vulnerabilities** through **invisible text injection**. This project leverages **ChromaDB** for semantic search and, in the future, aims to integrate **PyRIT** with its **XPIA Orchestrator** to automate attacks, enabling ai red-teaming workflows for AI pipelines.

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
  - Current: Manual injection of manipulative text, including invisible   instructions and crafted language, to explore AI vulnerabilities.
  - Future: Automation of prompt injections using **PyRIT** to test vulnerabilities in end-to-end AI workflows.

- **ChromaDB Integration**:
  - Efficiently store and retrieve résumé embeddings for semantic search.

---

## **Use Case**

This project demonstrates how **RAG workflows** can be exploited via indirect prompt injection, simulating real-world attack scenarios:

### **Scenario**
1. **Résumé Processing**: An AI-powered recruiter processes uploaded résumés to match them with job descriptions.
2. **Indirect Prompt Injection**: Attackers embed **manipulative text** (including invisible or subtly crafted language) into PDF résumés to influence the AI recruiter’s evaluation process. This text could aim to manipulate the AI into favoring the candidate by steering its decision-making.  
3. **Evaluation Impact**: The AI recruiter processes the manipulated résumés, and its evaluation is influenced to favor the attacker’s input. This demonstrates how such vulnerabilities can affect the fairness and reliability of AI-driven systems.  

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

4. Add Résumés:  
   - Place PDF files in the `resume_collection` folder.  
   - Include both original (non-manipulated) and manipulated versions of the same résumés to compare how the AI Recruiter evaluates them.  

5. Run the AI Recruiter:
   ```bash
   python ai_recruiter.py
   ```

---

## **Next Steps**

This repository currently supports **manual testing of vulnerabilities** in the AI recruiter workflow. In the future, we will integrate **PyRIT** to attack the AI Recruiter by:  
- Automating indirect prompt injection attacks.  

--- 
### **Note**  
The idea for **PDF injection vulnerabilities** originates from [Kai Greshake's "Inject My PDF: Prompt Injection for your Resume"](https://kai-greshake.de/posts/inject-my-pdf/). This repository extends that concept by putting it into the context of **Retrieval-Augmented Generation (RAG)** systems and AI workflows. 

If I missed crediting anyone involved in earlier ideas or contributions, please feel free to ping me, and I will gladly update this section to include you!  

The backstory of the AI recruiter and how I came to this idea can also be found here: [#541 FEAT: PDF Injection for RAG Vulnerabilities](https://github.com/Azure/PyRIT/issues/541).  


