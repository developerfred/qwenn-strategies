# Qwenn-Strategies
Framework neural-symbolic para geração e verificação de estratégias de trading.

## Maintainer
**codingsh <codingsh@pm.me>**

## Description
Pipeline onde Qwen3.5 gera programas BendLite → BendVM verifica static rules → 
engine executa → trace generation → backtest results.

## Pipeline
1. Qwen gera programa BendLite a partir de prompt
2. Static verification (type checks, affine use, termination)
3. Engine execution with trace
4. Results analysis

## Status
- [ ] Strategy generator (WIP)
- [ ] BendVM verification (planned)
- [ ] Engine execution (planned)
- [ ] Backtest framework (planned)

## Quick Start
```bash
# Install
pip install -r requirements.txt

# Generate strategy (quando implementado)
qwenn-strategies --prompt "MA crossover 5/20 em ETH/USD"
```