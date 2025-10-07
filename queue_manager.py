import os
import json

class QueueManager:
    def __init__(self,
                 official_dir="seed_pool/official_suite",
                 interesting_dir="seed_pool/interesting_seeds",
                 state_path="seed_pool/queue_state.json"):
        self.official_dir = official_dir
        self.interesting_dir = interesting_dir
        self.state_path = state_path
        self.queue = []  # lista de dicts: {"name","path","coverage" (float or None)}
        os.makedirs(self.official_dir, exist_ok=True)
        os.makedirs(self.interesting_dir, exist_ok=True)

    def load_initial_names(self):
        """Carrega apenas nomes e paths, coverage fica None (lazy)."""
        files = [f for f in os.listdir(self.official_dir) if f.endswith(".lua")]
        for fname in files:
            path = os.path.join(self.official_dir, fname)
            self.queue.append({"name": fname, "path": path, "coverage": None})

    def ensure_coverage(self, seed_info, executor):
        """
        Garante que seed_info['coverage'] tenha um valor.
        Se coverage for None, executa executor.run_with_luacov no arquivo original.
        Retorna o valor (float) ou None se falhar.
        """
        if seed_info.get("coverage") is not None:
            return seed_info["coverage"]

        path = seed_info["path"]
        cov = executor.run_with_luacov(path)
        seed_info["coverage"] = cov  # pode ser float ou None
        return cov

    def add_seed(self, name, path, coverage):
        """Adiciona um novo seed (mutado) e ordena."""
        self.queue.append({"name": name, "path": path, "coverage": coverage})
        self.sort_queue()

    def requeue_original(self, seed_info):
        """Reinsere o seed original no final da fila."""
        self.queue.append(seed_info)

    def sort_queue(self):
        """Ordena por coverage (None conta como -inf, vai pro fim)."""
        def keyfn(s):
            c = s.get("coverage")
            return c if c is not None else -1.0  # None -> -1 para ficar no fim
        self.queue.sort(key=lambda s: keyfn(s), reverse=True)

    def pop_next(self):
        """Pega o próximo seed (ou None). Não calcula cobertura aqui."""
        if not self.queue:
            return None
        return self.queue.pop(0)

    def save_state(self, path=None):
        p = path or self.state_path
        with open(p, "w", encoding="utf-8") as f:
            json.dump(self.queue, f, indent=2)

    def load_state(self, path=None):
        p = path or self.state_path
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                self.queue = json.load(f)

    def __len__(self):
        return len(self.queue)
