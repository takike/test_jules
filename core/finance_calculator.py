from typing import Union

def calculate_max_affordable_loan(
    annual_income: float,
    annual_other_debt_payments: float,
    mortgage_interest_rate_annual: float,
    loan_term_years: int,
    down_payment_percentage: float,
    estimated_annual_property_tax_and_insurance: float
) -> float:
    """
    Calculates the maximum affordable mortgage loan principal.

    This calculation is based on a simplified model using a front-end
    Debt-to-Income (DTI) ratio for housing-related payments (PITI: Principal,
    Interest, Taxes, Insurance). It does not consider the overall DTI ratio
    which would include `annual_other_debt_payments`.

    Args:
        annual_income (float): The borrower's gross annual income.
        annual_other_debt_payments (float): The borrower's total annual payments for
            other debts (e.g., car loans, student loans).
            Note: This parameter is included for future enhancements (e.g., full DTI
            calculation) but is not used in the current PITI-based loan amount logic.
        mortgage_interest_rate_annual (float): The annual mortgage interest rate
            (e.g., 0.065 for 6.5%).
        loan_term_years (int): The term of the loan in years (e.g., 30).
        down_payment_percentage (float): The percentage of the home price the
            borrower plans to pay as a down payment (e.g., 20 for 20%).
            Note: This function calculates and returns the maximum loan principal,
            not the affordable house price. The down payment is relevant for the
            latter but not directly for the loan amount output here.
        estimated_annual_property_tax_and_insurance (float): Estimated total annual
            cost for property taxes and homeowner's insurance (T&I).

    Returns:
        float: The maximum affordable loan principal, rounded to two decimal places.
               Returns 0.0 if the calculated maximum monthly Principal & Interest (P&I)
               payment is not positive (e.g., if T&I exceeds the affordable PITI).

    Key Assumptions:
        - A front-end DTI ratio of 28% for housing costs (PITI) is used.
        - The function calculates the loan principal, not the affordable home price.
        - `annual_other_debt_payments` is not used in this specific calculation but is
          retained for potential future use with total DTI.
    """

    """

    # Step 1: Calculate Gross Monthly Income (GMI)
    gross_monthly_income: float = annual_income / 12

    # Step 2: Calculate maximum monthly housing payment (PITI) allowed.
    # This is based on a common front-end DTI ratio (e.g., 28%) for housing costs.
    # PITI = Principal, Interest, Taxes, Insurance.
    MAX_HOUSING_DTI_RATIO = 0.28 
    max_monthly_piti: float = gross_monthly_income * MAX_HOUSING_DTI_RATIO

    # Step 3: Calculate monthly property taxes and insurance (T&I)
    monthly_ti: float = estimated_annual_property_tax_and_insurance / 12

    # Step 4: Calculate the maximum monthly principal and interest (P&I) payment affordable.
    # This is the portion of PITI that can be allocated to the loan's principal and interest.
    max_monthly_pi: float = max_monthly_piti - monthly_ti
    
    # If affordable P&I is zero or negative (e.g., T&I consumes all or more than allowed PITI),
    # then no loan principal can be afforded.
    if max_monthly_pi <= 0:
        return 0.0

    # Step 5: Convert the annual mortgage interest rate to a monthly rate.
    # Assumes the input `mortgage_interest_rate_annual` is in decimal form (e.g., 0.05 for 5%).
    monthly_interest_rate: float = mortgage_interest_rate_annual / 12

    # Step 6: Calculate the total number of payments over the loan term.
    num_payments: int = loan_term_years * 12

    # Step 7: Use the loan payment formula to calculate the maximum loan principal (M).
    # The formula for the present value of an ordinary annuity is:
    # M = P * [ (1 - (1 + r)^-n) / r ]
    # or equivalently, M = P * [ ((1 + r)^n - 1) / (r * (1 + r)^n) ]
    # where:
    #   M = Mortgage Principal (the value we are solving for)
    #   P = Monthly Principal and Interest payment (max_monthly_pi)
    #   r = Monthly interest rate (monthly_interest_rate)
    #   n = Total number of payments (num_payments)
    max_loan_principal: float
    
    if num_payments == 0: # If loan term is 0 years, no loan can be taken.
        max_loan_principal = 0.0
    elif monthly_interest_rate == 0:
        # Special case: If interest rate is 0, the loan principal is simply P * n.
        max_loan_principal = max_monthly_pi * num_payments
    else:
        try:
            # Standard formula calculation
            # (1 + r)^n
            factor = (1 + monthly_interest_rate) ** num_payments
            # Numerator: P * [ (1 + r)^n - 1 ]
            numerator = max_monthly_pi * (factor - 1)
            # Denominator: r * (1 + r)^n
            denominator = monthly_interest_rate * factor
            
            # Avoid division by zero if denominator is zero (though unlikely with r > 0 and n > 0)
            if denominator == 0: 
                max_loan_principal = 0.0
            else:
                max_loan_principal = numerator / denominator
        except OverflowError:
            # This can occur if num_payments is excessively large, causing 'factor' to become extremely large.
            # For typical loan terms (e.g., up to 50 years), this is highly unlikely.
            # If it does happen, it implies a scenario where the loan is essentially interest-only in perpetuity.
            # The maximum loan would be what can be sustained by the monthly P&I payment
            # as if it were an interest-only payment (Present Value of a perpetuity = P / r).
            max_loan_principal = max_monthly_pi / monthly_interest_rate # monthly_interest_rate > 0 here

    # Step 8: Return the calculated loan principal, rounded.
    # Note: The function returns the max_loan_principal.
    # If the goal was to calculate the affordable house price, the formula would be:
    # affordable_house_price = max_loan_principal / (1 - (down_payment_percentage / 100.0))
    # This is outside the current scope of this function's return value.

    return round(max_loan_principal, 2)

# Placeholder comment for future enhancements, such as a more comprehensive DTI calculation.
# def check_total_dti_compliance(annual_income: float, annual_housing_payment_piti: float, 
#                                annual_other_debt_payments: float, max_total_dti_ratio: float = 0.43) -> bool:
#     """Checks if total debts (housing + other) are within a specified total DTI ratio."""
#     total_monthly_debt = (annual_housing_payment_piti / 12) + (annual_other_debt_payments / 12)
#     gross_monthly_income = annual_income / 12
#     if gross_monthly_income == 0:
#         return False # Avoid division by zero; cannot meet DTI with no income.
#     current_total_dti = total_monthly_debt / gross_monthly_income
#     return current_total_dti <= max_total_dti_ratio


def calculate_future_education_cost(
    current_age_child1: int,
    current_age_child2: int,
    years_of_college_child1: int,
    years_of_college_child2: int,
    current_annual_cost_per_child: float,
    annual_inflation_rate_education: float,
    investment_return_rate: float,
    college_start_age: int = 18
) -> dict[str, float]:
    """
    Projects future college costs for two children and related savings needs.

    Calculates the total inflated future cost of college, the lump sum amount
    that would need to be invested today to cover these costs, and the
    annual savings required until the first child starts college.

    Args:
        current_age_child1 (int): Current age of the first child.
        current_age_child2 (int): Current age of the second child. (Set to 0 or negative
            if only one child or if this child should not be considered).
        years_of_college_child1 (int): Number of years child 1 will attend college.
        years_of_college_child2 (int): Number of years child 2 will attend college.
        current_annual_cost_per_child (float): Current annual cost of college for one
            child, in today's dollars.
        annual_inflation_rate_education (float): Expected annual inflation rate for
            education costs (e.g., 0.05 for 5%).
        investment_return_rate (float): Expected average annual rate of return on
            investments (e.g., 0.07 for 7%). This is used for discounting future
            costs to present value and for calculating annuity payments.
        college_start_age (int, optional): Typical age children start college.
            Defaults to 18.

    Returns:
        dict[str, float]: A dictionary containing:
            - 'total_future_inflated_cost' (float): Sum of all projected inflated
              annual college costs for both children.
            - 'lump_sum_needed_today' (float): Total present value of all future
              inflated college costs, discounted by `investment_return_rate`.
            - 'annual_savings_needed' (float): The annual amount that needs to be
              saved, assuming it's invested at `investment_return_rate`, until the
              first child starts college. Returns `float('inf')` if there's no time
              to save (e.g., college starts now or in the past) or if the
              investment return rate makes the standard annuity formula problematic
              (e.g. rate <= 0 when interest is expected for the formula).

    Key Assumptions:
        - College costs are incurred at the beginning of each college year.
        - Inflation is applied to the current annual cost for each year until payment.
        - Investment returns are compounded annually.
        - If a child's `current_age` implies they are already past `college_start_age`
          for some or all of their `years_of_college`, only the remaining future
          costs are calculated. If all college years are in the past for a child,
          their cost contribution is zero.
        - Annual savings are made at the end of each year.
    """
    """
    results: dict[str, float] = {
        'total_future_inflated_cost': 0.0,
        'lump_sum_needed_today': 0.0,
        'annual_savings_needed': 0.0
    }

    # Consolidate data for iteration
    children_data = [
        {'current_age': current_age_child1, 'years_of_college': years_of_college_child1},
        {'current_age': current_age_child2, 'years_of_college': years_of_college_child2}
    ]

    min_years_to_college_for_saving = float('inf') # Used to determine the savings period

    # Loop through each child to calculate their individual costs
    for child_idx, child in enumerate(children_data):
        # Skip if child's age is non-positive and it's the second entry (child2),
        # or if years_of_college is zero for this child.
        if child_idx == 1 and child['current_age'] <= 0: # A way to signify "no second child"
            continue
        if child['years_of_college'] <= 0:
            continue

        total_inflated_cost_for_child = 0.0
        lump_sum_for_child = 0.0

        # Years from today until the child starts college
        years_to_college = college_start_age - child['current_age']
        
        # If child is already past college_start_age, years_to_college will be negative.
        # Example: Child is 19, college_start_age is 18 -> years_to_college = -1.
        # This means their first year of college (attendance year 0) would have been 1 year ago.
        
        # Only proceed if there are college years and they are not entirely in the past.
        # years_to_college >= -child['years_of_college'] ensures that at least some part of college is in the future or current year.
        # E.g., if child is 22, 4 years college, start 18 -> years_to_college = -4.
        # -4 >= -4 is true. First year of expense = -4 + 0 = -4 (past). Last year = -4 + 3 = -1 (past). All past.
        # E.g., if child is 21, 4 years college, start 18 -> years_to_college = -3.
        # -3 >= -4 is true. First year of expense = -3 + 0 = -3 (past). Last year = -3 + 3 = 0 (current). One year is current.
        if years_to_college >= -child['years_of_college']:
            
            # Determine the minimum years to the start of college for any child;
            # this defines the period over which savings can be made.
            if years_to_college > 0: # Only positive years_to_college contribute to savings period length
                 min_years_to_college_for_saving = min(min_years_to_college_for_saving, years_to_college)
            elif years_to_college <= 0 and min_years_to_college_for_saving == float('inf'):
                 # If this child is starting college now/soon (or already started) and is the first one considered
                 # for min_years_to_college_for_saving, set it to 0. If other child is younger, this will be updated.
                 min_years_to_college_for_saving = 0

            # Calculate costs for each year of college attendance
            for year_of_college_attendance in range(child['years_of_college']):
                # year_of_expense is the number of years from today when this specific college year's cost is incurred.
                # E.g., if years_to_college = 0, first year_of_expense is 0 (current year).
                # E.g., if years_to_college = 1, first year_of_expense is 1 (next year).
                # E.g., if years_to_college = -1 (child is 19, start 18), first year_of_attendance (index 0)
                #       would have been year_of_expense = -1. Second year_of_attendance (index 1) is year_of_expense = 0.
                year_of_expense = years_to_college + year_of_college_attendance

                if year_of_expense < 0: # This specific year of college cost was in the past.
                    continue

                # Inflate the current annual cost to the year of expense.
                inflated_cost_for_year = current_annual_cost_per_child * \
                                         ((1 + annual_inflation_rate_education) ** year_of_expense)
                total_inflated_cost_for_child += inflated_cost_for_year

                # Calculate the Present Value (PV) of this single year's future inflated cost.
                # Discount it back to today (year 0) using the investment return rate.
                if (1 + investment_return_rate) == 0: # Handles -100% return rate
                    pv_of_that_year_cost = float('inf') if year_of_expense > 0 else inflated_cost_for_year
                else:
                    pv_of_that_year_cost = inflated_cost_for_year / \
                                       ((1 + investment_return_rate) ** year_of_expense)
                lump_sum_for_child += pv_of_that_year_cost
        
        results['total_future_inflated_cost'] += total_inflated_cost_for_child
        results['lump_sum_needed_today'] += lump_sum_for_child

    # If min_years_to_college_for_saving remained float('inf'), it means no future college years
    # for any child, or all children start college now/in the past (or have 0 years of college).
    # In such cases, the savings period is effectively 0.
    if min_years_to_college_for_saving == float('inf'):
        min_years_to_college_for_saving = 0

    # Calculate annual_savings_needed using the Present Value of an ordinary annuity formula.
    # PMT = PV * [ r / (1 - (1 + r)^-n) ]
    # where PV = results['lump_sum_needed_today'], r = investment_return_rate, n = min_years_to_college_for_saving
    pv_total = results['lump_sum_needed_today']
    n_savings_periods = min_years_to_college_for_saving # This is 'n'
    r_investment = investment_return_rate            # This is 'r'

    if pv_total == 0: # If no future cost, no savings needed.
        results['annual_savings_needed'] = 0.0
    elif n_savings_periods <= 0:
        # If college starts now or in the past, no time for gradual annual savings.
        # The full lump sum would be needed immediately.
        results['annual_savings_needed'] = float('inf')
    elif r_investment == 0: # Special case for 0% investment return
        if n_savings_periods > 0: # Avoid division by zero if somehow n=0 here
             results['annual_savings_needed'] = pv_total / n_savings_periods
        else: # Should be caught by n_savings_periods <= 0
             results['annual_savings_needed'] = float('inf')
    else: # Standard case with r_investment > 0 (or < 0 but not problematic for formula)
        try:
            # (1 + r)^-n
            compound_factor_inv = (1 + r_investment) ** -n_savings_periods
            # Denominator: 1 - (1 + r)^-n
            denominator_annuity = 1 - compound_factor_inv
            
            if denominator_annuity == 0:
                # This can happen if (1+r)^-n = 1, e.g. if r=0 (already handled) or n=0 (already handled).
                # Or if r is such that it leads to issues, though unlikely with typical financial rates.
                results['annual_savings_needed'] = float('inf')
            else:
                # Numerator: PV * r
                numerator_annuity = pv_total * r_investment
                results['annual_savings_needed'] = numerator_annuity / denominator_annuity
        except OverflowError:
            # Highly unlikely with typical financial values for (1+r)^-n.
            results['annual_savings_needed'] = float('inf')

    # Round final results
    results['total_future_inflated_cost'] = round(results['total_future_inflated_cost'], 2)
    results['lump_sum_needed_today'] = round(results['lump_sum_needed_today'], 2)
    if results['annual_savings_needed'] != float('inf'):
        results['annual_savings_needed'] = round(results['annual_savings_needed'], 2)

    return results


def project_income(
    current_annual_income_user1: float,
    current_annual_income_user2: float,
    annual_growth_rate_user1: float,
    annual_growth_rate_user2: float,
    projection_years: int
) -> list[dict[str, float]]:
    """
    Projects the combined annual income of two users over several years.

    Args:
        current_annual_income_user1 (float): Current annual income of the first user.
        current_annual_income_user2 (float): Current annual income of the second user.
            (Set to 0 if only one user).
        annual_growth_rate_user1 (float): Expected average annual income growth rate
            for user 1 (e.g., 0.03 for 3%).
        annual_growth_rate_user2 (float): Expected average annual income growth rate
            for user 2 (e.g., 0.03 for 3%). (Set to 0 if only one user or no growth
            for user 2).
        projection_years (int): The number of years into the future to project income.
            Income for year 'y' is the income anticipated at the end of that year.

    Returns:
        list[dict[str, float]]: A list of dictionaries. Each dictionary represents
        a future year and contains:
            - 'year' (float): The projection year number (e.g., 1.0 for end of year 1).
            - 'user1_income' (float): Projected income for user 1 for that year, rounded.
            - 'user2_income' (float): Projected income for user 2 for that year, rounded.
            - 'combined_income' (float): Combined projected income for that year, rounded.
        Returns an empty list if `projection_years` is 0 or negative.

    Key Assumptions:
        - Income growth is compounded annually at the specified rates.
        - Income for a given year is the value at the end of that year.
    """
    """
    projected_incomes_by_year: list[dict[str, float]] = []

    if projection_years <= 0:
        return projected_incomes_by_year # Return empty list if no years to project

    # Iterate for each year in the projection period
    for year_num in range(1, projection_years + 1):
        # Calculate future income for user 1: Current * (1 + growth_rate)^year
        income_user1_future = current_annual_income_user1 * ((1 + annual_growth_rate_user1) ** year_num)
        # Calculate future income for user 2
        income_user2_future = current_annual_income_user2 * ((1 + annual_growth_rate_user2) ** year_num)
        # Combine incomes for the year
        combined_income_for_year = income_user1_future + income_user2_future

        projected_incomes_by_year.append({
            'year': float(year_num), # Year number (as float for consistency with other monetary values)
            'user1_income': round(income_user1_future, 2),
            'user2_income': round(income_user2_future, 2),
            'combined_income': round(combined_income_for_year, 2)
        })

    return projected_incomes_by_year


def project_cost_of_living(
    current_annual_col: float,
    annual_col_inflation_rate: float,
    child_related_annual_expense_increase_per_child: float,
    ages_of_children: list[int],
    child_expense_start_age: int,
    child_expense_end_age: int,
    projection_years: int
) -> list[dict[str, float]]:
    """
    Projects annual cost of living (CoL), including child-related expenses.

    This function inflates a base CoL and adds specific, inflated child-related
    expenses for children within a defined age range over a projection period.

    Args:
        current_annual_col (float): Current total annual cost of living, excluding
            major education savings and housing mortgage payments which are typically
            handled separately.
        annual_col_inflation_rate (float): General annual inflation rate for CoL
            (e.g., 0.02 for 2%). This applies to both base CoL and the
            child-related expense amount.
        child_related_annual_expense_increase_per_child (float): Additional annual
            expense (in today's dollars) that applies per child when they are
            within the `child_expense_start_age` and `child_expense_end_age`.
            This amount will be inflated to the future year it applies.
        ages_of_children (list[int]): A list containing the current ages of the children.
            An empty list signifies no children to consider for additional expenses.
        child_expense_start_age (int): The age at which the additional child-related
            expense starts applying for each child.
        child_expense_end_age (int): The age at which the additional child-related
            expense stops applying. The expense applies if `start_age <= child_age < end_age`.
            So, if `end_age` is 18, expense applies up to age 17.
        projection_years (int): The number of years into the future to project CoL.
            Year 'y' represents the CoL at the end of that year.

    Returns:
        list[dict[str, float]]: A list of dictionaries. Each dictionary represents
        a future year and contains:
            - 'year' (float): The projection year number (e.g., 1.0 for end of year 1).
            - 'base_cost_of_living' (float): The general CoL inflated for that year.
            - 'additional_child_expenses' (float): Total inflated additional expenses
              for all children eligible in that year.
            - 'total_cost_of_living' (float): Sum of base CoL and additional child
              expenses for that year.
        Returns an empty list if `projection_years` is 0 or negative.

    Key Assumptions:
        - CoL inflation is compounded annually.
        - The `child_related_annual_expense_increase_per_child` is an amount in
          today's dollars and is inflated using `annual_col_inflation_rate` to the
          year the expense is incurred.
        - Child expenses apply if a child's age in a given future year is
          `>= child_expense_start_age` and `< child_expense_end_age`.
    """
    """
    projected_col_by_year: list[dict[str, float]] = []

    if projection_years <= 0:
        return projected_col_by_year

    num_children = len(ages_of_children)

    # Iterate for each year in the projection period
    for year_num in range(1, projection_years + 1):
        # Inflate the base cost of living for the current projection year
        base_inflated_col = current_annual_col * ((1 + annual_col_inflation_rate) ** year_num)

        # Calculate total additional child expenses for this specific year
        total_additional_child_expense_for_year = 0.0
        if child_related_annual_expense_increase_per_child > 0 and num_children > 0:
            for child_idx in range(num_children):
                current_child_age = ages_of_children[child_idx]
                # Calculate the child's age in the projection year
                child_age_in_year_x = current_child_age + year_num

                # Check if the child is within the age range for incurring additional expenses
                if child_expense_start_age <= child_age_in_year_x < child_expense_end_age:
                    # Inflate the per-child additional expense to its value in the projection year
                    single_child_additional_expense_inflated = \
                        child_related_annual_expense_increase_per_child * \
                        ((1 + annual_col_inflation_rate) ** year_num)
                    
                    total_additional_child_expense_for_year += single_child_additional_expense_inflated
        
        # Sum base CoL and child expenses for the total CoL for the year
        total_col_for_year = base_inflated_col + total_additional_child_expense_for_year

        projected_col_by_year.append({
            'year': float(year_num),
            'base_cost_of_living': round(base_inflated_col, 2),
            'additional_child_expenses': round(total_additional_child_expense_for_year, 2),
            'total_cost_of_living': round(total_col_for_year, 2)
        })

    return projected_col_by_year


def generate_financial_summary(
    # Income parameters (passed directly to project_income)
    current_annual_income_user1: float, current_annual_income_user2: float,
    annual_growth_rate_user1: float, annual_growth_rate_user2: float,
    # Cost of Living parameters (passed directly to project_cost_of_living)
    current_annual_col: float, annual_col_inflation_rate: float,
    child_related_annual_expense_increase_per_child: float, ages_of_children: list[int],
    child_expense_start_age: int, child_expense_end_age: int,
    # Fixed annual expenses (assumed constant for the summary period)
    annual_education_savings_needed: float,
    annual_mortgage_payment: float,
    # General projection parameter
    projection_years: int
) -> list[dict[str, float]]:
    """
    Generates a year-by-year financial summary, projecting income, expenses, and net savings.

    This function integrates projections from `project_income` and
    `project_cost_of_living`, and incorporates fixed annual expenses for
    education savings and mortgage payments to provide a comprehensive overview.

    Args:
        current_annual_income_user1 (float): Current annual income of user 1.
        current_annual_income_user2 (float): Current annual income of user 2.
        annual_growth_rate_user1 (float): Income growth rate for user 1.
        annual_growth_rate_user2 (float): Income growth rate for user 2.
        current_annual_col (float): Current base annual cost of living.
        annual_col_inflation_rate (float): Inflation rate for CoL and child expenses.
        child_related_annual_expense_increase_per_child (float): Additional CoL per child
            (in today's dollars) within the specified age range.
        ages_of_children (list[int]): Current ages of children for CoL calculation.
        child_expense_start_age (int): Start age for additional child CoL.
        child_expense_end_age (int): End age (exclusive) for additional child CoL.
        annual_education_savings_needed (float): The annual amount allocated for
            education savings. This is treated as a constant annual expense.
        annual_mortgage_payment (float): The total annual mortgage payment (PITI).
            This is treated as a constant annual expense.
        projection_years (int): The number of years to project the financial summary.

    Returns:
        list[dict[str, float]]: A list of dictionaries, each representing a year in the
        projection. Each dictionary contains:
            - 'year' (float): The projection year.
            - 'projected_combined_income' (float): Total projected income for the year.
            - 'projected_cost_of_living' (float): Total projected CoL for the year.
            - 'projected_education_savings' (float): Annual education savings amount.
            - 'projected_housing_payment' (float): Annual housing payment amount.
            - 'projected_total_expenses' (float): Sum of CoL, education, and housing.
            - 'projected_net_savings' (float): Income minus total expenses.
        Returns an empty list if `projection_years` is 0 or negative.

    Key Assumptions:
        - `annual_education_savings_needed` and `annual_mortgage_payment` are
          constant annual amounts throughout the projection period.
        - Projections for income and CoL are based on the logic and assumptions
          within `project_income` and `project_cost_of_living` respectively.
    """
    """
    if projection_years <= 0:
        return [] # Return empty list for non-positive projection years

    # Step 1: Get projected income data
    projected_incomes_list = project_income(
        current_annual_income_user1=current_annual_income_user1,
        current_annual_income_user2=current_annual_income_user2,
        annual_growth_rate_user1=annual_growth_rate_user1,
        annual_growth_rate_user2=annual_growth_rate_user2,
        projection_years=projection_years
    )

    # Step 2: Get projected cost of living data
    projected_col_list = project_cost_of_living(
        current_annual_col=current_annual_col,
        annual_col_inflation_rate=annual_col_inflation_rate,
        child_related_annual_expense_increase_per_child=child_related_annual_expense_increase_per_child,
        ages_of_children=ages_of_children,
        child_expense_start_age=child_expense_start_age,
        child_expense_end_age=child_expense_end_age,
        projection_years=projection_years
    )

    financial_summary_by_year: list[dict[str, float]] = []

    # Step 3: Combine income, CoL, and fixed expenses for each year
    # The helper functions `project_income` and `project_cost_of_living` return lists
    # where index `i` corresponds to year `i+1`.
    for year_idx in range(projection_years):
        year_num = year_idx + 1 # Actual year number (1-based)

        # Safety check: ensure data exists for the current index.
        # This should always pass if helper functions work correctly and `projection_years` is consistent.
        if year_idx >= len(projected_incomes_list) or year_idx >= len(projected_col_list):
            # Log an error or warning if this unexpected situation occurs.
            # For now, skip this year's summary if data is missing.
            # print(f"Warning: Missing income or CoL data for year index {year_idx}. Skipping summary for this year.")
            continue 

        income_data_for_year = projected_incomes_list[year_idx]
        col_data_for_year = projected_col_list[year_idx]

        # Extract relevant figures for the current year
        combined_income = income_data_for_year['combined_income']
        total_cost_of_living = col_data_for_year['total_cost_of_living']

        # Fixed annual expenses (assumed constant for simplicity in this summary model)
        # These are passed as arguments and not inflated within this function.
        fixed_education_savings = annual_education_savings_needed
        fixed_housing_payment = annual_mortgage_payment

        # Calculate total expenses and net savings for the year
        total_expenses_for_year = total_cost_of_living + fixed_education_savings + fixed_housing_payment
        net_savings_for_year = combined_income - total_expenses_for_year

        financial_summary_by_year.append({
            'year': float(year_num),
            'projected_combined_income': round(combined_income, 2),
            'projected_cost_of_living': round(total_cost_of_living, 2),
            'projected_education_savings': round(fixed_education_savings, 2), # Already an annual figure
            'projected_housing_payment': round(fixed_housing_payment, 2),     # Already an annual figure
            'projected_total_expenses': round(total_expenses_for_year, 2),
            'projected_net_savings': round(net_savings_for_year, 2)
        })

    return financial_summary_by_year
