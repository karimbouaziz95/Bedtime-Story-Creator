# 🌙 Bedtime Story Creator

A multi-agent AI app that generates personalized bedtime stories for children. Enter a child's name, age, and interests — and get a unique, safe, and age-appropriate story in seconds.

Built with the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) and [Gradio](https://www.gradio.app/).

---

## ✨ Features

- 🎨 Personalized stories based on the child's name, age, and interests
- 🌍 Supports **English**, **German**, and **Arabic**
- 📏 Three story lengths: short (5-7 min), medium (10-15 min), long (20-30 min)
- 🧠 Optional fun facts woven into the story
- 🛡️ Built-in Guardian agent that checks every story for safety and age-appropriateness
- 🔄 Automatic revision loop — if the story fails the safety check, it gets revised (up to 3 attempts)
- 📡 Real-time status updates in the UI as the story is being generated

---

## 🤖 Agent Pipeline

```
User Input
    │
    ▼
🎨 Planner Agent       →  Creates targeted web search queries based on child's profile
    │
    ▼
🔍 Research Agent      →  Runs searches in parallel and gathers story inspiration
    │
    ▼
✍️  Writer Agent        →  Writes the full bedtime story using the research
    │
    ▼
🛡️  Guardian Agent      →  Evaluates the story for safety and quality
    │
    ├── ✅ Approved     →  Story delivered to the user
    └── ❌ Rejected     →  Writer revises (up to 3 attempts), then re-evaluated
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- An [OpenAI API key](https://platform.openai.com/api-keys)
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/bedtime-story-creator.git
cd bedtime-story-creator
```

### 2. Set up your environment

Create a `.env` file in the root of the project:

```bash
cp .env.example .env
```

Then open `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Install dependencies

**With uv (recommended):**
```bash
uv sync
```

**With pip:**
```bash
pip install -r requirements.txt
```

### 4. Run the app

**With uv:**
```bash
uv run main.py
```

**With Python:**
```bash
python main.py
```

The app will open automatically in your browser at `http://localhost:7860`.

---

## 🖥️ Usage

1. Enter the **child's name**
2. Select their **age** and **interests**
3. Choose a **story length**, **language**, and **moral lesson**
4. Optionally add a special character and topics to avoid under **"More options"**
5. Click **✨ Create Story** and watch the story come to life!

---

## 📁 Project Structure

```
bedtime-story-creator/
├── main.py              # Gradio UI and entry point
├── story_manager.py     # Orchestrates the full agent pipeline
├── planner_agent.py     # Plans web search queries
├── research_agent.py    # Performs web searches for inspiration
├── writer_agent.py      # Writes the bedtime story
├── guardian_agent.py    # Evaluates story safety and quality
├── pyproject.toml       # Project metadata and dependencies
├── requirements.txt     # Pip-compatible dependencies
└── .env.example         # Environment variable template
```

---

## ⚠️ Disclaimer

Stories are reviewed by an AI Guardian agent for child safety. However, AI can make mistakes — always review generated stories before sharing them with children.
