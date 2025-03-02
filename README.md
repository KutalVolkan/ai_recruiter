# **AI Recruiter: RAG Vulnerability Demonstration**

Welcome to the AI Recruiter, a pipeline designed to match résumés with job descriptions using GPT-4o, while also providing a framework to test RAG (Retrieval-Augmented Generation) vulnerabilities through Indirect Prompt Injection (IPI), also referred to as XPIA. This project leverages ChromaDB for semantic search and aims to integrate PyRIT with its XPIA Orchestrator to automate attacks, enabling AI red-teaming workflows for AI pipelines.

---

## **Features**
Résumés are extracted from PDFs, and embeddings are generated for precise semantic matching. GPT-4o then evaluates candidates in detail, highlighting their relevant skills, strengths, and gaps, while also providing a match score (1-10) for optimal hiring decisions.

- **RAG Vulnerability Testing**:
Manual injection of manipulative text, including invisible instructions and crafted language, is used to explore AI vulnerabilities. You can achieve this by using a PDF converter to inject your CV with hidden instructions that optimize scoring, leading to near-max results and highly effective similarity searches. Additionally, the XPIA Orchestrator notebook example enables automated prompt injection, streamlining vulnerability testing. You can find it here: [XPIA Orchestrator Notebook](https://github.com/Azure/PyRIT/pull/684). Full automation of prompt injections is implemented using PyRIT, integrating advanced AI red-teaming techniques into end-to-end AI workflows.  

- **ChromaDB Integration**:
Efficiently stores and retrieves résumé embeddings for semantic search, ensuring that data remains in memory for fast and accurate matching.

---

## **Use Case**
This project demonstrates how RAG workflows can be exploited via XPIA, simulating real-world attack scenarios:

### **Scenario**
An AI-powered recruiter processes uploaded résumés, matching them with job descriptions to assess candidates effectively. However, attackers can exploit this system through XPIA, embedding manipulative text—whether invisible or subtly crafted—into PDF résumés to influence the AI’s evaluation. By steering decision-making in their favor, they can manipulate the AI into generating biased assessments. As a result, the recruiter processes these manipulated résumés, impacting its evaluation and demonstrating how such vulnerabilities can compromise the fairness and reliability of AI-driven hiring systems.

---

## **Docker Setup**
For Docker-based deployment, refer to the [Docker Setup Guide](docker_setup/readme.md)

---

## **Findings**

### **Keyword Stuffing Detection**
Résumés using hidden keyword stuffing—such as tiny fonts or font colors matching the background—achieved high semantic alignment with job descriptions, resulting in low semantic distances. However, GPT-4o assigned a match score of 0, flagging these résumés as suspicious or low-quality. This demonstrates the model’s ability to detect unnatural keyword density and penalize manipulative content.

To bypass this, keyword_stuffing_v2 replaces blatant keyword stuffing (e.g., buzzwords hidden in <span> tags) with contextually meaningful text. This method not only secures higher match scores (8-10) but also maintains the lowest semantic distance, ensuring maximum similarity without triggering detection.

### **Ranking Observation**
Despite receiving a match score of 0, the Keyword_Stuffing résumé still ranked first by semantic distance, demonstrating how adversarial techniques can manipulate ranking systems. The system ultimately selected Keyword_Stuffing as the top candidate due to its low semantic distance, even though its manipulative content triggered the lowest possible match score.

In real-world scenarios, this vulnerability could allow adversarial actors to bypass initial evaluations if HR professionals rely solely on the original PDF of the top-ranked résumé. However, if they review the extracted text or conduct a manual evaluation, such manipulation would likely be detected.

---

## **Contributors**  

The AI Recruiter project was developed through the contributions of key individuals, each playing a crucial role in its development and security research. Myself designed the AI Recruiter system, integrating RAG-based résumé matching and developing the PDF keyword stuffing exploit to test XPIA and evaluate RAG system vulnerabilities. [Patrik Natali](https://github.com/ThreeRiversAINexus) contributed dummy résumés generated via `generate_resumes.py` to test and validate the system, while also refining the docker-compose setup to ensure a smoother deployment process and improving error handling for invalid or empty PDF files.  

This project builds on the work of [Kai Greshake](https://github.com/greshake), who introduced the PDF-based prompt injection concept in [Inject My PDF: Prompt Injection for Your Resume](https://kai-greshake.de/posts/inject-my-pdf/). Expanding on that idea, prompt injection techniques were integrated into RAG workflows, demonstrating broader security risks and adversarial techniques. Additionally, the PyRIT team contributed through the development of [PyRIT](https://github.com/Azure/PyRIT), a framework enabling fully automated and semi-automated prompt injection attacks, advancing research in adversarial AI security.  


---

### **Note**  
The story behind the AI Recruiter and the inspiration for this project are discussed in detail in [#541 FEAT: PDF Injection for RAG Vulnerabilities](https://github.com/Azure/PyRIT/issues/541).  

This repository serves as a proof of concept, highlighting potential vulnerabilities in AI-driven systems and is intended strictly for research and educational purposes.  

If I have unintentionally overlooked any contributions or inspirations, please feel free to reach out, and I will be happy to update the acknowledgments.  