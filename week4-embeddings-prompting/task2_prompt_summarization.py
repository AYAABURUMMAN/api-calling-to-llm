import llm_client

texts = {
    "ARTICLE": (
        "Jordan's tech sector has grown steadily over the past decade, driven by a young, "
        "well-educated workforce and a rising number of startups in Amman. Investors point to "
        "strong software talent, but founders say access to late-stage funding remains limited, "
        "and many move abroad to scale. The government has launched programs to support "
        "digital skills and early-stage companies."
    ),
    "STORY": (
        "Omar found a tiny kitten shivering outside his school one rainy morning. He wrapped it in "
        "his jacket and carried it to class, hiding it under his desk. When the teacher noticed, "
        "Omar braced for a scolding, but she smiled and called a nearby shelter. By afternoon the "
        "kitten was warm, fed, and waiting for a new home."
    ),
}

for name, text in texts.items():
    weak_prompt = f"Summarize this. {text}"

    structured_prompt = f"""Summarize the text below for a busy reader.
Constraints: maximum 2 sentences, neutral tone, use only information from the text.
Output format: one plain paragraph, no bullet points, no introduction.

Text: \"\"\"{text}\"\"\""""

    print("=====", name, "=====")
    print("WEAK      :", llm_client.chat(weak_prompt))
    print("STRUCTURED:", llm_client.chat(structured_prompt))
    print()