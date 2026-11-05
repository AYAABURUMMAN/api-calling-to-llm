Week 3 (Text to SQL)

This project allows users to ask questions about a university database in English.

The AI converts the question into an SQL query, runs it on PostgreSQL, and returns a short answer in English.

Setup

Load the database into PostgreSQL as university_db.

Create a .env file:

API_KEY=your_api_key
BASE_URL=your_api_url
DB_PASSWORD=your_database_password

Install the required libraries:

pip install -r requirements.txt

Run

python task_text_to_sql.py

Type your question in English.

Type exit to stop the program.

The questions, SQL queries, and answers are saved in results.csv.