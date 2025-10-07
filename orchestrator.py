import os
from queue_manager import QueueManager
from llm.init_ollama import LLMClient
from executor import Executor

def main():
    llm = LLMClient()
    executor = Executor()
    queue = QueueManager()

    # Carrega apenas nomes (coverage fica None - será calculado quando selecionado)
    queue.load_initial_names()
    print(f"✅ Fila inicial carregada (sem cobertura inicial). {len(queue)} seeds.")

    # Loop principal
    while len(queue) > 0:
        seed_info = queue.pop_next()
        if seed_info is None:
            break

        name = seed_info["name"]
        path = seed_info["path"]

        print(f"\n🔄 Selecionado {name} — verificando cobertura original (se necessário).")

        # Só executa luacov no original se coverage for None (primeira vez)
        original_cov = queue.ensure_coverage(seed_info, executor)
        if original_cov is None:
            print(f"⚠️ Original {name} falhou ao executar, descartando do fluxo.")
            # não re-enfileira; passa ao próximo
            continue

        print(f"📌 Cobertura original de {name}: {original_cov:.2f}%")

        # Lê código original
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        # 1. Gera mutação
        mutated_code = llm.mutate(code)
        mutated_filename = f"mutated_{os.path.splitext(name)[0]}.lua"
        mutated_path = os.path.join(queue.interesting_dir, mutated_filename)
        with open(mutated_path, "w", encoding="utf-8") as f:
            f.write(mutated_code)

        # 2. Executa mutado
        mutated_cov = executor.run_with_luacov(mutated_path)
        if mutated_cov is None:
            print(f"❌ Mutado {mutated_filename} falhou (syntax/runtime). Descarta-se.")
            try:
                os.remove(mutated_path)
            except OSError:
                pass
            # original volta pro fim da fila (sem alterar coverage)
            queue.requeue_original(seed_info)
            continue

        print(f"📊 Cobertura — Original: {original_cov:.2f}% | Mutado: {mutated_cov:.2f}%")

        # 3. Decisão: se mutado melhor que original, mantem mutado na fila
        if mutated_cov > original_cov:
            print(f"✅ Mutação melhorou: adicionando {mutated_filename} (cov {mutated_cov:.2f}%) à fila.")
            queue.add_seed(mutated_filename, mutated_path, mutated_cov)
            # opcional: poderíamos também atualizar coverage do original se quiser
        else:
            print(f"❌ Mutação não melhorou: descartando {mutated_filename}.")
            try:
                os.remove(mutated_path)
            except OSError:
                pass

        # 4. Reinsere o original no fim da fila (com coverage já preenchida)
        queue.requeue_original(seed_info)

        # 5. Reordena a fila (se quiser manter ordenada por coverage)
        queue.sort_queue()

        print(f"🪣 Fila atual (top 10): {[s['name'] for s in queue.queue[:10]]}")

        # opcional: salva estado a cada iteração
        # queue.save_state()

if __name__ == "__main__":
    main()
