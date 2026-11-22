"""Lê o plano de estudos em gemini-notebook.md."""

import re
from pathlib import Path

TITULO = re.compile(r"^### Notebook (\d+) — (.+)$", re.M)


def titulos_notebooks(caminho: Path) -> dict[int, str]:
    """Mapeia o número de cada notebook para o título do plano."""
    return {
        int(numero): titulo.strip()
        for numero, titulo in TITULO.findall(caminho.read_text(encoding="utf-8"))
    }
