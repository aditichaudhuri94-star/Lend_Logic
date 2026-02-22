def calculate_emi(principal, annual_rate, tenure_years):
    # Monthly interest rate
    monthly_rate = annual_rate / (12 * 100)
    # Total number of months
    months = tenure_years * 12

    # Standard EMI Formula: [P x R x (1+R)^N]/[(1+R)^N-1]
    emi = (principal * monthly_rate * (1 + monthly_rate)**months) / \
          ((1 + monthly_rate)**months - 1)

    total_payment = emi * months

    schedule = []
    balance = principal

    for month in range(1, months + 1):
        interest = balance * monthly_rate
        principal_paid = emi - interest
        balance -= principal_paid

        schedule.append({
            "month": month,
            "interest": round(interest, 2),
            "principal": round(principal_paid, 2),
            "balance": round(abs(balance), 2)
        })

    return round(emi, 2), round(total_payment, 2), schedule


def check_eligibility(emi, income):
    # Standard check: EMI should not exceed 40% of income
    if emi < income * 0.4:
        return "Eligible"
    return "Not Eligible"