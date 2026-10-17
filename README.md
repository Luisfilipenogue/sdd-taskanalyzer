# sdd-taskanalyzer

![tests](https://img.shields.io/badge/pytest-100%25%20passed-brightgreen)

Projeto da disciplina **Bootcamp III** — desenvolvimento orientado a especificação (SDD) com IA, Test Harness e versionamento Git/GitHub.

O `TaskAnalyzer` recebe uma lista de tarefas e calcula métricas: totais, tempo médio de conclusão (geral e por prioridade) e taxa de atraso.

## Estrutura

```
sdd-taskanalyzer/
├── README.md
├── CONTEXT_RULES.md          # regras de governança da IA
├── .gitignore
├── requirements.txt
├── specs/task_analyzer_spec.md   # contrato SDD
├── src/task_analyzer.py          # código gerado via IA e homologado por humano
└── tests/test_harness.py         # suíte pytest (cenários 1, 2 e bordas)
```

## Como executar

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

Requer Python 3.11+.

## Exemplo

```python
from src.task_analyzer import analyze_tasks

analyze_tasks([
    {"id": 1, "prioridade": "alta", "data_criacao": "2026-01-01T08:00:00",
     "data_conclusao": "2026-01-01T10:00:00", "prazo": "2026-01-01T12:00:00"},
])
```

## Fluxo de trabalho

- `main` protegida; mudanças entram via Pull Request.
- Branches: `feature/sdd-specification`, `feature/test-harness`, `feature/task-analyzer-impl`.
- Commits atômicos (`feat:`, `test:`, `docs:`).

## Status do build

Testes: **100% aprovados** (ver `pytest -v`). CI/CD será adicionado na Fase 3.
