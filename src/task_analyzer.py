"""TaskAnalyzer — análise de métricas de tarefas.

Implementa o contrato definido em specs/task_analyzer_spec.md,
seguindo as regras de CONTEXT_RULES.md.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

PRIORIDADES: tuple[str, ...] = ("alta", "media", "baixa")
CAMPOS_OBRIGATORIOS: tuple[str, ...] = (
    "id",
    "prioridade",
    "data_criacao",
    "data_conclusao",
)


class TaskValidationError(ValueError):
    """Levantada quando os dados de entrada violam o contrato."""


def _parse_data(valor: Any, campo: str, task_id: Any) -> datetime | None:
    """Converte `datetime` ou string ISO 8601 em `datetime`; `None` permanece `None`."""
    if valor is None:
        return None
    if isinstance(valor, datetime):
        return valor
    if isinstance(valor, str):
        try:
            return datetime.fromisoformat(valor)
        except ValueError as exc:
            raise TaskValidationError(
                f"Tarefa {task_id!r}: '{campo}' com formato inválido: {valor!r}"
            ) from exc
    raise TaskValidationError(
        f"Tarefa {task_id!r}: '{campo}' deve ser datetime, string ISO 8601 ou None"
    )


def _media(valores: list[float]) -> float:
    """Média aritmética arredondada a 2 casas; 0.0 se a lista for vazia."""
    if not valores:
        return 0.0
    return round(sum(valores) / len(valores), 2)


def _percentual(parte: int, total: int) -> float:
    """Percentual arredondado a 2 casas; 0.0 se o denominador for zero."""
    if total == 0:
        return 0.0
    return round(parte / total * 100, 2)


def analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    """Calcula métricas de produtividade a partir de uma lista de tarefas.

    Args:
        tasks: lista de dicionários com `id`, `prioridade`, `data_criacao`,
            `data_conclusao` (None se pendente) e, opcionalmente, `prazo`.

    Returns:
        Dicionário com `total_tarefas`, `total_concluidas`, `total_pendentes`,
        `tempo_medio_conclusao_horas`, `tempo_medio_por_prioridade` e
        `taxa_atraso_percentual`.

    Raises:
        TaskValidationError: entrada malformada, campo ausente, prioridade
            inválida, data inválida ou `data_conclusao < data_criacao`.
    """
    if not isinstance(tasks, list):
        raise TaskValidationError("A entrada deve ser uma lista de tarefas")

    horas_geral: list[float] = []
    horas_por_prioridade: dict[str, list[float]] = {p: [] for p in PRIORIDADES}
    concluidas_com_prazo = 0
    atrasadas = 0

    for tarefa in tasks:
        if not isinstance(tarefa, dict):
            raise TaskValidationError("Cada tarefa deve ser um dicionário")

        task_id = tarefa.get("id")
        for campo in CAMPOS_OBRIGATORIOS:
            if campo not in tarefa:
                raise TaskValidationError(
                    f"Tarefa {task_id!r}: campo obrigatório ausente: '{campo}'"
                )

        prioridade = tarefa["prioridade"]
        if prioridade not in PRIORIDADES:
            raise TaskValidationError(
                f"Tarefa {task_id!r}: prioridade inválida: {prioridade!r}"
            )

        criacao = _parse_data(tarefa["data_criacao"], "data_criacao", task_id)
        conclusao = _parse_data(tarefa["data_conclusao"], "data_conclusao", task_id)
        prazo = _parse_data(tarefa.get("prazo"), "prazo", task_id)

        if criacao is None:
            raise TaskValidationError(
                f"Tarefa {task_id!r}: 'data_criacao' não pode ser nula"
            )

        if conclusao is None:
            continue  # tarefa pendente

        if conclusao < criacao:
            raise TaskValidationError(
                f"Tarefa {task_id!r}: data_conclusao anterior à data_criacao"
            )

        horas = (conclusao - criacao).total_seconds() / 3600
        horas_geral.append(horas)
        horas_por_prioridade[prioridade].append(horas)

        if prazo is not None:
            concluidas_com_prazo += 1
            if conclusao > prazo:
                atrasadas += 1

    total_tarefas = len(tasks)
    total_concluidas = len(horas_geral)

    return {
        "total_tarefas": total_tarefas,
        "total_concluidas": total_concluidas,
        "total_pendentes": total_tarefas - total_concluidas,
        "tempo_medio_conclusao_horas": _media(horas_geral),
        "tempo_medio_por_prioridade": {
            p: _media(horas_por_prioridade[p]) for p in PRIORIDADES
        },
        "taxa_atraso_percentual": _percentual(atrasadas, concluidas_com_prazo),
    }
