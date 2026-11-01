"""Strategy generation module for Qwenn-Strategies.

This module provides the core functionality for generating
BendLite trading strategies using Qwen3.5 + LoRA.
"""

from __future__ import annotations

from typing import List, Optional, Dict, Any


def generate_strategy(
    market_data: str,
    strategy_type: str = "ma_crossover",
    parameters: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Generate a BendLite strategy program using Qwen3.5.

    Args:
        market_data: Description or data of market conditions
        strategy_type: Type of strategy (ma_crossover, rsi, etc.)
        parameters: Optional strategy parameters

    Returns:
        BendLite program source code as string

    Example:
        >>> program = generate_strategy(
        ...     "ETH/USD price data: 70,72,68,65,67,71,73,70,69,72",
        ...     "rsi",
        ...     {"period": 14, "overbought": 70, "oversold": 30}
        ... )
        >>> print(program)
    """
    # TODO: Integrate with Qwen3.5 + LoRA for actual generation
    # For now, return a template BendLite program

    if parameters is None:
        parameters = {}

    period = parameters.get("period", 14)
    overbought = parameters.get("overbought", 70)
    oversold = parameters.get("oversold", 30)

    # Template BendLite program for MA crossover strategy
    if strategy_type == "ma_crossover":
        program = f"""
import Base

def ma_period(c: Nat, prices: List[U32]) -> U32:
    # Média móvel simples para período c
    match c:
        case 0n: 0
        case 1n+p: (prices[p] + ma_period(p, prices) : U32)

def main() -> U32:
    // Strategy: MA crossover
    // Short period: {period[0] if isinstance(period, list) else period}
    // Long period: {period[1] if isinstance(period, list) else period + 20}
    // Receive prices via prompt
    run(ma_short(prices)) > run(ma_long(prices)) -> BUY
    -> HOLD
"""
    elif strategy_type == "rsi":
        program = f"""
import Base

def rsi_period(periodo: Nat, precos: List[U32]) -> U32:
    # RSI calculado exatamente dentro de BendLite
    match periodo:
        case 0n: 50
        case 1n+p: rsi_calc(p, precos)

def rsi_calc(p: Nat, precos: List[U32]) -> U32:
    # Simplified RSI calculation
    match p:
        case 0n: 50
        case 1n+q: 
            // Compare current vs previous
            (precos[q] > precos[0] ? 1 : 0) + rsi_calc(q, precos)

def main() -> U32:
    // RSI strategy
    // Period: {period}
    // Overbought: {overbought}
    // Oversold: {oversold}
    // Generate signal
    run(rsi_signal(prices)) -> BUY
    run(rsi_signal(prices)) -> SELL
    -> HOLD
"""
    else:
        # Generic template
        program = f"""
import Base

def main() -> U32:
    // {strategy_type} strategy
    // Parameters: {parameters}
    // Receive market data via prompt
    // Generate trading signal
    run(generate_signal) -> BUY
    -> HOLD
"""

    return program


def verify_strategy(program_source: str) -> Dict[str, Any]:
    """
    Verify a BendLite program obeys static rules.

    Args:
        program_source: BendLite program source code

    Returns:
        Dict with verification results:
        - valid: bool (passes static rules)
        - errors: list of error messages (if any)
        - type_check: bool
        - affine_check: bool
        - termination_check: bool
    """
    # TODO: Integrate with BendVM verification
    # For now, return template verification result

    # Parse basic structure checks
    has_def = "import Base" in program_source
    has_main = "def main()" in program_source
    has_return = "->" in program_source and "U32" in program_source

    # Basic heuristic checks
    errors = []

    # Check for affine use issues (variables used more than once without +)
    # This is a simplified check
    var_usage: Dict[str, int] = {}
    for line in program_source.split("\n"):
        # Simple variable counting (not production-ready)
        words = line.split()
        for w in words:
            if w.isidentifier() and w not in ("import", "Base", "def", "main", "->", "U32", "Nat", "Bool"):
                var_usage[w] = var_usage.get(w, 0) + 1

    # Check for variables used more than once (potential affine violation)
    for var, count in var_usage.items():
        if count > 1 and "+" + var not in program_source:
            errors.append(f"Variable '{var}' used {count} times without '+': affine violation")

    # Basic validity
    valid = (
        has_def
        and has_main
        and len(errors) == 0
        and "recursion" not in program_source.lower()  # Prevent infinite recursion
    )

    return {
        "valid": valid,
        "errors": errors,
        "type_check": has_def and has_main,
        "affine_check": len([e for e in errors if "affine" in str(e)]) == 0,
        "termination_check": "recursion" not in program_source.lower(),
    }


def execute_strategy(
    program_source: str,
    market_data: str,
) -> Dict[str, Any]:
    """
    Execute a BendLite strategy and generate trace.

    Args:
        program_source: BendLite program source code
        market_data: Market data string

    Returns:
        Dict with execution results:
        - result: U32 computed value
        - trace: list of tokens executed
        - success: bool
        - compliance: bool (passed static rules)
    """
    # TODO: Integrate with actual BendVM execution
    # For now, return template execution result

    # Basic program validation
    has_main = "def main()" in program_source
    has_run = "run(" in program_source

    if not has_main or not has_run:
        return {
            "result": 0,
            "trace": [],
            "success": False,
            "compliance": False,
            "error": "Invalid program: missing 'def main()' or 'run()'",
        }

    # Simulate basic execution
    # In production, this would use the BendVM engine
    try:
        # Parse simple program to extract signal
        # This is a placeholder for actual BendVM execution
        result = 50  # Neutral/hold as default
        trace = ["INS(0)", "MA", "COMPARE", "OUT"]
        compliance = True  # Assume compliance for valid structure

        return {
            "result": result,
            "trace": trace,
            "success": True,
            "compliance": compliance,
        }
    except Exception as e:
        return {
            "result": 0,
            "trace": [],
            "success": False,
            "compliance": False,
            "error": str(e),
        }


def main() -> None:
    """Entry point para geração e verificação de estratégias."""
    import sys
    import json

    if len(sys.argv) < 2:
        print("Uso: qwenn-strategies <comando> [argumentos]")
        print()
        print("Comandos disponíveis:")
        print("  generate <type> [params]   - Generate a strategy program")
        print("  verify <program>           - Verify static rules compliance")
        print("  execute <program>          - Execute strategy and generate trace")
        print("  help                       - Show this help message")
        sys.exit(1)

    comando = sys.argv[1]

    if comando == "generate":
        # Parse arguments
        strategy_type = sys.argv[2] if len(sys.argv) > 2 else "ma_crossover"
        params_str = sys.argv[3] if len(sys.argv) > 3 else "{}"
        try:
            parameters = json.loads(params_str) if params_str else {}
        except json.JSONDecodeError:
            parameters = {}

        program = generate_strategy(
            strategy_type=strategy_type, parameters=parameters
        )
        print("=" * 60)
        print(f"Strategy Type: {strategy_type}")
        print("=" * 60)
        print(program)

    elif comando == "verify":
        # Read program from stdin or file
        if len(sys.argv) > 2:
            program_source = " ".join(sys.argv[2:])
        else:
            print("Lendo do stdin...")
            program_source = sys.stdin.read()

        result = verify_strategy(program_source)
        print("=" * 60)
        print("Verification Results")
        print("=" * 60)
        print(f"Valid: {result['valid']}")
        print(f"Type check: {result['type_check']}")
        print(f"Affine check: {result['affine_check']}")
        print(f"Termination check: {result['termination_check']}")
        if result["errors"]:
            print(f"Errors ({len(result['errors'])}):")
            for e in result["errors"]:
                print(f"  - {e}")

    elif comando == "execute":
        if len(sys.argv) > 2:
            program_source = " ".join(sys.argv[2:])
        else:
            print("Lendo do stdin...")
            program_source = sys.stdin.read()

        # Read market data from prompt or default
        market_data = sys.argv[3] if len(sys.argv) > 3 else "70,72,68,65,67,71,73,70,69,72"

        result = execute_strategy(program_source, market_data)
        print("=" * 60)
        print("Execution Results")
        print("=" * 60)
        print(f"Success: {result['success']}")
        print(f"Compliance: {result['compliance']}")
        print(f"Result (U32): {result['result']}")
        if result["trace"]:
            print(f"Trace tokens: {len(result['trace'])}")
            print(f"Trace: {result['trace']}")
        if result.get("error"):
            print(f"Error: {result['error']}")

    elif comando == "help":
        print("""
Qwenn-Strategies Commands:

  generate <type> [params]
    Generate a BendLite strategy program.
    Example: qwenn-strategies generate ma_crossover '{"period": 14}'
    Example: qwenn-strategies generate rsi '{"period": 14, "overbought": 70}'

  verify <program_source>
    Verify a BendLite program obeys static rules.
    Reads program from argument or stdin.

  execute <program_source> [market_data]
    Execute a BendLite strategy and generate trace.
    Market data is comma-separated prices.

  help
    Show this help message.
        """)

    else:
        print(f"Comando desconhecido: {comando}")
        print("Use 'qwenn-strategies help' para ver comandos disponíveis.")
        sys.exit(1)


if __name__ == "__main__":
    main()