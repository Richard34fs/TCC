# init_ollama.py
import ollama

def check_model():
    try:
        response = ollama.generate(
            model="starcoder2:instruct",
            prompt="Test prompt to check if starcoder2:instruct is running."
        )
        print(" Ollama e starcoder2:instruct iniciados com sucesso!")
    except Exception as e:
        print(" Erro ao iniciar o modelo:", e)

if __name__ == "__main__":
    check_model()
