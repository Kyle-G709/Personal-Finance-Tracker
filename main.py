
#step 1, getting income
def getMonthlyIncome():
    return float(input("Monthly income:"))
    
def getYearlyIncome(monthly_income = 0.0):
    return monthly_income * 12

def displayIncome(monthly_income, yearly_income):
    print(f"Monthly Income: ${monthly_income:.2f}\nYearly Income: ${yearly_income:.2f}")

#step 2, expenses
def getFood():
    return float(input("How much spent on food per month: "))
    
def getTransportation():
    return float(input("How much spent on transportation per month: "))

def getEntertainment():
    return float(input("How much spent on entertainment: "))

def totalMonthlyExpenses(food, trans, entertain):
    return round(food + trans + entertain, 2)

def displayExpenses(expenses):
    print(f"Monthly expenses: ${expenses:.2f}")

#step 3, savings
def money_after_expenses_monthly(income, expenses):
    return income - expenses

def percent_of_income_spent(money_spent, total_income):
    return round((money_spent/total_income) * 100, 2)

def percent_of_income_saved(money_saved, total_income):
    return round((money_saved/total_income)*100, 2)

def financial_summary(money_after_expenses, per_spent, per_saved, total_expenses, income):
    print(f"Income:${income:.2f}\nExpenses:${total_expenses:.2f}\nAmount After Expenses:${money_after_expenses:.2f}\nPercent Spent:{per_spent}%\nPercent Saved:{per_saved}%")

def main():
    #income
    monthlyInc = getMonthlyIncome()
    yearlyInc = getYearlyIncome(monthlyInc)
    displayIncome(monthlyInc, yearlyInc)

    #expenses
    food = getFood()
    trans = getTransportation()
    ent = getEntertainment()
    total_expenses = totalMonthlyExpenses(food, trans, ent)
    displayExpenses(total_expenses)

    #Savings

    



if __name__ == "__main__":
    main()