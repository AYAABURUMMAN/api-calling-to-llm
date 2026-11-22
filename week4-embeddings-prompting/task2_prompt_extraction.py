import json
import llm_client

emails = [
    "Hi team, this is Sara Haddad. Please send the updated invoice to the finance office "
    "before Thursday 12 March. Thanks!",

    "Hello, Khaled here. Could you review the attached project proposal when you get a chance? "
    "Thanks.",

    "Dear team, this is Omar Nasser. The meeting moved to Sunday at 10am. "
    "Please confirm your attendance by Friday.",
]

for email in emails:
    weak_prompt = f"Get the info from this email. {email}"

    structured_prompt = f"""Extract these fields from the email below: sender_name, deadline, requested_action.
I need this for automated processing, so reply with ONLY valid JSON and nothing else.
If a field is not stated in the email, use null instead of guessing.

Use exactly this structure:
{{"sender_name": "...", "deadline": "...", "requested_action": "..."}}

Email: \"\"\"{email}\"\"\""""

    weak_answer = llm_client.chat(weak_prompt)
    structured_answer = llm_client.chat(structured_prompt)

    try:
        json.loads(structured_answer)
        is_json = True
    except ValueError:
        is_json = False

    print("EMAIL:", email)
    print("  WEAK      :", weak_answer)
    print("  STRUCTURED:", structured_answer)
    print("  Structured is valid JSON?", is_json)
    print()