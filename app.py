from typing import Callable, Dict, Any, List # Enhanced type hinting
# Import all calculation functions from the core module
from core.finance_calculator import (
    calculate_max_affordable_loan,
    calculate_future_education_cost,
    project_income,
    project_cost_of_living,
    generate_financial_summary
)

# Helper function to get float input
def get_float_input(prompt: str, default: float = None) -> float:
    """
    Prompts the user for a float input and handles potential errors.

    Args:
        prompt (str): The message displayed to the user.
        default (float, optional): The default value to return if the user
                                   enters nothing. Defaults to None.

    Returns:
        float: The float value entered by the user or the default.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and default is not None:
                print(f"(Using default: {default})")
                return default
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number (e.g., 123.45 or 100).")

# Helper function to get integer input
def get_int_input(prompt: str, default: int = None) -> int:
    """
    Prompts the user for an integer input and handles potential errors.

    Args:
        prompt (str): The message displayed to the user.
        default (int, optional): The default value to return if the user
                                 enters nothing. Defaults to None.

    Returns:
        int: The integer value entered by the user or the default.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and default is not None:
                print(f"(Using default: {default})")
                return default
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid whole number (e.g., 10 or 30).")

# Function to get housing inputs
def get_housing_inputs() -> Dict[str, Any]:
    """
    Gathers all necessary inputs from the user for housing affordability calculations.
    Default values are provided for most inputs to guide the user.

    Returns:
        Dict[str, Any]: A dictionary containing all housing-related inputs.
                        Keys match the parameter names of `calculate_max_affordable_loan`.
    """
    print("\n--- Housing Affordability Inputs ---")
    # Gather various financial details relevant to mortgage calculation.
    annual_income = get_float_input("Enter your gross annual income: $", default=70000.0)
    annual_other_debt_payments = get_float_input("Enter your total annual payments for other debts (e.g., car, student loans): $", default=5000.0)
    mortgage_interest_rate_annual = get_float_input("Enter the annual mortgage interest rate (e.g., 0.065 for 6.5%): ", default=0.065)
    loan_term_years = get_int_input("Enter the loan term in years (e.g., 30): ", default=30)
    down_payment_percentage = get_float_input("Enter your down payment percentage (e.g., 10 for 10% of home price): ", default=10.0)
    estimated_annual_property_tax_and_insurance = get_float_input("Enter estimated annual property tax and insurance (T&I): $", default=3500.0)
    
    return {
        "annual_income": annual_income, # User's gross annual income
        "annual_other_debt_payments": annual_other_debt_payments, # User's other debt payments
        "mortgage_interest_rate_annual": mortgage_interest_rate_annual, # Expected mortgage rate
        "loan_term_years": loan_term_years, # Loan duration
        "down_payment_percentage": down_payment_percentage, # Down payment as a percentage
        "estimated_annual_property_tax_and_insurance": estimated_annual_property_tax_and_insurance # Estimated T&I costs
    }

# Function to get education inputs
def get_education_inputs() -> Dict[str, Any]:
    """
    Gathers all necessary inputs from the user for education cost planning.
    Default values are provided to guide the user.

    Returns:
        Dict[str, Any]: A dictionary containing all education cost-related inputs.
                        Keys match parameter names of `calculate_future_education_cost`.
    """
    print("\n--- Education Cost Planning Inputs ---")
    # Details for the first child
    current_age_child1 = get_int_input("Enter current age of child 1: ", default=2)
    years_of_college_child1 = get_int_input(f"Enter years of college for child 1 (e.g., 4, default is {4 if current_age_child1 > 0 else 0}): ", default=(4 if current_age_child1 > 0 else 0))
    
    # Details for the second child, conditional on whether there is a second child
    current_age_child2 = get_int_input("Enter current age of child 2 (enter 0 if no second child or to skip): ", default=0)
    years_of_college_child2 = 0
    if current_age_child2 > 0 : # Only ask for years if a second child's age is provided
        years_of_college_child2 = get_int_input(f"Enter years of college for child 2 (e.g., 4): ", default=4)
    
    # Common financial details for education planning
    current_annual_cost_per_child = get_float_input("Enter current annual cost of college per child (today's value): $", default=20000.0)
    annual_inflation_rate_education = get_float_input("Enter expected annual inflation rate for education (e.g., 0.05 for 5%): ", default=0.05)
    investment_return_rate = get_float_input("Enter expected average annual rate of return on investments (e.g., 0.07 for 7%): ", default=0.07)
    college_start_age = get_int_input("Enter typical college start age (default 18): ", default=18)

    return {
        "current_age_child1": current_age_child1, # Age of child 1
        "current_age_child2": current_age_child2, # Age of child 2 (0 if none)
        "years_of_college_child1": years_of_college_child1, # College duration for child 1
        "years_of_college_child2": years_of_college_child2, # College duration for child 2
        "current_annual_cost_per_child": current_annual_cost_per_child, # Current cost per child per year
        "annual_inflation_rate_education": annual_inflation_rate_education, # Education cost inflation
        "investment_return_rate": investment_return_rate, # Expected investment return
        "college_start_age": college_start_age # Age college typically starts
    }

# Function to get income projection inputs
def get_income_projection_inputs() -> Dict[str, Any]:
    """
    Gathers inputs from the user for projecting future income for up to two users.
    Default values are provided to guide the user.

    Returns:
        Dict[str, Any]: A dictionary containing all income projection-related inputs.
                        Keys match parameter names of `project_income`, with
                        `projection_years_income` for the projection period.
    """
    print("\n--- Income Projection Inputs ---")
    # Income details for user 1
    current_annual_income_user1 = get_float_input("Enter current annual income for user 1: $", default=50000.0)
    annual_growth_rate_user1 = get_float_input("Enter expected annual income growth rate for user 1 (e.g., 0.03 for 3%): ", default=0.03)
    
    # Income details for user 2, conditional on whether there is a second user
    current_annual_income_user2 = get_float_input("Enter current annual income for user 2 (enter 0 if single user or to skip): $", default=50000.0)
    annual_growth_rate_user2 = 0.0 # Default to 0 if no second income
    if current_annual_income_user2 > 0: # Ask for growth rate only if there's a second income
        annual_growth_rate_user2 = get_float_input("Enter expected annual income growth rate for user 2 (e.g., 0.03 for 3%): ", default=0.03)
        
    # Number of years to project income
    projection_years_income = get_int_input("Enter number of years to project income: ", default=10)

    return {
        "current_annual_income_user1": current_annual_income_user1, # Income user 1
        "current_annual_income_user2": current_annual_income_user2, # Income user 2 (0 if none)
        "annual_growth_rate_user1": annual_growth_rate_user1, # Growth rate user 1
        "annual_growth_rate_user2": annual_growth_rate_user2, # Growth rate user 2
        "projection_years_income": projection_years_income # Projection period for income
    }

# Function to get cost of living (CoL) projection inputs
def get_col_projection_inputs() -> Dict[str, Any]:
    """
    Gathers inputs from the user for projecting future Cost of Living (CoL),
    including specific expenses related to children.
    Default values are provided to guide the user.

    Returns:
        Dict[str, Any]: A dictionary containing all CoL projection-related inputs.
                        Keys match parameter names of `project_cost_of_living`,
                        with specific suffixes like '_col' for clarity.
    """
    print("\n--- Cost of Living Projection Inputs ---")
    # Base CoL and general inflation
    current_annual_col = get_float_input("Enter current total annual cost of living (excluding specific education/housing): $", default=40000.0)
    annual_col_inflation_rate = get_float_input("Enter general annual CoL inflation rate (e.g., 0.02 for 2%): ", default=0.02)
    
    # Child-related expenses
    child_related_annual_expense_increase_per_child = get_float_input("Enter child-related additional annual expense per child (in today's value): $", default=5000.0)
    
    num_children_for_col = get_int_input("How many children to consider for these CoL-specific expenses? ", default=2)
    ages_of_children_for_col: List[int] = [] # Type hint for clarity
    if child_related_annual_expense_increase_per_child > 0 and num_children_for_col > 0:
        print(f"Please enter current ages for {num_children_for_col} children for CoL expense tracking:")
        for i in range(num_children_for_col):
            # Default ages like 2, 4, etc., for convenience
            age = get_int_input(f"  Enter current age of child {i+1}: ", default= (i*2)+2) 
            ages_of_children_for_col.append(age)
    
    child_expense_start_age_col = get_int_input("Enter age at which these additional child expenses start: ", default=0)
    child_expense_end_age_col = get_int_input("Enter age at which these additional child expenses end (exclusive, e.g., 18 means up to age 17): ", default=18)
    
    # Projection period for CoL
    projection_years_col = get_int_input("Enter number of years to project CoL: ", default=10)

    return {
        "current_annual_col": current_annual_col, # Base CoL today
        "annual_col_inflation_rate": annual_col_inflation_rate, # General CoL inflation
        "child_related_annual_expense_increase_per_child": child_related_annual_expense_increase_per_child, # Per-child expense today
        "ages_of_children_col": ages_of_children_for_col, # List of children's ages for CoL
        "child_expense_start_age_col": child_expense_start_age_col, # Start age for child CoL expense
        "child_expense_end_age_col": child_expense_end_age_col, # End age for child CoL expense
        "projection_years_col": projection_years_col # Projection period for CoL
    }

# Main application logic
if __name__ == "__main__":
    print("Welcome to the Financial Planning CLI Tool!")
    print("==========================================")

    while True:
        print("\nPlease select an option:")
        print("1. Calculate Maximum Affordable Housing Loan")
        print("2. Calculate Future Education Costs")
        print("3. Project Future Income")
        print("4. Project Future Cost of Living")
        print("5. Generate Full Financial Summary")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            housing_inputs = get_housing_inputs()
    # Main loop for the CLI application
    while True:
        # Display menu options
        print("\nPlease select an option:")
        print("1. Calculate Maximum Affordable Housing Loan")
        print("2. Calculate Future Education Costs")
        print("3. Project Future Income")
        print("4. Project Future Cost of Living")
        print("5. Generate Full Financial Summary")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        # Option 1: Housing Loan Calculation
        if choice == '1':
            housing_inputs = get_housing_inputs()
            # Call the calculation function, passing arguments directly from the input dictionary
            max_loan = calculate_max_affordable_loan(
                annual_income=housing_inputs["annual_income"],
                annual_other_debt_payments=housing_inputs["annual_other_debt_payments"], # Note: not used in current PITI calc in core
                mortgage_interest_rate_annual=housing_inputs["mortgage_interest_rate_annual"],
                loan_term_years=housing_inputs["loan_term_years"],
                down_payment_percentage=housing_inputs["down_payment_percentage"],
                estimated_annual_property_tax_and_insurance=housing_inputs["estimated_annual_property_tax_and_insurance"]
            )
            print(f"\nMaximum Affordable Loan: ${max_loan:,.2f}")

        elif choice == '2':
            education_inputs = get_education_inputs()
            # Call the calculation function using dictionary unpacking for arguments
            education_costs = calculate_future_education_cost(**education_inputs) 
            print("\n--- Future Education Cost Projection ---")
            # Display formatted results
            print(f"  Total Future Inflated Cost: ${education_costs['total_future_inflated_cost']:,.2f}")
            print(f"  Lump Sum Needed Today (if invested): ${education_costs['lump_sum_needed_today']:,.2f}")
            if education_costs['annual_savings_needed'] == float('inf'):
                print(f"  Annual Savings Needed: Infinite (consider lump sum or re-evaluate inputs if college starts very soon/investment rates are low).")
            else:
                print(f"  Annual Savings Needed: ${education_costs['annual_savings_needed']:,.2f}")
        
        # Option 3: Income Projection
        elif choice == '3':
            income_inputs = get_income_projection_inputs()
            # Call the calculation function, passing arguments from the input dictionary
            projected_incomes = project_income(
                current_annual_income_user1=income_inputs["current_annual_income_user1"],
                current_annual_income_user2=income_inputs["current_annual_income_user2"], # Will be 0 if single user
                annual_growth_rate_user1=income_inputs["annual_growth_rate_user1"], # Growth rate for user 1
                annual_growth_rate_user2=income_inputs["annual_growth_rate_user2"], # Growth rate for user 2 (0 if no second income)
                projection_years=income_inputs["projection_years_income"] # Use the projection period from income inputs
            )
            print("\n--- Income Projection ---")
            # Display formatted results for each year
            for yearly_income in projected_incomes:
                print(f"Year {int(yearly_income['year'])}: User1 Income: ${yearly_income['user1_income']:,.2f}, "
                      f"User2 Income: ${yearly_income['user2_income']:,.2f}, "
                      f"Combined: ${yearly_income['combined_income']:,.2f}")
        
        # Option 4: Cost of Living Projection
        elif choice == '4':
            col_inputs = get_col_projection_inputs()
            # Call the calculation function, passing arguments from the input dictionary
            projected_cols = project_cost_of_living(
                current_annual_col=col_inputs["current_annual_col"],
                annual_col_inflation_rate=col_inputs["annual_col_inflation_rate"],
                child_related_annual_expense_increase_per_child=col_inputs["child_related_annual_expense_increase_per_child"],
                ages_of_children=col_inputs["ages_of_children_col"], # Use specific key for ages list
                child_expense_start_age=col_inputs["child_expense_start_age_col"], # Use specific key
                child_expense_end_age=col_inputs["child_expense_end_age_col"], # Use specific key
                projection_years=col_inputs["projection_years_col"] # Use specific key for CoL projection period
            )
            print("\n--- Cost of Living Projection ---")
            # Display formatted results for each year
            for yearly_col in projected_cols:
                print(f"Year {int(yearly_col['year'])}: Base CoL: ${yearly_col['base_cost_of_living']:,.2f}, "
                      f"Child Expenses: ${yearly_col['additional_child_expenses']:,.2f}, "
                      f"Total CoL: ${yearly_col['total_cost_of_living']:,.2f}")
        
        # Option 5: Full Financial Summary
        elif choice == '5':
            print("\n--- Full Financial Summary Generation ---")
            print("This requires inputs for income, cost of living, education, and housing.")

            # 1. Gather Income Projection Inputs (this also sets the overall projection_years for the summary)
            income_inputs = get_income_projection_inputs()
            summary_projection_years = income_inputs["projection_years_income"] 
            print(f"\nSummary will be projected for {summary_projection_years} years (based on income projection period).")

            # 2. Gather Cost of Living Inputs (specifically for the summary, using summary_projection_years)
            #    This is done by calling the get_col_projection_inputs but we will use its components
            #    and override projection_years with summary_projection_years for the actual call to project_cost_of_living.
            #    Or, more simply, we can just re-gather the specific CoL inputs needed.
            print("\n--- Cost of Living Inputs for Summary ---")
            current_annual_col_summary = get_float_input("Enter current total annual cost of living (excluding specific education/housing): $", default=40000.0)
            annual_col_inflation_rate_summary = get_float_input("Enter general annual CoL inflation rate (e.g., 0.02 for 2%): ", default=0.02)
            child_related_expense_summary = get_float_input("Enter child-related additional annual expense per child (today's value): $", default=5000.0)
            num_children_summary = get_int_input(f"How many children for CoL-specific expenses (for {summary_projection_years} years)? ", default=0)
            ages_children_summary: List[int] = []
            if child_related_expense_summary > 0 and num_children_summary > 0:
                for i in range(num_children_summary):
                    age = get_int_input(f"  Enter current age of child {i+1} for CoL: ", default=(i*2)+2)
                    ages_children_summary.append(age)
            child_expense_start_summary = get_int_input("Enter start age for these additional child CoL expenses: ", default=0)
            child_expense_end_summary = get_int_input("Enter end age (exclusive) for these additional child CoL expenses: ", default=18)

            # 3. Gather Education Inputs & Calculate Annual Savings Needed
            education_inputs = get_education_inputs()
            education_cost_details = calculate_future_education_cost(**education_inputs)
            annual_education_savings_needed = education_cost_details['annual_savings_needed']
            # Handle cases where education savings might be infinite (e.g., college starts immediately)
            if annual_education_savings_needed == float('inf'):
                print("\nWarning: Annual education savings needed is calculated as infinite.")
                print("This might be due to college starting immediately or other factors.")
                override_edu_savings = get_float_input("Enter a specific annual amount for education savings if 'infinite' is not desired for the summary (or 0 to ignore): $", default=0.0)
                annual_education_savings_needed = override_edu_savings

            # 4. Get Annual Mortgage Payment Input
            annual_mortgage_payment = get_float_input("\nEnter your estimated total annual mortgage payment (PITI): $", default=12000.0)

            # 5. Prepare parameters and call generate_financial_summary
            summary_params = {
                "current_annual_income_user1": income_inputs["current_annual_income_user1"],
                "current_annual_income_user2": income_inputs["current_annual_income_user2"],
                "annual_growth_rate_user1": income_inputs["annual_growth_rate_user1"],
                "annual_growth_rate_user2": income_inputs["annual_growth_rate_user2"],
                "current_annual_col": current_annual_col_summary, # Use summary-specific CoL base
                "annual_col_inflation_rate": annual_col_inflation_rate_summary, # Summary CoL inflation
                "child_related_annual_expense_increase_per_child": child_related_expense_summary, # Summary child expense
                "ages_of_children": ages_children_summary, # Summary children ages
                "child_expense_start_age": child_expense_start_summary, # Summary child expense start
                "child_expense_end_age": child_expense_end_summary, # Summary child expense end
                "annual_education_savings_needed": annual_education_savings_needed, # From education calculation
                "annual_mortgage_payment": annual_mortgage_payment, # Direct input
                "projection_years": summary_projection_years # Consistent projection period
            }
            
            full_summary = generate_financial_summary(**summary_params) # Unpack all params
            print("\n--- Full Financial Summary Output ---")
            # Display formatted summary results
            for yearly_summary in full_summary:
                print(f"Year {int(yearly_summary['year'])}:")
                print(f"  Projected Combined Income: ${yearly_summary['projected_combined_income']:,.2f}")
                print(f"  Projected Cost of Living: ${yearly_summary['projected_cost_of_living']:,.2f}")
                print(f"  Projected Education Savings: ${yearly_summary['projected_education_savings']:,.2f}")
                print(f"  Projected Housing Payment: ${yearly_summary['projected_housing_payment']:,.2f}")
                print(f"  Projected Total Expenses: ${yearly_summary['projected_total_expenses']:,.2f}")
                print(f"  Projected Net Savings: ${yearly_summary['projected_net_savings']:,.2f}")
                print("-" * 30) # Separator for readability

        # Option 6: Exit
        elif choice == '6':
            print("\nThank you for using the Financial Planning CLI Tool. Goodbye!")
            break # Exit the main loop

        # Handle invalid menu choices
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")
        
        # Pause for user to read output before re-displaying the menu
        input("\nPress Enter to continue...")
