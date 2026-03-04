def get_prompt(tomato_class: str) -> str:
    prompt = f"""
    I will provide the predicted class of a tomato leaf disease. Based on the class name, return the response strictly in valid JSON format.

    The JSON must include:
    - predicted_class: The exact disease class provided
    - cause: What causes this disease (pathogen, environmental factors, etc.)
    - prescriptions: A list of commonly available pesticides, fungicides, or practical treatments that farmers can easily buy in local markets. Prefer product types or common market names instead of only scientific chemical names.

    Guidelines:
    - Keep recommendations practical and farmer-friendly
    - Include both treatment and prevention steps when possible
    - Avoid overly technical chemical jargon
    - Do not include any text outside the JSON

    Disease class: {tomato_class}
    """
    return prompt
