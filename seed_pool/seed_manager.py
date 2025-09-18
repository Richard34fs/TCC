import os
import shutil

class SeedManager:
    def __init__(self, base_path="seed_pool"):
        self.official_dir = os.path.join(base_path, "official_suite")
        self.interesting_dir = os.path.join(base_path, "interesting_seeds")

    def list_seeds(self):
        return sorted(os.listdir(self.official_dir))

    def get_seed_path(self, filename):
        return os.path.join(self.official_dir, filename)

    def move_to_interesting(self, filename, mutated_code):
        dst = os.path.join(self.interesting_dir, f"mutated_{filename}")
        with open(dst, "w", encoding="utf-8") as f:
            f.write(mutated_code)
        return dst

if __name__ == "__main__":
    sm = SeedManager()
    seeds = sm.list_seeds()
    print("Seeds:", seeds)
