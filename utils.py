import re

def get_coverage(report_file="luacov.report.out"):
    """Extrai % de cobertura do relatório do luacov"""
    try:
        with open(report_file, "r", encoding="utf-8") as f:
            text = f.read()
        match = re.search(r"Total coverage:\s+([\d\.]+)%", text)
        if match:
            return float(match.group(1))
    except FileNotFoundError:
        return 0.0
    return 0.0
