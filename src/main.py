from src.reports import spending_by_category
from src.services import investment_bank, transactions
from src.views import main_page

if __name__ == "__main__":
    # Web services
    web_info = main_page("31.07.2020")
    print(web_info)

    # Services

    sum_invest_bank = investment_bank("2020-07", transactions.to_dict(orient="records"), 50)
    print(sum_invest_bank)

    # Reports
    spending_by_category_result = spending_by_category(transactions, "Супермаркеты", "31.07.2020")
    print(spending_by_category_result)
