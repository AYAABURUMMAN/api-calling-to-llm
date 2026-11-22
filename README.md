Week 4 - Embeddings and Prompt Engineering

WHAT I DID

Task 1 - Embeddings: Embedded 8 sample sentences with the local model all-MiniLM-L6-v2 (384-dim vectors) and compared all pairs with cosine similarity. I used a local model because I could not find an embeddings model available with the course API key (common names returned "Invalid model name"). Set EMBEDDING_MODEL in .env to use an API model instead.

Task 2 - Prompts: For summarization, classification and extraction, I ran a weak and a structured prompt (instruction, constraints, output format, few-shot examples for classification) on the same inputs with gpt-5.6-luna and compared the outputs.

FILES

llm_client.py: chat API helper (settings from .env)

task1_embeddings.py: embeddings and similarity scores

task2_prompt_summarization.py, task2_prompt_classification.py, task2_prompt_extraction.py

.env.example: required variable names (no secrets)

RUN

pip install -r requirements.txt

copy .env.example .env (then fill in your values)

python task1_embeddings.py

python task2_prompt_summarization.py

python task2_prompt_classification.py

python task2_prompt_extraction.py

OBSERVATIONS

Embeddings:

Top pairs: cat/kitten (0.629), password/login (0.628), stock/shares (0.598). They share almost no words, so the model captures meaning.

The two "bank" sentences (river vs. money) scored 0.454, far above unrelated pairs (about 0), so the shared word pulls them together.

Scores are not close to 1 because wording differs; the ranking matters more than the absolute value.

Prompts:

Summarization: [write 1-2 sentences in your own words: did the weak prompt add an intro or bullets? did the structured one keep to 2 sentences?]

Classification: "Is this review good?" was read as a question about writing quality, so the model rewrote the reviews. The structured prompt (fixed labels, label-only output, 3 examples) classified the tested reviews correctly, including the sarcastic one.

Extraction: The structured prompt returned valid JSON every time, used null for the missing deadline, and picked the right deadline when two dates appeared. The weak prompt returned bullet lists and once added a year (2026) not in the email.

LIMITATIONS

Each prompt was run once on very few examples, so these are observations, not proof.

All texts are invented samples; no real personal data.

Embeddings were computed locally, not with the course API.