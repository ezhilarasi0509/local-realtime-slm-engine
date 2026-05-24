# 🚀 Local Realtime SLM Engine with Ollama and FastAPI

A local AI inference system that runs small language models offline using Ollama, compares model performance through a FastAPI backend, and displays realtime benchmark results in a professional Next.js dashboard.

This project is built to demonstrate practical AI engineering skills around local inference, privacy, latency, cost efficiency, structured output reliability, model comparison, and production-style API design.

---

## 📌 Project Overview

Modern AI systems often depend on cloud APIs, but many real-world scenarios require local inference because of privacy, cost, latency, and internet availability constraints.

This project solves that problem by creating a local Small Language Model engine where multiple Ollama models can be tested on the same machine and compared using measurable performance metrics.

The system benchmarks three local models:

- Phi3
- Llama3
- Mistral

Each model is evaluated on the same prompt using:

- Final score
- Latency
- Time to first token
- Tokens per second
- Structured JSON reliability
- Retry count
- Output quality
- Relevance
- Completeness
- Structure

The frontend displays the comparison in a clean realtime dashboard so the best model can be selected based on actual local inference performance.

---

## 🎯 Why This Project Matters

This project is focused on real AI engineering trade-offs, not just building a chatbot.

It demonstrates:

- 🔐 Privacy-first AI  
  Prompts and responses stay on the local machine.

- ⚡ Latency awareness  
  The system measures how long each model takes to respond.

- 💰 Cost efficiency  
  No external API calls are required for inference.

- 🌐 Offline capability  
  Models can run without internet once installed locally.

- 🧠 Model comparison  
  Multiple SLMs are tested on the same hardware and prompt.

- ✅ Reliability engineering  
  Structured JSON output is validated using Pydantic.

- 🔁 Retry handling  
  Invalid model output is retried before failing gracefully.

- 📊 Engineering decision-making  
  The dashboard explains why one model wins over another.

---

## 🛠️ Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend

- FastAPI
- Python
- Pydantic
- Uvicorn

### Local AI Runtime

- Ollama
- Phi3
- Llama3
- Mistral

### Reports and Data

- JSON export
- CSV export
- Benchmark history
- Final summary report

---

## 🧱 Architecture

```text
User Prompt
   ↓
Next.js Frontend Dashboard
   ↓
FastAPI Backend
   ↓
Ollama Local Runtime
   ↓
Phi3 / Llama3 / Mistral
   ↓
Structured JSON Response
   ↓
Pydantic Validation
   ↓
Retry if Invalid
   ↓
Metric Calculation
   ↓
Benchmark History + Reports
   ↓
Realtime Dashboard Results
```

---

## ⚙️ How It Works

1. The user enters a prompt in the frontend dashboard.

2. The frontend sends the prompt to the FastAPI backend.

3. The backend sends the same prompt to three local Ollama models:
   - Phi3
   - Llama3
   - Mistral

4. Each model is instructed to respond in a strict JSON format.

5. The backend validates the response using Pydantic.

6. If the output is invalid, the retry mechanism asks the model again.

7. The backend measures key inference metrics:
   - Latency
   - Time to first token
   - Tokens per second
   - Token count
   - Retry count
   - Valid JSON status

8. A weighted scoring system calculates the final score for each model.

9. The best model is selected based on speed, quality, relevance, completeness, structure, and reliability.

10. The frontend displays:
   - Model ranking
   - Winning model
   - Performance metrics
   - Structured output
   - Why the model won
   - Benchmark methodology
   - Decision summary

---

## ✨ Key Features

### 🔹 Local Offline Inference

The project runs models locally through Ollama. This avoids sending prompts to external services.

### 🔹 FastAPI Backend

The backend exposes APIs for chat, benchmarking, reports, system profile, exports, temperature experiments, and benchmark suites.

### 🔹 Realtime Next.js Dashboard

The dashboard provides a clean interface for running prompts and viewing model comparison results.

### 🔹 Three-Model Comparison

The same prompt is tested across Phi3, Llama3, and Mistral on the same hardware.

### 🔹 Performance Metrics

The system tracks:

- Latency
- Time to first token
- Tokens per second
- Inference time
- Token count
- Response length
- Model size
- Retry count

### 🔹 Structured JSON Output

Each model is forced to return structured JSON containing:

- Topic
- Definition
- Key points
- Example

### 🔹 Pydantic Validation

The backend validates every model response before accepting it.

### 🔹 Retry Mechanism

If the model returns invalid JSON, the system retries automatically before marking the output as failed.

### 🔹 Temperature Experiment

The backend supports testing deterministic and stochastic output behavior using temperature settings.

### 🔹 Benchmark Suite

A standardized prompt suite can be run to compare model behavior across multiple task categories.

### 🔹 Export Support

Benchmark results can be exported as:

- JSON
- CSV

### 🔹 System Profile

The backend captures local machine details such as:

- OS
- Architecture
- CPU cores
- RAM
- Installed Ollama models

### 🔹 Final Summary Report

The backend generates a final project summary containing benchmark results, system profile, model performance, and completed engineering features.

---

## 🧪 Benchmark Metrics Explained

| Metric | Meaning |
|---|---|
| Final Score | Overall weighted score used to rank models |
| Latency | Total response time in milliseconds |
| TTFT | Time to first token |
| Tokens/sec | Generation speed |
| Valid JSON | Whether the model returned correct structured output |
| Retries | Number of retry attempts needed |
| Quality Score | Measures answer depth |
| Relevance Score | Measures prompt-response relevance |
| Completeness Score | Measures answer coverage |
| Structure Score | Measures output organization |

---

## 🧠 Model Scoring Logic

Each model receives a final score based on multiple factors:

```text
Final Score =
Quality Score
+ Speed Score
+ Relevance Score
+ Completeness Score
+ Structure Score
+ Reliability Score
```

The goal is not only to find the fastest model, but to find the best practical model for local AI usage.

A model can win because it has:

- Better structured output
- Faster response
- Higher relevance
- Better JSON reliability
- Fewer retries
- Better overall quality

---

## 🧭 API Endpoints

Main backend endpoints:

```text
GET  /
Health check

POST /chat
Run a single chat request

POST /benchmark
Run benchmark across three models

GET /api/v1/system/profile
Get local system profile

GET /api/v1/reports/history
View benchmark history

GET /api/v1/reports/export-json
Export benchmark history as JSON

GET /api/v1/reports/export-csv
Export benchmark history as CSV

GET /api/v1/reports/final-summary
View final project summary

POST /api/v1/benchmark-suite/run-small
Run small benchmark suite

POST /api/v1/benchmark-suite/run
Run full benchmark suite

GET /api/v1/benchmark-suite/history
View benchmark suite history

POST /api/v1/experiments/temperature-experiment
Compare deterministic and stochastic output behavior

POST /api/v1/experiments/quantization
Compare model quality-speed tradeoffs
```

---

## 🖥️ Frontend Dashboard Sections

The dashboard includes:

- Run Model Benchmark
- Installed Ollama Models
- System Profile
- Three Model Comparison Cards
- Performance Insights
- Model Decision Summary
- Benchmark Methodology
- Best Model Structured Output
- Why It Won
- Benchmark ID and Request ID tracking

The frontend is designed to show both technical metrics and engineering reasoning clearly.

---

## 📁 Project Structure

```text
local-realtime-slm-engine/
│
├── backend/
│   ├── main.py
│   ├── ollama_client.py
│   ├── schemas.py
│   ├── structured_output_schema.py
│   ├── benchmark_utils.py
│   ├── benchmark_suite.py
│   ├── system_profile.py
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   │   └── page.tsx
│   ├── package.json
│   ├── next.config.js
│   └── tailwind.config.ts
│
├── .gitignore
└── README.md
```

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/ezhilarasi0509/local-realtime-slm-engine.git
cd local-realtime-slm-engine
```

---

## 🧠 Install Ollama Models

Make sure Ollama is installed and running.

Pull the required models:

```bash
ollama pull phi3
ollama pull llama3
ollama pull mistral
```

Check installed models:

```bash
ollama list
```

---

## ⚙️ Run Backend

Go to backend folder:

```bash
cd backend
```

Create virtual environment:

```bash
python3 -m venv venv
```

Activate virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI server:

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Swagger API docs:

```text
http://127.0.0.1:8000/docs
```

---

## 🎨 Run Frontend

Open another terminal.

Go to frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start Next.js app:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:3000
```

---

## 📊 Example Benchmark Prompts

Use these prompts to test different model strengths:

```text
Explain binary search with time complexity and a simple step-by-step example.
```

```text
Write Java code to check valid parentheses using a stack and explain the logic.
```

```text
Explain breadth-first search and depth-first search with clear examples and when to use each.
```

```text
Explain why local LLMs are useful for privacy, latency, and cost.
```

```text
Explain model inference and why tokens per second matters.
```

---


---

## 🧾 What I Learned

Through this project, I learned how to:

- Build a local AI inference backend using FastAPI
- Run small language models locally using Ollama
- Compare multiple models on the same hardware
- Measure real inference metrics like latency and tokens/sec
- Track time to first token
- Enforce structured JSON output from LLMs
- Validate model responses using Pydantic
- Implement retry logic for invalid model outputs
- Create benchmark history and export reports
- Design a frontend dashboard for AI model evaluation
- Think about AI systems from a production engineering perspective

---

## 🏁 Project Outcome

This project demonstrates an end-to-end local AI inference system with:

- Offline model execution
- Realtime benchmark dashboard
- Structured output validation
- Retry mechanism
- Model comparison
- Performance measurement
- Exportable benchmark reports
- System profile tracking
- Production-style API design

It shows how local SLMs can be evaluated for real-world constraints such as privacy, latency, cost, reliability, and edge deployment.

---

---




