"""
RTIH Session 3 — RAG Starter (technical track)

The five-step RAG pipeline in plain LangChain:
    LOAD -> CHUNK -> EMBED -> STORE -> RETRIEVE -> answer

You only need to change THREE things (look for the >>> markers):
    1. Point it at YOUR data folder.
    2. Ask YOUR question.
    3. Pick YOUR provider — Anthropic, OpenAI, or OpenRouter. Your choice.

Embeddings run locally (FastEmbed) — no API key needed for that part.
The only thing that needs an API key is the final answer step. Pick ONE provider
below. OpenRouter is the default (one key works for Claude, GPT, and open-source
models, and you swap between them by changing one line), but you can use Anthropic
or OpenAI directly if you already have a key for them.
"""

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI  # OpenRouter speaks the OpenAI dialect

load_dotenv()  # reads OPENROUTER_API_KEY from your .env file

# >>> 1. DROP YOUR DATA HERE — point this at your folder of .txt / .md files
DATA_FOLDER = "data/"

# >>> 2. ASK YOUR QUESTION HERE — a real query your product needs to answer
QUESTION = "What is the new handover date for Tower B and why did it change?"


# ============================================================================
# 1. LOAD — bring YOUR data in. This is the ONLY step that changes per format.
#    Everything after (chunk -> embed -> store -> retrieve -> answer) is identical.
#    Every loader below just produces a list of Documents. Pick ONE; the default
#    loads .txt from data/. Install notes are in requirements.txt.
# ============================================================================

# --- Text / Markdown (default — no extra install) ---------------------------
docs = DirectoryLoader(DATA_FOLDER, glob="**/*.txt", loader_cls=TextLoader).load()
# For Markdown, change the glob:
# docs = DirectoryLoader(DATA_FOLDER, glob="**/*.md", loader_cls=TextLoader).load()

# --- PDFs (pip install pypdf) -----------------------------------------------
# from langchain_community.document_loaders import PyPDFDirectoryLoader
# docs = PyPDFDirectoryLoader(DATA_FOLDER).load()

# --- Word .docx (pip install docx2txt) --------------------------------------
# from langchain_community.document_loaders import Docx2txtLoader
# docs = Docx2txtLoader(f"{DATA_FOLDER}/yourfile.docx").load()

# --- CSV / spreadsheet, one row at a time (no extra install) -----------------
# from langchain_community.document_loaders import CSVLoader
# docs = CSVLoader(f"{DATA_FOLDER}/yourdata.csv").load()

# --- Notion export (export pages as Markdown, then) -------------------------
# from langchain_community.document_loaders import NotionDirectoryLoader
# docs = NotionDirectoryLoader(DATA_FOLDER).load()
#   Simplest: export Notion as Markdown and use the .md text loader above.

# --- Emails (pip install unstructured) --------------------------------------
# from langchain_community.document_loaders import UnstructuredEmailLoader
# docs = DirectoryLoader(DATA_FOLDER, glob="**/*.eml",
#                        loader_cls=UnstructuredEmailLoader).load()
#   Most reliable live: export each email to a .txt and use the default loader.

# --- HTML / web pages (pip install beautifulsoup4) --------------------------
# from langchain_community.document_loaders import WebBaseLoader
# docs = WebBaseLoader(["https://example.com/page"]).load()

# --- Logs + profiles / any table or DB rows (pip install pandas) ------------
#   Connectree-style structured data: pull rows with pandas (CSV, JSON, or a SQL
#   query), build one text column, then embed it.
# import pandas as pd
# from langchain_community.document_loaders import DataFrameLoader
# df = pd.read_csv(f"{DATA_FOLDER}/members.csv")     # or pd.read_sql(query, conn)
# df["text"] = df.apply(lambda r: f"Member {r['name']}: {r['notes']}", axis=1)
# docs = DataFrameLoader(df, page_content_column="text").load()

# --- UNIVERSAL fallback: any weird format -> build Documents yourself --------
#   If no loader fits, read your data into strings and wrap each one. Always
#   works, because the pipeline only needs Document objects.
# from langchain_core.documents import Document
# records = [("source-name", "the text content")]    # you produce this list
# docs = [Document(page_content=text, metadata={"source": name})
#         for name, text in records]

# NOTE — two data types do NOT load here (see BLOCK2_DATA_TYPES.md):
#   * Structured ERP / database (VIDURAi): use text-to-SQL, not embeddings.
#   * Sensor / ML data (Vahini): a model-training problem, not retrieval.

# 2. CHUNK — split into small pieces the AI can retrieve precisely
chunks = RecursiveCharacterTextSplitter(
    chunk_size=800, chunk_overlap=100
).split_documents(docs)

# 3. EMBED + 4. STORE — turn chunks into vectors and save them in Chroma
db = Chroma.from_documents(chunks, FastEmbedEmbeddings())

# 5. RETRIEVE — find the chunks most relevant to the question
retriever = db.as_retriever(search_kwargs={"k": 4})

# >>> 3. PICK YOUR PROVIDER — uncomment ONE option. You only need one key.
#
# Option A (default): OpenRouter — one key for every model. Change MODEL to swap
# brains (Claude / GPT / open-source) without touching anything else.
#     Browse models + live prices at https://openrouter.ai/models
MODEL = "anthropic/claude-haiku-4.5"   # or "openai/gpt-4o-mini", "meta-llama/llama-3.3-70b-instruct"
llm = ChatOpenAI(
    model=MODEL,
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
    max_tokens=512,   # IMPORTANT: OpenRouter reserves credit for the MAX output tokens.
                      # Without this it reserves ~64k and a small balance gets a 402.
                      # A RAG answer is short — 512 is plenty and keeps cost tiny.
)

# Option B: Anthropic directly (needs ANTHROPIC_API_KEY in your .env)
# from langchain_anthropic import ChatAnthropic
# llm = ChatAnthropic(model="claude-haiku-4-5")

# Option C: OpenAI directly (needs OPENAI_API_KEY in your .env)
# llm = ChatOpenAI(model="gpt-4o-mini")
# ============================================================================
# ANSWER — one helper, reused for the demo question AND the interactive loop.
# Each question retrieves its OWN fresh context (stateless — ideal for testing data).
# ============================================================================
def answer(question):
    context = "\n\n".join(d.page_content for d in retriever.invoke(question))
    prompt = (
        "Answer the question using ONLY the context below. "
        "If the answer is not in the context, say 'I don't know based on the provided data.'\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )
    return llm.invoke(prompt).content


# Demo run with the default question
print("\nQUESTION:", QUESTION)
print("ANSWER:", answer(QUESTION))

# Now ask as many of your own questions as you want — a tiny chat loop.
print("\n--- Ask your own questions (type 'quit' to stop) ---")
while True:
    q = input("\nAsk a question: ").strip()
    if q.lower() in ("quit", "exit", "q", ""):
        print("Done.")
        break
    print(">", answer(q))
