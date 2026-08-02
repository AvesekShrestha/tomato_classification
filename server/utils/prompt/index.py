def get_prompt(tomato_class: str) -> str:
    prompt = f"""
    I will provide the predicted class of a tomato leaf disease. Based on the class name, return the response strictly in valid JSON format.

    The JSON must include:
    - predicted_class: The exact disease class provided
    - cause: A short, farmer-friendly sentence explaining what causes this disease (pathogen, pest, environmental factors, etc.)
    - prescriptions: A list of complete recommendation sentences, not only product or treatment names. Each item should say what to use or do and why.

    Guidelines:
    - Keep recommendations practical and farmer-friendly
    - Include both treatment and prevention steps when possible
    - Avoid overly technical chemical jargon
    - Prefer product types or common market names instead of only scientific chemical names
    - Do not write prescription items as titles like "Insecticidal Soap" or "Copper Fungicide"
    - Write prescription items like "Use insecticidal soap to control the affected pests." or "Apply a copper-based fungicide to slow the spread of leaf spots."
    - Do not include any text outside the JSON

    Disease class: {tomato_class}
    """
    return prompt
