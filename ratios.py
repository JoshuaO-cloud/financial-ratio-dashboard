import yfinance as yf

def get_current_ratio(balance_sheet):
    try:
        current_assets = balance_sheet.loc["Current Assets"].iloc[0]
        current_liabilities = balance_sheet.loc["Current Liabilities"].iloc[0]
        return float(current_assets / current_liabilities)
    except (KeyError, IndexError, ZeroDivisionError):
        return None


def get_debt_to_equity(balance_sheet):
    try:
        total_liabilities = balance_sheet.loc["Total Liabilities Net Minority Interest"].iloc[0]
        equity = balance_sheet.loc["Stockholders Equity"].iloc[0]
        return float(total_liabilities / equity)
    except (KeyError, IndexError, ZeroDivisionError):
        return None


def get_net_margin (income_statement):
    try:
        net_income = income_statement.loc["Net Income"].iloc[0]
        revenue = income_statement.loc["Total Revenue"].iloc[0]
        return float(net_income / revenue)
    except (KeyError, IndexError, ZeroDivisionError):
        return None



def get_ratios(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    balance_sheet = ticker.balance_sheet
    income_statement = ticker.financials

    return {
        "current_ratio": get_current_ratio(balance_sheet),
        "debt_to_equity_yf": get_debt_to_equity(balance_sheet),
        "net_margin_yf": get_net_margin(income_statement)
    }

from edgar import Company, set_identity
set_identity("Oluwaferanmi Owoodusi doony1738@gmail.com")


def get_annual_value(facts, concept_names, label=None):
    for concept_name in concept_names:
        try:
            data = facts.query().by_concept(concept_name).to_dataframe()
            annual_data = data[data["fiscal_period"].isin(["FY", "Q4"])]
            if label:
                annual_data = annual_data[annual_data["label"] == label]
            annual_data = annual_data.sort_values("period_end", ascending=False)
            value = annual_data["numeric_value"].iloc[0]
            return float(value)
        except (KeyError, IndexError):
            continue
    return None


def get_edgar_ratios(ticker_symbol):
    company = Company(ticker_symbol)
    facts = company.get_facts()

    total_assets = get_annual_value(facts, ["Assets"], label="Assets")
    total_liabilities = get_annual_value(facts, ["Liabilities"], label="Liabilities")
    equity = get_annual_value(facts, ["StockholdersEquity"], label="Stockholders' Equity Attributable to Parent")
    net_income = get_annual_value(facts, ["NetIncomeLoss"], label="Net Income (Loss) Attributable to Parent")
    revenue = get_annual_value(
        facts,
        ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
        label="Revenue from Contract with Customer, Excluding Assessed Tax"
    )

    try:
        debt_to_equity = total_liabilities / equity
    except (TypeError, ZeroDivisionError):
        debt_to_equity = None

    try:
        net_margin = net_income / revenue
    except (TypeError, ZeroDivisionError):
        net_margin = None

    try:
        roe = net_income / equity
    except (TypeError, ZeroDivisionError):
        roe = None

    return {
        "debt_to_equity_edgar": debt_to_equity,
        "net_margin_edgar": net_margin,
        "roe_edgar": roe,
    }

def get_all_ratios(ticker_symbol):
    yfinance_ratios = get_ratios(ticker_symbol)

    company = Company(ticker_symbol)
    facts = company.get_facts()
    edgar_ratios = get_edgar_ratios(ticker_symbol)

    combined = {**yfinance_ratios, **edgar_ratios}
    return combined

print(get_all_ratios("MSFT"))
