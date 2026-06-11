# Pre-Session Setup — Working With Your Own Data

**Build With AI: RTIH AP Startup Sprint**

> Tonight's job is small: get a couple of accounts and your data ready. **You do not
> need any code yet** — we share the code and walk through it together during the
> session. This takes about 20 minutes.

| | |
|---|---|
| Topic | Working with your own data — RAG, knowledge bases, and structured inputs |
| Your track | Technical (Python / LangChain) **or** Non-technical (Flowise) — pick one below |
| Time needed now | ~20 minutes |
| Session date | **Thursday, 11 June 2026 · 3:30–5:00 PM** |
| Office hours | Friday — bring one working query against your own data |

> We may update this before the session — re-check it the night before.

---

## 1. Everyone — do these first (both tracks)

These three matter more than any tool. Get them right and the session works.

- [ ] **Have your REAL data ready, not a sample.** The whole point is connecting AI to
  *your* business data — a folder of files, an export, or a database dump, whatever
  your product actually runs on. Just have it on hand; you don't upload anything yet.
- [ ] **Write down ONE real question** your product needs to answer from that data.
  Example (PropTech): *"What is the new handover date for Tower B and why did it change?"*
- [ ] **Redact anything sensitive.** Remove customer PII, passwords, account numbers.
  Once data goes into a cloud tool, treat it as no longer private. When in doubt, mask it.

**What format should my data be in?**

| Data type | Examples | Good format to have |
|---|---|---|
| Unstructured | emails, PDFs, Word docs, chat logs | `.txt` / `.md` / `.pdf`, or `.mbox` / `.json` email export |
| Semi-structured | spreadsheets, bug DBs, Notion exports | `.csv` or `.json` (export Notion as Markdown/JSON) |
| Structured | ERP, inventory, accounting | a database dump, or confirm you have export/API access |

> If your data is a database or ERP (not documents), flag it — your path is a little
> different (we cover this in the session). You still attend and set up normally.

---

## 2. Technical track — just two things (no code yet)

Tonight you only need two things ready. On the session day we share the code (a GitHub
link), and it installs everything else for you. Nothing else to set up now.

- [ ] **Install Python** (version 3.8 or newer) — download from
  **https://www.python.org/downloads/** and run the installer. On Windows, tick
  **"Add Python to PATH"** during install.
- [ ] **Get one API key** — pick a provider, sign up, create the key, save it somewhere safe:
  - **OpenRouter** — one key works for Claude, GPT, and open-source models.
    **https://openrouter.ai/keys** (`sk-or-...`). You may need a small amount of credit to
    run the models — add enough to test.
  - **Anthropic** — **https://console.anthropic.com** (`sk-ant-...`), or
  - **OpenAI** — **https://platform.openai.com** (`sk-...`).

Plus your data and one question from Section 1. That is the whole setup.

**You are ready (technical) when:** Python is installed, your API key is saved, and your
data + one question are ready.

---

## 3. Non-technical track — Flowise (no code, no flow-building)

- [ ] **Create a free Flowise account** and confirm you can log in. Sign up at
  **https://cloud.flowiseai.com** — the **free plan ($0)** is enough for the session and
  needs no install. Keep your document small (the free plan has limited storage).
- [ ] **Get one API key** for the answer step — OpenRouter, OpenAI, or Anthropic (same
  links as above). Keep a small balance on it so it can be tested. You will paste it into
  a node during the session.
- [ ] **Have your primary document** ready in `.pdf`, `.txt`, or Google Doc export, plus
  one question.
- [ ] You do **not** build anything beforehand — we share a starter flow and build it
  together during the session.

**You are ready (non-technical) when:** you can log into Flowise, your API key is saved,
and your document + one question are ready.

---

## 4. Quick self-check (everyone)

- [ ] I know which track I am on (technical or Flowise).
- [ ] My real data is ready, in a sensible format, with sensitive parts removed.
- [ ] I have written down one real question.
- [ ] I have an API key saved.
- [ ] (Technical) Python is installed on my machine.
- [ ] (Flowise) My instance is running and I can log in.

---

## On the day (so you know what to expect)

- **Technical:** we share the code via a GitHub link and run it on your machine together.
  The code installs the libraries it needs, then you paste your API key, drop in your
  data, and ask your question — live.
- **Non-technical:** we share a Flowise starter flow and build it together, then you load
  your document and ask your question.

Nothing to download or run before then. Just come ready with the accounts and data above.
