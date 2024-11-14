from src.services import investment_bank


def test_investment_bank(transaction_investment_bank: list) -> None:
    result = investment_bank("2018-01", transaction_investment_bank, 50)
    assert result == 60.1
