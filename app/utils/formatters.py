def format_large_number(num):
    """
    Formats large numbers into human-readable strings with T, B, M suffixes.
    """
    if num is None or not isinstance(num, (int, float)):
        return "N/A"
    
    abs_num = abs(num)
    if abs_num >= 1e12:
        return f"{num / 1e12:.2f}T"
    elif abs_num >= 1e9:
        return f"{num / 1e9:.2f}B"
    elif abs_num >= 1e6:
        return f"{num / 1e6:.2f}M"
    else:
        return f"{num:,.2f}"
