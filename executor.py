import subprocess
from utils import get_coverage

class Executor:
    def __init__(self, lua_path="lua"):
        self.lua_path = lua_path

    def run_with_luacov(self, script_path):
        """Executa o script com luacov e retorna a cobertura (%)"""
        # Limpa relatório anterior
        subprocess.run(["rm", "-f", "luacov.report.out"], check=False)

        # Executa script
        subprocess.run([self.lua_path, "-lluacov", script_path], check=False)

        # Gera relatório
        subprocess.run([self.lua_path, "-lluacov", "-e", "require('luacov.runner').shutdown()"], check=False)

        # Extrai cobertura
        return get_coverage("luacov.report.out")

if __name__ == "__main__":
    ex = Executor()
    coverage = ex.run_with_luacov("seed_pool/official_suite/hello.lua")
    print("Cobertura:", coverage)