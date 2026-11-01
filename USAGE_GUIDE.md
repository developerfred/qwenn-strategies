# 🧠 Qwenn-Strategies - Guia de Utilização

## Visão Geral
Framework neural-symbolic para geração e verificação de estratégias de trading com regras static Bend2.

## 🚀 Quick Start

### Instalação
```bash
# Clonar repositório
git clone git@github.com:developerfred/qwenn-strategies.git
cd qwenn-strategies

# Instalar dependências
pip install -r requirements.txt
```

### Gerar Estratégia MA Crossover
```python
from qwenn_strategies.strategy_gen import generate_strategy

program = generate_strategy(
    market_data="ETH/USD price data: 70,72,68,65,67,71,73,70,69,72",
    strategy_type="ma_crossover",
    parameters={"period": 14}
)

print(program)
# Output: Programa BendLite para estratégia de crossover de médias móveis
```

### Verificar Estratégia
```python
from qwenn_strategies.strategy_gen import verify_strategy

program = """
import Base
def main() -> U32:
    +tvls: List[U32] = [129055918773, 28919628159, 21928811565]
    +first: U32 = +tvls[0]
    +second: U32 = +tvls[1]
    if +second > +first: +result: U32 = +second
    else: +result: U32 = +first
    +result
"""

result = verify_strategy(program)
print(f"Valid: {result['valid']}")
print(f"Type Check: {result['type_check']}")
print(f"Affine Check: {result['affine_check']}")
print(f"Termination Check: {result['termination_check']}")
print(f"Errors: {len(result['errors'])}")
```

## 📋 Tipos de Estratégia Suportados

### MA Crossover (Média Móvel Cruzada)
```python
from qwenn_strategies.strategy_gen import generate_strategy

program = generate_strategy(
    market_data="ETH/USD: 70,72,68,65,67,71,73,70,69,72",
    strategy_type="ma_crossover",
    parameters={"period": 14}
)

# O programa gerado inclui:
# - Média móvel curta (period)
# - Média móvel longa (period + 20)
# - Sinal BUY quando ma_short > ma_long
# - Sinal HOLD caso contrário
```

### RSI Strategy
```python
from qwenn_strategies.strategy_gen import generate_strategy

program = generate_strategy(
    market_data="ETH/USD: 70,72,68,65,67,71,73,70,69,72",
    strategy_type="rsi",
    parameters={"period": 14, "overbought": 70, "oversold": 30}
)

# O programa gerado inclui:
# - Cálculo RSI interno no BendLite
# - Sinais BUY quando RSI <= oversold
# - Sinais SELL quando RSI >= overbought
# - Sinal HOLD quando neutro
```

## 🔧 Verificação de Regras Static (Bend2)

### Verificar Programa BendLint
```python
from qwenn_strategies.strategy_gen import verify_strategy

program = """
import Base
def main() -> U32:
    +tvls: List[U32] = [129055918773, 28919628159]
    +first: U32 = +tvls[0]
    +second: U32 = +tvls[1]
    if +second > +first: +result: U32 = +second
    else: +result: U32 = +first
    +result
"""

result = verify_strategy(program)
print(f"""
🔍 Resultados da Verificação:
  Valid: {result['valid']}               ✅ Passa regras static
  Type Check: {result['type_check']}     ✅ Tipo consistente
  Affine Check: {result['affine_check']} ✅ Uso affine consistente
  Termination Check: {result['termination_check']} ✅ Terminação garantida
  Errors: {len(result['errors'])}         {'Zero = compliance' if not result['errors'] else 'Errors found'}
""")
```

### O Que os Checks Significam

| Check | Significado | Status Esperado |
|-------|-------------|-----------------|
| **Valid** | Programa passa em todas as regras static | `True` |
| **Type Check** | Tipos de dados consistentes (U32, Nat, etc.) | `True` |
| **Affine Check** | Variáveis usadas corretamente com operador `+` | `True` |
| **Termination Check** | Programa termina (sem recursão infinita) | `True` |
| **Errors** | Lista de erros encontrados (se houver) | `[]` (ideal) |

## 📊 Pipeline Completo

### Pipeline de Geração e Verificação
```
1. Qwen gera programa BendLite a partir de prompt
2. Static verification (type checks, affine use, termination)
3. Engine execution with trace
4. Results analysis and backtesting
```

### Exemplo de Pipeline Completo
```python
from qwenn_strategies.strategy_gen import generate_strategy, verify_strategy, execute_strategy

# Step 1: Gerar programa
program = generate_strategy(
    market_data="ETH/USD: 70,72,68,65,67,71,73,70,69,72",
    strategy_type="rsi",
    parameters={"period": 14, "overbought": 70, "oversold": 30}
)

print("📝 Programa Gerado:")
print(program[:500] + "...")

# Step 2: Verificar regras static
verify_result = verify_strategy(program)
print("\n🔍 Verificação Bend2:")
print(f"  Valid: {verify_result['valid']}")
print(f"  Errors: {len(verify_result['errors'])}")

# Step 3: Executar estratégia
market_data = "70,72,68,65,67,71,73,70,69,72"
execute_result = execute_strategy(program, market_data)
print(f"\n⚡ Execução:")
print(f"  Success: {execute_result['success']}")
print(f"  Compliance: {execute_result['compliance']}")
print(f"  Result (U32): {execute_result['result']}")
print(f"  Trace tokens: {len(execute_result['trace'])}")
```

## 🧪 Testes

```bash
# Executar todos os testes
python3 -m pytest tests/

# Expected output:
============================= test session starts ==============================
platform darwin -- Python 3.14.1, pytest-9.0.2, pluggy-1.6.0 -- /opt/homebrew/Cellar/python@3.14/3.14.1/lib/python3.14/bin/python3.14
cachedir: .pytest_cache
rootdir: /Volumes/MASS/qwenn-strategies
configfile: pyproject.toml
plugins: anyio-4.12.0, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 7 items

tests/test_framework.py::test_generate_ma_crossover PASSED               [ 14%]
tests/test_framework.py::test_generate_rsi_strategy PASSED               [ 28%]
tests/test_framework.py::test_verify_strategy_valid PASSED               [ 42%]
tests/test_framework.py::test_verify_strategy_invalid PASSED             [ 57%]
tests/test_framework.py::test_verify_strategy_missing_main PASSED        [ 71%]
tests/test_framework.py::test_execute_strategy PASSED                    [ 85%]
tests/test_framework.py::test_generate_all_types PASSED                  [100%]

============================== 7 passed in 0.02s ==============================
```

## 📁 Estrutura do Repositório
```
qwenn-strategies/
├── qwenn_strategies/          # Framework principal
│   ├── __init__.py
│   ├── strategy_gen.py        # geração e verificação de estratégias
│   └── ...                   # módulos adicionais
├── src/                       # Arquivos fonte
├── tests/                     # Testes unitários (7 testes)
├── examples/                  # Exemplos de estratégias
├── pyproject.toml             # Configuração do projeto
├── README.md                  # Documentação principal
└── USAGE_GUIDE.md             # Este guia (novo)
```

## 🔧 Parâmetros de Estratégia

### Parâmetros RSI
| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| **period** | 14 | Período de cálculo RSI |
| **overbought** | 70 | Limite sobrecompra (RSI >= questo valor = SELL) |
| **oversold** | 30 | Limite sobrevendido (RSI <= isso = BUY) |

### Parâmetros MA Crossover
| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| **period** | [14, 34] | Períodos [curto, longo] da média móvel |

## 🎯 Casos de Uso

### Trading Automatizado
```python
# Gerar estratégia para token específico
program = generate_strategy(
    market_data=f"TOKEN/USD: {price_series}",
    strategy_type="rsi",
    parameters={"period": 14, "overbought": 70, "oversold": 30}
)

# Verificar compliance antes de executar
verify_result = verify_strategy(program)
if verify_result['valid']:
    print("✅ Estratégia compliant - pode executar")
    execute_result = execute_strategy(program, market_data)
else:
    print(f"❌ {len(verify_result['errors'])} erros de compliance")
```

### Avaliação de Novo Token (Clanker Integration)
```python
from qwenn_strategies.strategy_gen import generate_strategy, verify_strategy

# Analisar token recém-lançado pelo Clanker
token_info = {
    "symbol": "BRNE",
    "name": "Bringing Next Billion",
    "type": "clanker_v4"
}

program = generate_strategy(
    market_data=f"{token_info['symbol']} analysis: TVL high, recent launch",
    strategy_type="ma_crossover",
    parameters={"period": [14, 30]}
)

verify_result = verify_strategy(program)
print(f"Token {token_info['symbol']} compliance: {verify_result['valid']}")
```

## 🚦 Melhores Práticas

### 1. Sempre Verificar Compliance
```python
# NUNCA execute uma estratégia sem verificar antes
verify_result = verify_strategy(program)
if not verify_result['valid']:
    print(f"❌ Rejeitar: {verify_result['errors']}")
    return
```

### 2. Use Parâmetros Adequados
- Para RSI: period >= 10, overbought > 70, oversold < 30
- Para MA Crossover: long_period > short_period

### 3. Monitore o Trace
- O campo `trace` no execute_strategy mostra a sequência de tokens executados
- Útil para debugging e entender o fluxo do programa

### 4. Testar com Dados Históricos
- Sempre teste estratégias com dados passados antes de usar em trading real
- Use o campo `backtest` ou implemente seu próprio backtest

## ⚠️ Erros Comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `affine violation` | Variável usada >1 vez sem `+` | Reestruturar programa para usar `+` |
| `recursion detected` | Recursão infinita detectada | Remover ou limitar recursão |
| `missing main` | Programa sem `def main()` | Adicionar função main |
| `invalid program` | Programa mal estruturado | Revisar sintaxe BendLite |

## 🆘 Suporte

- **Issues:** GitHub Issues do repositório
- **Discussions:** Discussions na aba Discussions
- **Exemplos:** Confira a pasta `examples/` do repositório

## 📜 Licença
Apache-2.0 - See LICENSE file for details.