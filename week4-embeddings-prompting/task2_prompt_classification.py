import llm_client

reviews = [
    "Works exactly as described, very happy with it.",
    "Arrived late and the box was broken.",
    "The screen is gorgeous but the battery barely lasts two hours.",
    "Oh great, another phone that dies by noon. Just what I needed.",
]

for review in reviews:
    weak_prompt = f"Is this review good? {review}"

    structured_prompt = f"""Classify the customer review into exactly ONE label: positive, negative, or mixed.
Reply with the label only, nothing else.

Review: "Works exactly as described." -> positive
Review: "Arrived late and broken." -> negative
Review: "Great camera but terrible price." -> mixed

Review: "{review}" ->"""

    print("REVIEW:", review)
    print("  WEAK      :", llm_client.chat(weak_prompt))
    print("  STRUCTURED:", llm_client.chat(structured_prompt))
    print()