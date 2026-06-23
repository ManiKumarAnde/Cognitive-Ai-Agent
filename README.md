# 🤖 AI Agent from Scratch

A modular, from-scratch AI agent built in Python with memory, reasoning, tool use, and an optional Streamlit chat UI. The agent combines a local LLM (Microsoft Phi-2), a TF-IDF intent classifier, Wikipedia lookup, an expression calculator, and a persistent JSON memory store — all wired together through a utility-based decision brain.

---

## ✨ Features

| Capability | Details |
|---|---|
| 🧠 **LLM Backbone** | Microsoft `phi-2` via HuggingFace Transformers |
| 🎯 **Intent Classification** | TF-IDF + Logistic Regression (sklearn) |
| 💾 **Persistent Memory** | JSON file (`memory.json`) for personal facts |
| 🗄️ **SQLite Memory** | Optional key-value store (`memory.db`) |
| 📐 **Vector Memory** | TF-IDF cosine similarity for semantic recall |
| 🌐 **Wikipedia Tool** | Live Wikipedia search with query cleaning & spell correction |
| 🧮 **Calculator Tool** | Natural language math expression evaluator |
| 🧩 **Utility-Based Brain** | Scores and picks the best action for every input |
| 💬 **Streamlit Web UI** | Interactive chat interface |
| 🖥️ **CLI Mode** | Simple terminal REPL |

---

## 📁 Project Structure

```
ai_agent_from_scratch/
│
├── main.py                  # CLI entry point (terminal REPL)
├── memory.json              # Persistent personal-fact store
│
└── agent/
    ├── __init__.py
    ├── agent.py             # Core Agent: perception → reasoning → action
    ├── brain.py             # Utility-based decision engine (scores actions)
    ├── planner.py           # Routes intent to the Brain
    ├── intent_model.py      # TF-IDF + Logistic Regression intent classifier
    ├── llm_engine.py        # HuggingFace Phi-2 text generation wrapper
    ├── tools.py             # Wikipedia + Calculator tools
    ├── state.py             # In-session state & JSON memory persistence
    ├── sqlite_memory.py     # SQLite key-value memory store
    ├── vector_memory.py     # TF-IDF vector memory for semantic recall
    ├── actions.py           # Canned responses (greet, farewell, etc.)
    ├── goals.py             # Agent goal definitions
    └── web_app.py           # Streamlit chat UI
```

---

## 🏗️ Architecture Overview

```
User Input
    │
    ▼
AgentState.remember()          ← stores input in session history
    │
    ▼
Agent.think_and_act()
    │
    ├─ Greeting / Farewell?    ← Actions.greet() / farewell()
    ├─ Math expression?        ← CalculatorTool.calculate()
    ├─ "my X is Y" pattern?    ← AgentState.update_knowledge()
    ├─ "what is my X"?         ← AgentState.knowledge lookup
    │
    └─ Planner.decide()        ← TF-IDF intent + confidence
           │
           ├─ explain          → LLMEngine.generate() (informative prompt)
           ├─ recall_fact      → WikipediaTool.search()
           ├─ answer           → LLMEngine.generate() (direct prompt)
           └─ unknown/low-conf → Brain utility scoring → best action
```

### Brain Decision Logic

The `Brain` class scores each candidate action using a weighted utility formula:

```
score = w_accuracy × accuracy + w_risk × risk + w_cost × cost + w_learning × learning
```

Possible actions: `ANSWER_FROM_MEMORY`, `ANSWER_FROM_SEMANTIC`, `USE_WIKIPEDIA`, `ASK_CLARIFICATION`, `STORE_FACT`, `CONFIRM_STORAGE`, `REJECT_STORAGE`, `DO_NOTHING`

---

## ⚙️ Prerequisites

- **Python 3.9+**
- **pip**
- ~5 GB disk space (for the Phi-2 model download on first run)
- An internet connection on first run (model download + Wikipedia queries)

---

## 🚀 Steps to Run

### 1. Clone / navigate to the project

```bash
cd ai_agent_from_scratch
```

### 2. Create and activate a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install torch transformers scikit-learn wikipedia streamlit
```

> **Note:** On first run, the Phi-2 model (~5 GB) will be automatically downloaded from HuggingFace and cached in `~/.cache/huggingface/`.

### 4a. Run in CLI (terminal) mode

```bash
python main.py
```

You will see:
```
AI Agent started. Type 'exit' to quit.
You: 
```

### 4b. Run the Streamlit web UI

```bash
streamlit run agent/web_app.py
```

This opens a browser at `http://localhost:8501` with a full chat interface.

---

## 💬 Example Interactions

| You say | Agent does |
|---|---|
| `hello` | Greets you |
| `my name is Manik` | Stores "name → Manik" in memory |
| `what is my name?` | Recalls "Manik" from memory |
| `what is 25 * 4 + 10` | Calculates → `110` |
| `who is the prime minister of India` | Searches Wikipedia |
| `explain neural networks` | Uses LLM (Phi-2) to explain |
| `exit` | Stops the agent |

---

## 🔧 Configuration

| Setting | File | How to change |
|---|---|---|
| LLM model | `agent/llm_engine.py` line 7 | Replace `"microsoft/phi-2"` with any HuggingFace causal LM |
| Memory file | `agent/state.py` line 5 | Change `memory_file="memory.json"` |
| SQLite DB file | `agent/sqlite_memory.py` line 4 | Change `db_file="memory.db"` |
| Intent training data | `agent/intent_model.py` | Add more `texts` / `labels` pairs |
| Brain utility weights | `agent/brain.py` lines 4–9 | Tune `accuracy`, `risk`, `cost`, `learning` weights |

---

## 📦 Full Dependency List

```
torch
transformers
scikit-learn
wikipedia
streamlit
```

Install all at once:
```bash
pip install torch transformers scikit-learn wikipedia streamlit
```

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'transformers'` | Run `pip install transformers` |
| Model download is slow / fails | Ensure internet access; the Phi-2 model is ~5 GB |
| `wikipedia.exceptions.DisambiguationError` | Handled internally; agent falls back to LLM |
| Streamlit page is blank | Make sure you ran `streamlit run agent/web_app.py` (not `python`) |
| `torch` install fails on Windows | Use `pip install torch --index-url https://download.pytorch.org/whl/cpu` for CPU-only |

---

## 📄 License

This project is for educational purposes — built from scratch to demonstrate core AI agent concepts.
