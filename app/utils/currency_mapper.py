def get_currency_symbol(currency_code):
    """
    Maps currency codes to their respective symbols.
    """
    mapping = {
        "USD": "$",
        "INR": "₹",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "CAD": "C$",
        "AUD": "A$",
        "CHF": "Fr",
        "HKD": "HK$",
        "NZD": "NZ$",
        "KRW": "₩",
        "SGD": "S$",
        "CNY": "¥",
        "TWD": "NT$",
        "BRL": "R$",
        "MXN": "Mex$",
        "RUB": "₽",
        "ZAR": "R",
        "TRY": "₺",
    }
    return mapping.get(currency_code.upper(), f"{currency_code} ")
