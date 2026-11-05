import os
import requests
import psycopg2
import pandas as pd
from dotenv import load_dotenv

# Settings
load_dotenv()               # read the .env file
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Stop early if a setting is missing
if not API_KEY or not BASE_URL or not DB_PASSWORD:
    raise ValueError("API_KEY, BASE_URL or DB_PASSWORD not found. Check your .env file.")

HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
MODEL = "gpt-5.6-luna"

DB_CONFIG = {
    "dbname": "university_db",
    "user": "postgres",
    "password": DB_PASSWORD,
    "host": "localhost",
    "port": 5432,
}

#  Database description (for the LLM only) 
# The LLM cannot see our database so we list the tables and columns for it
SCHEMA = """
departments(id, name, code, budget)
courses(id, code, title, credits, department_id)
instructors(id, person_id, department_id, rank, salary)
people(id, first_name, last_name, email, gender, date_of_birth)
programs(id, name, degree_level, credits_required, department_id)
students(id, person_id, program_id, status, enrollment_date)
sections(id, course_id, instructor_id, semester_id, capacity)
enrollments(id, student_id, section_id, letter_grade, grade_points)
"""



def ask_llm(prompt):
    """Send one prompt to the LLM and return its text answer."""
    payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}]}
    r = requests.post(BASE_URL, headers=HEADERS, json=payload, timeout=30)
    r.raise_for_status()                                          # error on 4xx/5xx
    return r.json()["choices"][0]["message"]["content"].strip()   # the reply text


def question_to_sql(question):
    """Step 1: the LLM turns the question into a SQL query."""
    prompt = (
        "You are a PostgreSQL expert. Use only this schema:\n"
        f"{SCHEMA}\n"                                            # give it the tables
        "Write ONE SELECT query that answers the question below. "
        "Return only the SQL, with no explanation and no markdown.\n"
        f"Question: {question}"
    )
    sql = ask_llm(prompt)
    return sql.replace("```sql", "").replace("```", "").strip()   # remove code fences


def run_query(sql):
    """Step 2: run the SQL on university_db and return the result as a table."""
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        conn.set_session(readonly=True)         # safety: can never change the data
        with conn.cursor() as cur:
            cur.execute(sql)
            columns = [col[0] for col in cur.description]         # column names
            rows = cur.fetchall()
    finally:
        conn.close()                            # always close the connection
    return pd.DataFrame(rows, columns=columns)

def result_to_answer(question, df):
    """Step 3: the LLM turns the table into a plain English answer."""

    if df.empty:
        return "No data found."

    table = df.to_string(index=False)

    prompt = (
        "Answer the question in one or two plain English sentences, "
        "using only the data below.\n"
        f"Question: {question}\n\nData:\n{table}"
    )

    return ask_llm(prompt)



print("""
Welcome! This assistant answers questions about a university database.
The database holds information about students, courses, departments,
instructors, degree programs and grades. Ask anything about this data
in plain English, and the assistant will find the answer and reply in
plain English. Type 'exit' to stop.
""")

results = []                                    # every question asked in this session
while True:
    question = input("\nYour question: ").strip()
    if question.lower() == "exit":              # the user wants to stop
        break
    if not question:                            # empty input: ask again
        continue

    sql, answer = "", ""
    try:
        sql = question_to_sql(question)                           # question -> SQL
        if not sql.lower().startswith("select"):                  # only allow SELECT
            raise ValueError("the model did not return a SELECT query")
        df = run_query(sql)                                       # SQL -> table
        answer = result_to_answer(question, df)                   # table -> answer
        status = "ok"
    except Exception as e:
        status = f"error: {e}"         

    print(f"\nSQL:    {sql}")
    print(f"Answer: {answer}" if status == "ok" else f"Status: {status}")
    results.append({"question": question, "sql": sql, "answer": answer, "status": status})

# Save everything that was asked in this session
if results:
    pd.DataFrame(results).to_csv("results.csv", index=False, encoding="utf-8-sig")
    print("\nSaved to results.csv")