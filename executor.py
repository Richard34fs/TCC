import subprocess
import os
import re

class Executor:
    def __init__(self, lua_bin="lua"):
        self.lua_bin = lua_bin

    def run_with_luacov(self, filepath: str) -> float | None:
        """Executa script Lua com luacov e retorna cobertura (%) ou None se falhar."""

        # Remove relatórios antigos
        for f in ("luacov.report.out", "luacov.stats.out"):
            if os.path.exists(f):
                os.remove(f)

        # 1. Rodar com luacov
        try:
            result = subprocess.run(
                [self.lua_bin, "-lluacov", filepath],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                print(f"⚠️ Erro executando {filepath}:\n{result.stderr}")
                return None
        except Exception as e:
            print(f"⚠️ Falha ao rodar {filepath}: {e}")
            return None

        # 2. Gerar relatório
        subprocess.run(["luacov"], capture_output=True, text=True)

        # 3. Ler luacov.report.out
        if not os.path.exists("luacov.report.out"):
            return None

        with open("luacov.report.out", "r", encoding="utf-8") as f:
            report = f.read()

        # 4. Extrair linha "Total    Hits Missed Coverage"
        match = re.search(r"Total\s+\d+\s+\d+\s+([\d.]+)%", report)
        if match:
            return float(match.group(1))
        return None
