# sdd-taskanalyzer

[![CI](https://github.com/Luisfilipenogue/sdd-taskanalyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/Luisfilipenogue/sdd-taskanalyzer/actions/workflows/ci.yml)

Projeto final do **Bootcamp III** — desenvolvimento orientado a especificação (SDD) com IA, Test Harness, CI/CD com GitHub Actions, containerização com Docker e governança ética de IA.

O `TaskAnalyzer` recebe uma lista de tarefas e calcula métricas: totais, tempo médio de conclusão (geral e por prioridade) e taxa de atraso.

## Arquitetura do repositório

```
sdd-taskanalyzer/
├── .github/workflows/ci.yml      # Pilar 1: pipeline CI (GitHub Actions)
├── Dockerfile                    # Pilar 2: empacotamento (python:3.11-slim)
├── docker-compose.yml            # Pilar 2: orquestração da suíte de testes
├── CONTEXT_RULES.md              # Pilar 3: governança da IA
├── specs/
│   ├── task_analyzer_spec.md     # contrato SDD (cenários Dado-Quando-Então)
│   ├── system_design_document.pdf
│   └── requirements.yaml
├── src/task_analyzer.py          # código gerado por IA e homologado por humano
├── tests/test_harness.py         # suíte pytest (21 testes)
├── requirements.txt
└── README.md
```

## Como executar

### Local
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest tests/test_harness.py -v
```

### Docker (um único comando)
```bash
docker compose run --rm tests
```
Para construir e executar passo a passo:
```bash
docker build -t sdd-taskanalyzer-tests .
docker run --rm sdd-taskanalyzer-tests
```

## CI/CD

O workflow `.github/workflows/ci.yml` roda em `ubuntu-latest` com Python 3.11 a cada **push** ou **pull request** nas branches `main` e `develop`: instala as dependências do `requirements.txt` e executa `pytest tests/test_harness.py -v`.

## Fluxo de trabalho

- `main` recebe mudanças via Pull Request.
- Branches de funcionalidade (`feature/*`), commits atômicos (`feat:`, `test:`, `docs:`, `ci:`, `build:`).
- Código gerado por IA só entra após: testes 100% aprovados, revisão humana contra `CONTEXT_RULES.md` e PR documentado.
