# RTIH RAG Starter — Technical Track

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dinesh1309/rtih-rag-starter/blob/main/notebook.ipynb)

**Fastest start:** click the badge above to open the notebook in Google Colab — no install, just paste your API key and run.

A working RAG pipeline in ~15 lines. Load your data, ask a question, get an answer grounded in **your** content — not the model's generic knowledge.

This is the five-step pattern, nothing more:

```
LOAD  ->  CHUNK  ->  EMBED  ->  STORE  ->  RETRIEVE  ->  answer
```

You change **two things**: the data folder, and the question. Everything else already works.

---

## Two ways to run it

### Option A — Google Colab (zero setup, recommended if you're not sure)
1. Open `notebook.ipynb` in [Google Colab](https://colab.research.google.com/) (File → Upload notebook).
2. Run the cells top to bottom.
3. Paste your OpenRouter API key when asked, upload your files, edit the question.

### Option B — Local repo (if your Python environment is ready)

**Prerequisites:** Python 3.9+. The install pulls a large dependency tree (langchain is big) — **expect ~2 minutes and a lot of console output. That's normal**, not an error. A virtual environment is recommended so it doesn't touch your system Python:

```bash
# 0. (recommended) isolate in a venv
python3 -m venv .venv && source .venv/bin/activate

# 1. install — pinned versions, ~2 min, lots of output is normal
pip install -r requirements.txt

# 2. add your key
cp .env.example .env        # then paste your key into .env

# 3. run  (first run also downloads the ~67MB embedding model, once)
python rag_starter.py
```

You should see an answer about Tower B's handover date, pulled from the sample emails.

---

## Make it YOUR data

1. Drop your files (`.txt` or `.md`) into the `data/` folder.
2. Open `rag_starter.py` and edit the two lines marked `>>>`:
   - `DATA_FOLDER` — your folder
   - `QUESTION` — a real query your product needs to answer
3. Run it again.

> **Where does my file go?**
> The code points at the **`data/` folder**, not at individual files — it scans the
> whole folder. So you just put your files in `data/`; you don't type a path per file.
>
> - **Running locally?** Put files inside `rtih-rag-starter/data/`, and run the script
>   from the `rtih-rag-starter/` folder (`data/` is a relative path).
> - **Running in Colab?** Colab is a cloud machine — it can't see your laptop. You must
>   **upload** your files into a `data/` folder there first (folder icon on the left).
>   Uploaded files are temporary and vanish when the runtime disconnects.
> - **Single-file loaders** (`CSVLoader`, `Docx2txtLoader`) are the exception — they
>   take the exact file path, e.g. `data/members.csv`. The file still has to be in
>   `data/` (locally) or uploaded to `data/` (Colab).

**Loading PDFs?** Uncomment `pypdf` in `requirements.txt`, then swap the loader:
```python
from langchain_community.document_loaders import PyPDFDirectoryLoader
docs = PyPDFDirectoryLoader(DATA_FOLDER).load()
```

---

## How the pieces map to the five steps

| Step | What it does | The line that does it |
|------|--------------|-----------------------|
| LOAD | reads your files | `DirectoryLoader(...).load()` |
| CHUNK | splits into small, retrievable pieces | `RecursiveCharacterTextSplitter(...)` |
| EMBED | turns each chunk into a vector (meaning) | `FastEmbedEmbeddings()` |
| STORE | saves vectors in a searchable DB | `Chroma.from_documents(...)` |
| RETRIEVE | finds the chunks closest to your question | `retriever.invoke(question)` |

Embeddings run **locally** (FastEmbed) — no key needed. Only the final answer step calls a model. **Pick your provider** — Anthropic, OpenAI, or OpenRouter (see Option A/B/C in `rag_starter.py`). The default is **OpenRouter**: one key runs Claude, GPT, and open-source models, and swapping between them is a one-line change. Get a key at [openrouter.ai/keys](https://openrouter.ai/keys), or use your own Anthropic/OpenAI key.

---

## Optional: persist to Supabase (upgrade path)

Chroma (the default) is local and friction-free — perfect for the live session. If you want your vectors to **persist** in a hosted database so S4/S5 agents can reuse them, swap the store for Supabase.

You'll need a free Supabase project with the `vector` extension enabled, then:

```python
# pip install langchain-postgres psycopg
from langchain_postgres import PGVector

CONNECTION = "postgresql+psycopg://user:pass@host:5432/postgres"  # from Supabase
db = PGVector.from_documents(chunks, FastEmbedEmbeddings(),
                             connection=CONNECTION, collection_name="my_docs")
```

Everything else (load, chunk, embed, retrieve, answer) stays identical — only the STORE step changes. Embeddings still run locally, so no embeddings key needed. *(Not pre-tested in this repo — needs your own Supabase project.)*

## Things to try in the activity

- Ask a question the data **does** contain → does it answer correctly?
- Ask a question the data **does not** contain → does it say "I don't know," or make something up?
- Make chunks bigger (`chunk_size=2000`) → does retrieval get *worse*? (It usually does — smaller, precise chunks beat big vague ones.)

That's the whole game. If your answer comes back grounded in your own data, you've hit the bar for Friday office hours.

## Troubleshooting

- **402 / "requires more credits" from OpenRouter** — OpenRouter reserves credit for the *maximum* output tokens, not what you actually use. The starter caps this with `max_tokens=512`, so a tiny balance is enough. If you still hit it, lower `max_tokens` further or add a little credit.
- **First run is slow** — the local embedding model (`bge-small`, ~130MB) downloads once on first run, then it's cached.
