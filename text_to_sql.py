"""
RTIH — Text-to-SQL demo (the STRUCTURED-data track).

This is NOT RAG. For structured data (ERP, invoices, tables), you don't embed and
retrieve — the LLM writes a SQL query, the database runs it, and you get an EXACT
answer. No vectors, no embeddings.

Same LLM as the RAG starter (OpenRouter). Different job: it generates SQL.
"""
import os, sqlite3
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

load_dotenv()  # reads OPENROUTER_API_KEY

# 1. Build a tiny sample database — a project's invoices (Meadows Dev world) --
DB_PATH = "project.db"
con = sqlite3.connect(DB_PATH)
con.executescript("""
DROP TABLE IF EXISTS invoices;
CREATE TABLE invoices (
  id INTEGER PRIMARY KEY, vendor TEXT, description TEXT,
  amount INTEGER, due_date TEXT, status TEXT, days_overdue INTEGER
);
INSERT INTO invoices (vendor, description, amount, due_date, status, days_overdue) VALUES
  ('Otis', 'Tower A lift cars', 1850000, '2026-05-20', 'overdue', 22),
  ('Spark Electricals', 'Tower B electrical rework', 800000, '2026-05-25', 'overdue', 17),
  ('AquaSeal', 'Podium waterproofing', 1400000, '2026-05-15', 'overdue', 27),
  ('Spark Electricals', 'Floor 7 RCD installation', 120000, '2026-06-01', 'paid', 0),
  ('BuildRight', 'Tower A structural works', 5200000, '2026-04-30', 'paid', 0),
  ('AquaSeal', 'Basement tanking', 600000, '2026-06-05', 'pending', 0),
  ('Otis', 'Lift annual maintenance', 95000, '2026-05-10', 'overdue', 32),
  ('GreenScape', 'Podium landscaping', 750000, '2026-06-14', 'pending', 0);
""")
con.commit(); con.close()

# 2. Connect the DB + the LLM (OpenRouter — same key as the RAG starter) ------
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
llm = ChatOpenAI(
    model="anthropic/claude-haiku-4.5",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
    max_tokens=512,
)

# 3. Ask: the LLM writes SQL from the schema, then we run it -----------------
#    Direct LLM call — no extra langchain.chains import, so it just works in Colab.
# The schema is the CREATE TABLE text (column names + types). The LLM reads this
# so it knows what to query — without it, it would be guessing your column names.
SCHEMA = db.get_table_info()


def clean_sql(text):
    """Clean the LLM's reply down to a single runnable SQL statement.

    LLMs often wrap their answer in markdown fences (```sql ... ```) or prefix it
    with a label like "SQLQuery:". SQLite can't execute any of that, so we strip
    it out and hand back bare SQL.

    Args:
        text: the raw string the model returned.
    Returns:
        a clean SQL string, ready to run.
    """
    # 1. Remove markdown code fences if the model added them.
    s = text.strip().replace("```sql", "").replace("```sqlite", "").replace("```", "")
    # 2. Drop any leading label and keep only what comes after it.
    for p in ("SQLQuery:", "SQLite query:", "SQL:"):
        if p in s:
            s = s.split(p, 1)[1]
    # 3. Trim whitespace and a trailing semicolon so db.run() gets clean SQL.
    return s.strip().rstrip(";").strip()


def ask(question):
    """Answer a plain-English question by having the LLM write, then run, SQL.

    The whole text-to-SQL idea in one function:
        question -> LLM writes SQL (using the schema) -> database runs it -> result.

    Args:
        question: a natural-language question about the data,
                  e.g. "What is the total amount still overdue?".
    """
    # Hand the LLM the table schema and ask for ONLY the SQL (no chatter).
    # The schema is what lets it write a query against the right columns.
    prompt = (
        "You are a SQLite expert. Given this database schema:\n"
        f"{SCHEMA}\n\n"
        "Write ONE SQLite query that answers the question. "
        "Return ONLY the SQL — no explanation, no markdown.\n\n"
        f"Question: {question}"
    )
    sql = clean_sql(llm.invoke(prompt).content)   # LLM writes the SQL; we clean it
    answer = db.run(sql)                          # the database executes the query
    print(f"\nQ:   {question}\nSQL: {sql}\nA:   {answer}")


# 4. Ask in English — the LLM writes the query, the DB returns exact numbers --
ask("What is the total amount still overdue?")
ask("Which vendor have we paid the most in total, and how much?")
ask("How many invoices are more than 25 days overdue?")
