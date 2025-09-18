# queue_manager.py
import os
import shutil

class SeedQueue:
    def __init__(self, seed_dir="seed_pool/official_suite",
                 interesting_dir="seed_pool/interesting_seeds",
                 mutated_dir="seed_pool/mutated_scripts"):
        self.seed_dir = seed_dir
        self.interesting_dir = interesting_dir
        self.mutated_dir = mutated_dir
        os.makedirs(self.interesting_dir, exist_ok=True)
        os.makedirs(self.mutated_dir, exist_ok=True)

    def get_queue(self):
        """Lista seeds em ordem"""
        return sorted([os.path.join(self.seed_dir, f) for f in os.listdir(self.seed_dir) if f.endswith(".lua")])

    def get_next_seed(self):
        """Retorna o próximo da fila (ou None)"""
        queue = self.get_queue()
        return queue[0] if queue else None

    def requeue(self, seed_path):
        """Move seed para o fim da fila"""
        new_path = os.path.join(self.seed_dir, f"requeued_{os.path.basename(seed_path)}")
        shutil.move(seed_path, new_path)
        return new_path

    def save_mutation(self, mutated_code, seed_name):
        """Salva código mutado no diretório temporário"""
        out_path = os.path.join(self.mutated_dir, f"mutated_{seed_name}")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(mutated_code)
        return out_path

    def promote_interesting(self, mutated_path):
        """Move mutação para interesting_seeds"""
        new_path = os.path.join(self.interesting_dir, os.path.basename(mutated_path))
        shutil.move(mutated_path, new_path)
        return new_path
