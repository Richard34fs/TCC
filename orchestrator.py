from seed_pool.seed_manager import SeedManager
from queue_manager import SeedQueue
from llm.init_ollama import LLMClient
from executor import Executor
import os

def main():
    seed_manager = SeedManager()
    llm = LLMClient()
    executor = Executor()
    queue = SeedQueue()

    # Inicializa fila com seeds
    for seed in seed_manager.list_seeds():
        queue.push(seed, 0)

    while not queue.is_empty():
        _, seed_filename = queue.pop()
        seed_path = seed_manager.get_seed_path(seed_filename)

        # 1. Executa original
        original_cov = executor.run_with_luacov(seed_path)
        if original_cov is None:
            print(f"⚠️ Original {seed_filename} falhou, descartando.")
            continue

        with open(seed_path, "r", encoding="utf-8") as f:
            code = f.read()

        # 2. Gera mutação
        mutated_code = llm.mutate(code)

        # 3. Salva mutado
        mutated_path = os.path.join(seed_manager.interesting_dir, f"mutated_{seed_filename}")
        with open(mutated_path, "w", encoding="utf-8") as f:
            f.write(mutated_code)

        # 4. Executa mutado
        mutated_cov = executor.run_with_luacov(mutated_path)
        if mutated_cov is None:
            print(f"❌ Mutado {mutated_path} falhou, descartando.")
            os.remove(mutated_path)
            queue.push(seed_filename, 0)
            continue

        print(f"[{seed_filename}] Original: {original_cov:.2f}% | Mutado: {mutated_cov:.2f}%")

        # 5. Decide destino
        if mutated_cov > original_cov:
            print(f"✅ Mutação melhorou! Mantendo {mutated_path}")
            queue.push(seed_filename, 0)  # Original volta para fila
        else:
            print(f"❌ Mutação não melhorou, descartando {mutated_path}")
            os.remove(mutated_path)
            queue.push(seed_filename, 0)

if __name__ == "__main__":
    main()
