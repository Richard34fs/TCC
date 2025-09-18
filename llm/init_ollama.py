import ollama
import random

class LLMClient:
    def __init__(self, model="starcoder2:instruct", prompt_file="llm/prompts.txt"):
        self.model = model
        self.prompts = self._load_prompts(prompt_file)

    def _load_prompts(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def random_prompt(self):
        return random.choice(self.prompts)

    def mutate(self, code, prompt=None):
        if prompt is None:
            prompt = self.random_prompt()
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a Lua code mutator."},
                {"role": "user", "content": f"{prompt}\n\n{code}"}
            ]
        )
        return response["message"]["content"]
