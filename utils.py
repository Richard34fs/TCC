import re

def parse_luacov_report(report_file="luacov.report.out"):
    """Extrai % de cobertura do relatório do luacov (Total Coverage)"""
    try:
        with open(report_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Procura linha que começa com "Total"
        for line in lines:
            if line.startswith("Total"):
                parts = line.split()
                if len(parts) >= 4:
                    coverage_str = parts[-1]  # Ex: "66.67%"
                    return float(coverage_str.replace("%", ""))
    except FileNotFoundError:
        return 0.0

    return 0.0
