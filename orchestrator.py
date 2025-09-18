from seed_pool.seed_manager import SeedManager
from queue_manager import SeedQueue
from llm.init_ollama import LLMClient
from executor import Executor

def main():
    seed_manager = SeedManager()
    llm = LLMClient()
    executor = Executor()
    queue = SeedQueue()

    # Inicializa fila com seeds
    for seed in seed_manager.list_seeds():
        queue.push(seed, 0)  # prioridade inicial 0

    # Loop
    while not queue.is_empty():
        _, seed_filename = queue.pop()
        seed_path = seed_manager.get_seed_path(seed_filename)

        # Lê código original
        with open(seed_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Gera mutação
        mutated_code = llm.mutate(code)

        # Salva mutação em interesting_seeds
        seed_manager.move_to_interesting(seed_filename, mutated_code)

        # Executa mutação com luacov e mede cobertura
        coverage = executor.run_with_luacov(seed_path)

        # Quanto maior a cobertura, mais cedo ele volta pra fila
        priority = -coverage
        queue.push(seed_filename, priority)

        print(f"Seed {seed_filename} -> cobertura {coverage}% (prioridade {priority})")

if __name__ == "__main__":
    main()
