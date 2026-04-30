# 🧠 Docker AI Doctor — Self-Healing Container System

An autonomous **AI-Powered DevOps Agent** for Docker containers using a multi-agent architecture. It monitors runtime behavior, diagnoses failures using LLMs, retrieves similar past issues via vector memory, and safely executes fixes using a controlled action layer.

---

## 🚀 Overview

Debugging container failures manually is slow and error-prone.

**Docker AI Doctor** solves this by:

* Continuously monitoring containers
* Analyzing logs using an AI agent
* Identifying root causes
* Suggesting and executing safe fixes
* Learning from past incidents using vector memory

> Think of it as a **self-healing system for Docker environments**

---

## 🧠 Key Features

### 🔍 Real-Time Monitoring

* Tracks container status (running, exited, restarting)
* Automatically detects failures
* Extracts logs for analysis

### 🤖 AI-Powered Diagnosis

* Uses LLMs to analyze logs
* Produces structured output:

  * Root cause
  * Severity
  * Suggested fix

### ⚡ Auto-Healing Engine

* Maps AI suggestions → safe actions
* Supports:

  * Restart container
  * Stop container
* Includes safety guardrails:

  * Severity filtering
  * Whitelisted actions only

### 🧩 Multi-Agent Architecture

Built using **LangGraph**:

* 🔍 Investigator → prepares logs
* 🧠 Diagnoser → finds root cause
* 🛠 Planner → maps fix to action
* ⚖️ Decision → applies safety rules
* ⚡ Executor → performs fix

### 🧠 Vector Memory (FAISS)

* Stores past failures using embeddings
* Retrieves similar incidents
* Improves accuracy over time

> This makes the system a **retrieval-augmented AI agent**

### 🎨 Interactive Dashboard (Streamlit)

* View container status
* Inspect logs
* Run AI diagnosis
* Trigger manual fixes
* Toggle auto-healing

---

## ⚙️ Tech Stack

* **Backend:** Python, Docker SDK
* **AI Layer:** OpenAI LLMs
* **Agent Framework:** LangGraph
* **Memory:** FAISS + Sentence Transformers
* **Frontend:** Streamlit

---

## 🧪 Demo Scenarios

### 🔴 Container Crash

```bash
docker run --name crash-test node:18 node -e "throw new Error('Boom')"
```

**AI Output:**

* Root Cause: Unhandled exception
* Severity: High
* Fix: Restart container

---

### 🔴 Missing Dependency

```bash
Cannot find module 'express'
```

**AI Output:**

* Root Cause: Missing dependency
* Fix: Install required package

> ⚠️ System suggests but does not auto-install (safe design)

---

### 🔴 Restart Loop / Failure

* Automatically detected
* Auto-restarted (if safe)

---

## ▶️ How to Run

### 1. Clone Repo

```bash
git clone <git-repo-url>
cd <cloned-repo-folder>
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create .env For API Key

```bash
OPENAI_API_KEY=your_key
```

---

### 5. Launch Dashboard

```bash
streamlit run frontend/app.py
```

---

## 🎥 Demo Flow

1. Start system
2. Launch broken container
3. Open UI
4. View logs
5. Click **Analyze**
6. Click **Fix** (or auto-fix runs)

---

## 🧠 How It Works

1. Monitor detects container failure
2. Logs are extracted
3. Agent analyzes logs using LLM
4. Similar past issues are retrieved (FAISS)
5. Fix is planned and validated
6. Safe action is executed

---

## ⚠️ Safety Design

* No arbitrary shell execution
* Only predefined safe actions
* Severity-based filtering

---

## 💡 Why This Project Matters

This project demonstrates:

* Agentic AI systems
* Tool-augmented LLMs
* Retrieval-Augmented Generation (RAG)
* Real-world DevOps automation
* Production-style system design

---

## 🚀 Future Improvements

* Kubernetes support
* Prometheus metrics integration
* Slack / alerting system
* Cloud deployment (AWS/GCP)
* Advanced planning agents

---

## ⭐ If you like this project

Give it a star ⭐ and feel free to contribute!
