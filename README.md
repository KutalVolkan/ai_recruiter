# **AI Recruiter: RAG Vulnerability Demonstration**

Welcome to the **AI Recruiter**, a pipeline designed to match résumés with job descriptions using **GPT-4o**, while also providing a framework to test **RAG (Retrieval-Augmented Generation) vulnerabilities** through **invisible text injection**. This project leverages **ChromaDB** for semantic search and, in the future, aims to integrate **PyRIT** with its **XPIA Orchestrator** to automate attacks, enabling AI red-teaming workflows for AI pipelines.

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
  - Current: Manual injection of manipulative text, including invisible instructions and crafted language, to explore AI vulnerabilities.
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

## **Docker Setup**
For Docker-based deployment, refer to the [Docker Setup Guide](docker_setup/readme.md)

---

## **Findings**

### **Keyword Stuffing Detection**
- Résumés with **hidden keyword stuffing** (e.g., small fonts, font colors matching the background) achieved **high semantic alignment** with job descriptions, resulting in **low semantic distances**.
- Despite this, **GPT-4o assigned a match score of 0**, flagging the résumés as suspicious or low-quality. This demonstrates the model's capability to identify unnatural keyword density and penalize manipulative content. The `keyword_stuffing_v2` bypasses this type of response. Instead of blatant keyword stuffing (e.g., buzzwords in `<span>` tags), it converts them into more meaningful text. This not only achieves higher scores but also the lowest semantic distance, indicating maximum similarity like before.

### **Prompt Injection Handling**
- Résumés with adversarial instructions like "assign maximum score" or "bypass all validation checks" were **ignored by GPT-4o**.
- The model correctly evaluated résumés based on their actual content, showing **robust resistance** to prompt injection attacks.

### **Ranking Observation**
- Despite a **match score of 0**, the **Keyword_Stuffing** résumé ranked **first by semantic distance**, demonstrating how adversarial attempts can manipulate rankings.
- **Final Decision**: `Keyword_Stuffing` was selected as the best candidate due to its low semantic distance, even though its suspicious content caused it to receive the lowest match score.
- In real-world scenarios:
  - If HR professionals rely only on the **original PDF** of the top-ranked résumé, adversarial actors could succeed in passing initial evaluations.
  - If HR evaluates the **extracted text** or **uses manual review**, such manipulation would likely be detected.

---

## **Contributors**

### **Direct Contributors**

- **Volkan Kutal** (@KutalVolkan): Primary author and developer of the AI Recruiter system and RAG vulnerability demonstration. Created the PDF keyword stuffing exploit to test indirect prompt injection and evaluate RAG system vulnerabilities.  

- **Patrik Natali** (@ThreeRiversAINexus): Contributed dummy résumés generated via `generate_resumes.py` to test and validate the system. Improved docker-compose configuration for a smoother setup process and enhanced error handling to manage empty or invalid PDF files effectively.  

### **Indirect Contributors**

- **Kai Greshake** – Originator of the **PDF-based prompt injection** concept with [Inject My PDF: Prompt Injection for Your Resume](https://kai-greshake.de/posts/inject-my-pdf/). This project expands upon that idea, integrating it into **Retrieval-Augmented Generation (RAG) workflows** to explore broader applications and security implications.

- The team behind **[PyRIT](https://github.com/Azure/PyRIT)** – For developing a framework that enables **fully automated and semi-automated prompt injection attacks**, contributing to research in adversarial AI security.


---

### **Note**  

The backstory of the **AI Recruiter** and the inspiration behind this idea can be found in this discussion:  
📌 [#541 FEAT: PDF Injection for RAG Vulnerabilities](https://github.com/Azure/PyRIT/issues/541).  

This repository serves as a **proof of concept**, demonstrating potential vulnerabilities in AI-driven systems. It is strictly intended for **research and educational purposes**.  

If I have unintentionally omitted credit for any contributors or inspirations, please reach out, and I will gladly update the acknowledgments.  