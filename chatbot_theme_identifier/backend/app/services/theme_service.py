from app.services.llm_service import query_llm


def identify_themes(responses):
    combined = "\n\n".join([f"Response {i+1}: {res}" for i, res in enumerate(responses)])
    prompt = f"""
You are an AI assistant tasked with identifying common themes across multiple document responses.
Given the following responses from different documents, identify and describe all coherent themes you can find.
For each theme, list which documents (by ID) contributed to it.

Responses:
{combined}

Instructions:
- List each identified theme clearly.
- For each theme, mention which document(s) support it.
- Use bullet points or numbered format for clarity.
- Keep your output detailed and well-structured.

Themes:
"""
    return query_llm(prompt)