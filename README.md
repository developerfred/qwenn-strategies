# Qwenn-Strategies

Neural-symbolic framework for strategy generation and verification with Bend2 static rules.

## Maintainer
**codingsh <codingsh@pm.me>**

## Description
Pipeline where Qwen3.5 generates BendLite programs → BendVM verifies static rules → engine executes → trace generation → backtest results.

### Features
- ✅ BendLite program generation
- ✅ Static verification (type checks, affine use, termination)
- ✅ Engine execution with full trace
- ✅ Backtest framework (planned)
- ✅ Clanker integration (planned)

### Compliance
- All strategies verified against Bend2 static rules
- Type safety verification
- Affine mode verification
- Termination guarantee verification

## Status
- [x] Framework implementado (7/7 testes passando)
- [x] Bend2 static verification
- [ ] Strategy generator WIP (planejado)
- [ ] Backtest framework (planejado)
- [ ] Clanker integration (planejado)

## Tests
```
$ cd /Volumes/MASS/qwenn-strategies
$ python3 -m pytest tests/
# 7 tests passing
```

## Architecture
```
Qwenn-Strategies
├── qwenn_strategies/       # Strategy framework
├── src/                    # Source files
├── tests/                  # Test suite
├── examples/               # Example strategies
├── pyproject.toml         # Project config
└── README.md              # This file
```

## Pipeline
1. Qwen gera programa BendLite a partir de prompt
2. Static verification (type checks, affine use, termination)
3. Engine execution with trace
4. Results analysis and backtesting

## Quick Start
```bash
# Install
pip install -r requirements.txt

# Generate strategy (exemplo)
qwenn-strategies --prompt "MA crossover 5/20 em ETH/USD"
```

## Integration with Clanker
This framework can be integrated with Clanker token launcher for:
- Automated strategy generation for new tokens
- Risk-compliant strategy recommendations
- AI droid strategy personalization
```