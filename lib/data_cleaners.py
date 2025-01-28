class Cleanser:
    def ensure_gpt_format(self, text) -> str:
        return text \
        .replace("```json", "") \
        .replace("```", "") \
        .replace("'", "\'") \
        .replace('"', '\"') \
        .replace("'", '"') \
        .replace("```python", "") \
        .strip("python").split("=")[-1].strip()

    def no_quote(self, text) -> str:
        return text \
        .replace("'", "") \
        .replace('"', '')