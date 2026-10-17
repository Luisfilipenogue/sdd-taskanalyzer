# Especificação SDD — TaskAnalyzer

> Contrato de negócio executável. Reconstituído a partir da Fase 1; ajuste aos termos exatos da sua especificação do Google Docs, se houver diferença.

## 1. Objetivo
Analisar uma lista de tarefas e devolver métricas de produtividade.

## 2. Assinatura
```python
class TaskValidationError(ValueError): ...

def analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]: ...
```

## 3. Entrada
Cada tarefa é um dicionário com:

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `id` | `int` ou `str` | sim | Identificador |
| `prioridade` | `str` | sim | `"alta"`, `"media"` ou `"baixa"` |
| `data_criacao` | `datetime` ou ISO 8601 `str` | sim | Criação |
| `data_conclusao` | `datetime`, ISO 8601 `str` ou `None` | sim | `None` = pendente |
| `prazo` | `datetime`, ISO 8601 `str` ou `None` | não | Data limite |

## 4. Saída
Dicionário com exatamente estas chaves:

| Chave | Regra |
|---|---|
| `total_tarefas` | Quantidade de tarefas recebidas |
| `total_concluidas` | Tarefas com `data_conclusao` |
| `total_pendentes` | `total_tarefas - total_concluidas` |
| `tempo_medio_conclusao_horas` | Média de (`data_conclusao - data_criacao`) em horas das concluídas; `0.0` se nenhuma |
| `tempo_medio_por_prioridade` | Dict com `alta`, `media`, `baixa`, cada uma com a média em horas das concluídas daquela prioridade; `0.0` se nenhuma |
| `taxa_atraso_percentual` | % das tarefas concluídas **com prazo** cuja `data_conclusao > prazo`; denominador = concluídas com prazo; `0.0` se denominador zero |

Valores numéricos são `float` arredondados a 2 casas.

## 5. Regras de validação (`TaskValidationError`)
- Entrada não é lista, ou item não é dicionário.
- Campo obrigatório ausente.
- `prioridade` fora do domínio.
- Data em formato inválido.
- `data_conclusao < data_criacao`.

## 6. Cenários de aceite (Dado-Quando-Então)

**Cenário 1 — Sucesso.** Dado um conjunto com tarefas concluídas e pendentes de prioridades variadas, quando `analyze_tasks` é chamada, então retorna totais, tempos médios (geral e por prioridade) e taxa de atraso corretos.

**Cenário 2 — Datas inconsistentes.** Dado uma tarefa com `data_conclusao < data_criacao`, quando `analyze_tasks` é chamada, então levanta `TaskValidationError`.

**Casos de borda.** Dado lista vazia ou somente pendentes, quando chamada, então retorna médias `0.0` e taxa `0.0` sem exceção.
