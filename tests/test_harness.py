"""Test Harness — traduz os cenários de aceite da especificação SDD."""

import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.task_analyzer import TaskValidationError, analyze_tasks  # noqa: E402


def dt(dia: int, hora: int = 0) -> datetime:
    return datetime(2026, 1, dia, hora)


@pytest.fixture
def tarefas_cenario_1() -> list[dict]:
    return [
        # alta: 10h, dentro do prazo
        {"id": 1, "prioridade": "alta", "data_criacao": dt(1, 8),
         "data_conclusao": dt(1, 18), "prazo": dt(2, 0)},
        # alta: 20h, atrasada
        {"id": 2, "prioridade": "alta", "data_criacao": dt(1, 0),
         "data_conclusao": dt(1, 20), "prazo": dt(1, 12)},
        # media: 4h, dentro do prazo
        {"id": 3, "prioridade": "media", "data_criacao": dt(2, 8),
         "data_conclusao": dt(2, 12), "prazo": dt(3, 0)},
        # baixa: 6h, sem prazo (fora da taxa de atraso)
        {"id": 4, "prioridade": "baixa", "data_criacao": dt(3, 6),
         "data_conclusao": dt(3, 12)},
        # pendentes
        {"id": 5, "prioridade": "media", "data_criacao": dt(4, 8),
         "data_conclusao": None, "prazo": dt(5, 0)},
        {"id": 6, "prioridade": "baixa", "data_criacao": dt(4, 9),
         "data_conclusao": None},
    ]


# ---------- Cenário 1: sucesso ----------

def test_cenario1_totais(tarefas_cenario_1):
    r = analyze_tasks(tarefas_cenario_1)
    assert r["total_tarefas"] == 6
    assert r["total_concluidas"] == 4
    assert r["total_pendentes"] == 2


def test_cenario1_tempo_medio_geral(tarefas_cenario_1):
    # (10 + 20 + 4 + 6) / 4 = 10.0
    assert analyze_tasks(tarefas_cenario_1)["tempo_medio_conclusao_horas"] == 10.0


def test_cenario1_tempo_medio_por_prioridade(tarefas_cenario_1):
    r = analyze_tasks(tarefas_cenario_1)["tempo_medio_por_prioridade"]
    assert r == {"alta": 15.0, "media": 4.0, "baixa": 6.0}


def test_cenario1_taxa_atraso(tarefas_cenario_1):
    # 3 concluídas com prazo, 1 atrasada -> 33.33%
    assert analyze_tasks(tarefas_cenario_1)["taxa_atraso_percentual"] == 33.33


def test_cenario1_aceita_strings_iso():
    tarefas = [{"id": "a", "prioridade": "alta",
                "data_criacao": "2026-01-01T08:00:00",
                "data_conclusao": "2026-01-01T10:30:00",
                "prazo": "2026-01-01T12:00:00"}]
    r = analyze_tasks(tarefas)
    assert r["tempo_medio_conclusao_horas"] == 2.5
    assert r["taxa_atraso_percentual"] == 0.0


def test_cenario1_nao_muta_entrada(tarefas_cenario_1):
    copia = [dict(t) for t in tarefas_cenario_1]
    analyze_tasks(tarefas_cenario_1)
    assert tarefas_cenario_1 == copia


# ---------- Cenário 2: erro ----------

def test_cenario2_data_conclusao_anterior_a_criacao():
    tarefas = [{"id": 1, "prioridade": "alta",
                "data_criacao": dt(2, 10), "data_conclusao": dt(1, 10)}]
    with pytest.raises(TaskValidationError, match="anterior"):
        analyze_tasks(tarefas)


def test_cenario2_task_validation_error_e_value_error():
    assert issubclass(TaskValidationError, ValueError)


@pytest.mark.parametrize("tarefa", [
    {"id": 1, "prioridade": "urgente", "data_criacao": dt(1), "data_conclusao": None},
    {"id": 2, "prioridade": "alta", "data_conclusao": None},
    {"id": 3, "prioridade": "alta", "data_criacao": "ontem", "data_conclusao": None},
    {"id": 4, "prioridade": "alta", "data_criacao": 123, "data_conclusao": None},
])
def test_validacoes_de_contrato(tarefa):
    with pytest.raises(TaskValidationError):
        analyze_tasks([tarefa])


@pytest.mark.parametrize("entrada", ["texto", None, {"id": 1}, [1, 2]])
def test_entrada_malformada(entrada):
    with pytest.raises(TaskValidationError):
        analyze_tasks(entrada)


# ---------- Casos de borda ----------

ZERADO = {
    "total_tarefas": 0,
    "total_concluidas": 0,
    "total_pendentes": 0,
    "tempo_medio_conclusao_horas": 0.0,
    "tempo_medio_por_prioridade": {"alta": 0.0, "media": 0.0, "baixa": 0.0},
    "taxa_atraso_percentual": 0.0,
}


def test_borda_lista_vazia():
    assert analyze_tasks([]) == ZERADO


def test_borda_somente_pendentes():
    tarefas = [
        {"id": 1, "prioridade": "alta", "data_criacao": dt(1), "data_conclusao": None},
        {"id": 2, "prioridade": "baixa", "data_criacao": dt(2), "data_conclusao": None,
         "prazo": dt(3)},
    ]
    r = analyze_tasks(tarefas)
    assert r["total_tarefas"] == 2
    assert r["total_concluidas"] == 0
    assert r["total_pendentes"] == 2
    assert r["tempo_medio_conclusao_horas"] == 0.0
    assert r["tempo_medio_por_prioridade"] == {"alta": 0.0, "media": 0.0, "baixa": 0.0}
    assert r["taxa_atraso_percentual"] == 0.0


def test_borda_concluida_sem_prazo_nao_divide_por_zero():
    tarefas = [{"id": 1, "prioridade": "media", "data_criacao": dt(1, 0),
                "data_conclusao": dt(1, 3)}]
    r = analyze_tasks(tarefas)
    assert r["taxa_atraso_percentual"] == 0.0
    assert r["tempo_medio_conclusao_horas"] == 3.0


def test_borda_conclusao_igual_criacao_e_valida():
    tarefas = [{"id": 1, "prioridade": "alta", "data_criacao": dt(1, 5),
                "data_conclusao": dt(1, 5)}]
    assert analyze_tasks(tarefas)["tempo_medio_conclusao_horas"] == 0.0


def test_borda_conclusao_exatamente_no_prazo_nao_e_atraso():
    tarefas = [{"id": 1, "prioridade": "alta", "data_criacao": dt(1, 0),
                "data_conclusao": dt(1, 10), "prazo": dt(1, 10)}]
    assert analyze_tasks(tarefas)["taxa_atraso_percentual"] == 0.0
