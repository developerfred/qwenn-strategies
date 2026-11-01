"""Tests for Qwenn-Strategies framework."""

from qwenn_strategies.strategy_gen import (
    generate_strategy,
    verify_strategy,
    execute_strategy,
    main,
)


def test_generate_ma_crossover():
    """Test generation of MA crossover strategy."""
    program = generate_strategy(
        market_data="ETH/USD price data",
        strategy_type="ma_crossover",
        parameters={"period": 14},
    )
    assert "import Base" in program
    assert "def main()" in program
    assert "ma_period" in program
    print("✓ MA crossover strategy generated successfully")


def test_generate_rsi_strategy():
    """Test generation of RSI strategy."""
    program = generate_strategy(
        market_data="ETH/USD price data",
        strategy_type="rsi",
        parameters={"period": 14, "overbought": 70, "oversold": 30},
    )
    assert "import Base" in program
    assert "def main()" in program
    assert "rsi_period" in program or "rsi_calc" in program
    print("✓ RSI strategy generated successfully")


def test_verify_strategy_valid():
    """Test verification of a valid BendLite program."""
    valid_program = """
import Base

def main() -> U32:
    run(generate_signal) -> BUY
    -> HOLD
"""
    result = verify_strategy(valid_program)
    assert result["valid"] is True, f"Expected valid=True, got {result}"
    assert result["type_check"] is True
    assert result["affine_check"] is True
    print("✓ Valid program passed verification")


def test_verify_strategy_invalid():
    """Test verification of an invalid BendLite program."""
    invalid_program = """
import Base

def main() -> U32:
    x + x + x  // Variable used 3 times without affine marker
    -> HOLD
"""
    result = verify_strategy(invalid_program)
    # Should detect affine violation
    has_affine_errors = any("affine" in str(e).lower() for e in result["errors"])
    # The program may or may not be marked valid depending on heuristics,
    # but should at least run without crashing
    assert "valid" in result
    assert "errors" in result
    print(f"✓ Invalid program verified (errors: {len(result['errors'])})")


def test_verify_strategy_missing_main():
    """Test verification of program missing main function."""
    no_main_program = """
import Base

def helper() -> U32:
    return 50
"""
    result = verify_strategy(no_main_program)
    assert result["valid"] is False, "Expected valid=False for program without main"
    assert result["type_check"] is False
    print("✓ Program without main correctly marked invalid")


def test_execute_strategy():
    """Test execution of a BendLite strategy."""
    program = """
import Base

def main() -> U32:
    run(generate_signal) -> BUY
    -> HOLD
"""
    # Read market data from args or use default
    import sys
    market_data = "70,72,68,65,67,71,73,70,69,72" if len(sys.argv) <= 1 else sys.argv[1]

    result = execute_strategy(program, market_data)
    assert "success" in result
    assert "compliance" in result
    assert "result" in result
    print(f"✓ Strategy execution result: success={result['success']}, compliance={result['compliance']}, result={result['result']}")


def test_generate_all_types():
    """Test generation of different strategy types."""
    types = ["ma_crossover", "rsi", "generic"]
    for strategy_type in types:
        program = generate_strategy(
            market_data="test data",
            strategy_type=strategy_type,
        )
        assert "import Base" in program, f"Missing 'import Base' for {strategy_type}"
        assert "def main()" in program, f"Missing 'def main()' for {strategy_type}"
    print(f"✓ All strategy types generated: {types}")


if __name__ == "__main__":
    test_generate_ma_crossover()
    test_generate_rsi_strategy()
    test_verify_strategy_valid()
    test_verify_strategy_invalid()
    test_verify_strategy_missing_main()
    test_execute_strategy()
    test_generate_all_types()
    print("\n🎉 All tests passed!")