# CONTEXT_RULES.md — Governança de IA do projeto TaskAnalyzer

Estas regras devem ser fornecidas ao assistente de IA **junto com** `specs/task_analyzer_spec.md` em toda sessão de geração de código.

## 1. Hierarquia de fontes
1. `specs/task_analyzer_spec.md` é a única fonte de verdade sobre o comportamento do sistema.
2. Este arquivo define **como** o código deve ser escrito.
3. Se algo não estiver nas duas fontes, a IA deve **perguntar ou declarar a lacuna**; nunca inventar regra de negócio.

## 2. Stack e estilo
- Python **3.11+**.
- **Type hints em 100%** das funções, parâmetros e retornos.
- Apenas biblioteca padrão no código de produção. Dependências autorizadas: `pytest` (somente testes).
- Docstrings curtas em português descrevendo contrato, entradas e exceções.
- Um único arquivo de produção: `src/task_analyzer.py`.

## 3. Tratamento de erros
- Usar apenas exceções específicas; proibido `except:` ou `except Exception:` genérico.
- Violações do contrato de dados levantam `TaskValidationError` (subclasse de `ValueError`) com mensagem clara.
- **Prevenção de divisão por zero**: toda média ou percentual deve checar o denominador e retornar `0.0` quando for zero.
- Entrada vazia (`[]`) é válida e nunca levanta exceção.

## 4. Proibições (anti-alucinação)
- Não criar funções, campos de saída, parâmetros ou regras que não estejam na especificação.
- Não usar bibliotecas externas (pandas, numpy, etc.).
- Não importar módulos inexistentes nem citar APIs de que não se tenha certeza.
- Não alterar nomes das chaves de saída definidas na especificação.
- Não imprimir (`print`) nem acessar rede/disco dentro de `analyze_tasks`.
- A função não deve mutar a lista de entrada.

## 5. Homologação humana
Todo código gerado por IA só entra na `main` após:
1. Execução de `pytest` com 100% de aprovação.
2. Revisão humana confrontando o código com cada item deste arquivo e da especificação.
3. Pull Request documentado com checklist de conformidade.
