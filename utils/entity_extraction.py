import json
import re

def build_extraction_prompt(enquiry_text: str, extraction_fields: list[str], instructions: str = "") -> str:
    fields_list = "\n".join(f"- {field.replace('_', ' ').capitalize()}" for field in extraction_fields)
    prompt = f"""
You are an expert entity extraction assistant.
{instructions}

Extract the following fields from the enquiry text and return a JSON object with exact keys:

{fields_list}

Enquiry text:
\"\"\"{enquiry_text}\"\"\"

Output only the JSON object, no markdown or extra text.
"""
    return prompt.strip()

def extract_entities_with_gpt(client, enquiry_text: str, customer_config: dict) -> dict:
    prompt = build_extraction_prompt(
        enquiry_text,
        extraction_fields=customer_config.get("fields", []),
        instructions=customer_config.get("prompt_instructions", "")
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    text = response.choices[0].message.content.strip()
    print("GPT extraction raw output:", text)  # Debug log

    # Remove markdown code fences if present
    if text.startswith("```"):
        # Remove lines starting and ending with ```
        lines = text.splitlines()
        cleaned_lines = [line for line in lines if not line.strip().startswith("```") and not line.strip().endswith("```")]
        text = "\n".join(cleaned_lines).strip()

    try:
        data = json.loads(text)
    except Exception:
        print("Failed to parse JSON from GPT output.")
        data = {}
    return data

def extract_email_from_text(text: str) -> str | None:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else None
