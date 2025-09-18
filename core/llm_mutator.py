# ll_mutator.py
import ollama
import random

class LLMmutator:
    def __init__(self, model="starcoder2:instruct", prompts_file="prompts.txt"):
        self.model = model
        self.prompts = self._load_prompts(prompts_file)

    def _load_prompts(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def mutate(self, script_content: str) -> str:
        """Escolhe um prompt aleatório e aplica mutação"""
        prompt = random.choice(self.prompts)
        response = ollama.generate(
            model=self.model,
            prompt=f"{prompt}\n\nHere is the Lua script:\n{script_content}\n\nMutated version:"
        )
        return response["response"], prompt
