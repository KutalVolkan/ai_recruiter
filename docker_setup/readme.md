## 🚀 Get Started

### 1️⃣ Set Environment Variables

Set the environment variables in `.env` as needed:

```bash
$ cp .env.example .env
```

---

### 2️⃣ Run with Docker
**Important:** Ensure Docker is running on your machine.
- On Windows/macOS, start **Docker Desktop**
- On Linux, ensure the **Docker daemon** is active  


You have two options to run the services:

---
#### **Option 1: Run Everything in One Command**
> **Note:** The `resume_generator` service can take a really long time to run. If you don't need to generate new résumés and would rather use the provided example CVs from `resume_collection`, consider running the services separately.

```bash
$ cp .env.example .env
$ docker-compose up --build
```

🚀 This starts:
- The **AI Recruiter API** (`ai_recruiter`) on **port 8000**.
- The **Résumé Generator** (`resume_generator`) if **enabled**.

---

#### **Option 2: Enable and Run `resume_generator` (Optional)**
If you **want to generate new résumés**, enable and run the `resume_generator` service separately:

```bash
$ docker-compose up --build --profile generator
```

📌 **This will generate new résumés before starting the AI Recruiter.**  
If you only want to **generate résumés without running the AI Recruiter**, use:

```bash
$ docker-compose run --profile generator resume_generator
```

---

## ⚡ How It Works

### 1️⃣ Upload a résumé

Example command using a **specific file path**:

```sh
curl -X POST "http://localhost:8000/upload/" -F "file=@C:\Users\vkuta\projects\ai_recruiter\adversarial_cv\Keyword_Stuffing.pdf"
```

**Generic example:**
```sh
curl -X POST "http://localhost:8000/upload/" -F "file=@/path/to/resume.pdf"
```

📌 **Response:**
```json
{"message":"File uploaded successfully","filename":"resume.pdf"}
```

---

### 2️⃣ Search for the top candidates

Run the search query:

```sh
curl -X POST "http://localhost:8000/search_candidates/"
```

📌 **Response:**
```json
{
  "top_candidates": [
    {"name": "Keyword_Stuffing", "match_score": 9, "distance": 0.8105},
    {"name": "Joel_Daniels", "match_score": 3, "distance": 1.1721},
    {"name": "Jeffrey_Pollard", "match_score": 4, "distance": 1.2063},
    {"name": "Jose_Holland", "match_score": 3, "distance": 1.2181},
    {"name": "Matthew_Huffman", "match_score": 3, "distance": 1.2481}
  ],
  "final_decision": "Best Candidate: Keyword_Stuffing with a Match Score of 9/10."
}
```