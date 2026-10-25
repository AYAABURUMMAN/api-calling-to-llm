import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
)

while True:
    question = input("\nEnter your question (or type exit): ").strip()

    if question.lower() == "exit":
        print("Bye!")
        break

    if question:
        response = client.chat.completions.create(
            model="gpt-5.6-luna",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": question},
            ],
        )

        print("\nAI Answer:")
        print(response.choices[0].message.content)
    else:
        print("Please enter a question.")