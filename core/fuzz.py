# orchestrator.py
from ll_mutator import LLMmutator
from queue_manager import SeedQueue
from utils import get_coverage

def run_with_luacov(lua_file):
    """Executa script com luacov e retorna cobertura (%)"""
    # roda o script
    subprocess.run(["lua", "-lluacov", lua_file], capture_output=True)

    # gera relatório
    subprocess.run(["luacov"], capture_output=True)

    return get_coverage("luacov.report.out")

def main():
    mutator = LLMmutator()
    queue = SeedQueue()

    while True:
        seed_path = queue.get_next_seed()
        if not seed_path:
            print("⚠️ Nenhum seed disponível, encerrando.")
            break

        print(f"\n📌 Processando: {seed_path}")

        # ler script original
        with open(seed_path, "r", encoding="utf-8") as f:
            script_content = f.read()

        # mutar
        mutated_code, used_prompt = mutator.mutate(script_content)
        print(f"🔄 Mutação feita com prompt: {used_prompt}")

        mutated_file = queue.save_mutation(mutated_code, seed_name=os.path.basename(seed_path))
        print(f"✅ Mutação salva em {mutated_file}")

        # medir cobertura
        coverage = run_with_luacov(mutated_file)
        print(f"📊 Cobertura do mutado: {coverage:.2f}%")

        if coverage > 70.0:  # regra de interesse (exemplo)
            queue.promote_interesting(mutated_file)
            print("🌟 Mutação promovida para interesting_seeds")
        else:
            print("🗑️ Mutação descartada")

        # re-enfileira seed original baseado na cobertura
        queue.requeue(seed_path, coverage)
        print(f"🔁 Seed re-enfileirado com prioridade {coverage:.2f}%")

if __name__ == "__main__":
    main()