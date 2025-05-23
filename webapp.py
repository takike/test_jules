from flask import Flask, render_template, request, redirect, url_for # Added request, redirect, url_for
from core.finance_calculator import (
    calculate_max_affordable_loan,
    calculate_future_education_cost,
    project_income,
    project_cost_of_living,
    generate_financial_summary
)

app = Flask(__name__)

# Placeholder for secret key if we use sessions later
# app.secret_key = 'your secret key'

@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/housing', methods=['GET', 'POST'])
def housing_calculator():
    error = None
    result = None
    if request.method == 'POST':
        try:
            # Retrieve form data
            annual_income = float(request.form['annual_income'])
            annual_other_debt_payments = float(request.form['annual_other_debt_payments'])
            mortgage_interest_rate_annual = float(request.form['mortgage_interest_rate_annual'])
            loan_term_years = int(request.form['loan_term_years'])
            down_payment_percentage = float(request.form['down_payment_percentage']) # Not directly used by current calculate_max_affordable_loan but good to have
            estimated_annual_property_tax_and_insurance = float(request.form['estimated_annual_property_tax_and_insurance'])

            # Validate inputs (basic example, can be more thorough)
            if not (annual_income > 0 and \
                    mortgage_interest_rate_annual > 0 and \
                    mortgage_interest_rate_annual < 1 and \
                    loan_term_years > 0 and \
                    estimated_annual_property_tax_and_insurance >= 0 and \
                    down_payment_percentage >=0 and \
                    annual_other_debt_payments >=0 ): # other debts can be 0
                error = "Invalid input values. Please check the constraints: Income, interest rate (0-1), and loan term must be positive. Other fields can be zero or positive."
            
            # Add more specific validation as needed, e.g. rate < 1 (done above)

            if not error:
                # Call the core calculator function (ensure parameter names match the function signature)
                result = calculate_max_affordable_loan(
                    annual_income=annual_income,
                    annual_other_debt_payments=annual_other_debt_payments,
                    mortgage_interest_rate_annual=mortgage_interest_rate_annual,
                    loan_term_years=loan_term_years,
                    down_payment_percentage=down_payment_percentage, # Pass it even if not used by the core logic currently for future flexibility
                    estimated_annual_property_tax_and_insurance=estimated_annual_property_tax_and_insurance
                )
        except ValueError:
            error = "Invalid input. Please ensure all fields are numbers."
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"
    
    return render_template('housing_loan_form.html', title='Housing Loan Calculator', result=result, error=error)

@app.route('/education', methods=['GET', 'POST'])
def education_calculator():
    error = None
    result = None
    if request.method == 'POST':
        try:
            # Retrieve form data
            current_age_child1 = int(request.form['current_age_child1'])
            years_of_college_child1 = int(request.form['years_of_college_child1'])
            current_age_child2 = int(request.form['current_age_child2'])
            years_of_college_child2 = int(request.form['years_of_college_child2'])
            current_annual_cost_per_child = float(request.form['current_annual_cost_per_child'])
            annual_inflation_rate_education = float(request.form['annual_inflation_rate_education'])
            investment_return_rate = float(request.form['investment_return_rate'])
            college_start_age = int(request.form['college_start_age'])

            # Basic Validations (can be more comprehensive)
            if not (0 <= current_age_child1 <= college_start_age + 10 and 0 <= current_age_child2 <= college_start_age + 10): # Max age reasonable check
                error = "Child ages seem unrealistic."
            if not (0 <= years_of_college_child1 <= 10 and 0 <= years_of_college_child2 <= 10): # Max years of college check
                error = "Years of college seems unrealistic (0-10)."
            if not (current_annual_cost_per_child >= 0):
                error = "Current annual cost per child must be non-negative."
            if not (0 <= annual_inflation_rate_education < 1 and 0 <= investment_return_rate < 1) : # Rates should be less than 100%
                 error = "Inflation and return rates should be realistic (e.g., 0.05 for 5%)."   
            if not (college_start_age > 0):
                error = "College start age must be positive."

            if not error:
                result = calculate_future_education_cost(
                    current_age_child1=current_age_child1,
                    years_of_college_child1=years_of_college_child1,
                    current_age_child2=current_age_child2,
                    years_of_college_child2=years_of_college_child2,
                    current_annual_cost_per_child=current_annual_cost_per_child,
                    annual_inflation_rate_education=annual_inflation_rate_education,
                    investment_return_rate=investment_return_rate,
                    college_start_age=college_start_age
                )
        except ValueError:
            error = "Invalid input. Please ensure all fields are numbers and ages/years are integers."
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"
    
    return render_template('education_cost_form.html', title='Education Cost Calculator', result=result, error=error)

@app.route('/income_projection', methods=['GET', 'POST'])
def income_projection_calculator():
    error = None
    result = None # This will be a list of dictionaries
    if request.method == 'POST':
        try:
            current_annual_income_user1 = float(request.form['current_annual_income_user1'])
            annual_growth_rate_user1 = float(request.form['annual_growth_rate_user1'])
            current_annual_income_user2 = float(request.form['current_annual_income_user2'])
            annual_growth_rate_user2 = float(request.form['annual_growth_rate_user2'])
            projection_years = int(request.form['projection_years'])

            # Validations
            if not (current_annual_income_user1 >= 0 and current_annual_income_user2 >= 0):
                error = "Current annual incomes must be non-negative."
            if not (-0.5 < annual_growth_rate_user1 < 1 and -0.5 < annual_growth_rate_user2 < 1): # Allow for negative growth but cap at 100% growth or 50% decline
                error = "Annual growth rates should be realistic (e.g., 0.03 for 3%, between -0.5 and 1)."
            if not (0 < projection_years <= 50): # Max 50 years projection
                error = "Projection years must be between 1 and 50."
            
            if not error:
                result = project_income(
                    current_annual_income_user1=current_annual_income_user1,
                    annual_growth_rate_user1=annual_growth_rate_user1,
                    current_annual_income_user2=current_annual_income_user2,
                    annual_growth_rate_user2=annual_growth_rate_user2,
                    projection_years=projection_years
                )
        except ValueError:
            error = "Invalid input. Please ensure all fields are numbers and projection years is an integer."
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"
    
    return render_template('income_projection_form.html', title='Income Projection', result=result, error=error)

@app.route('/col_projection', methods=['GET', 'POST'])
def col_projection_calculator():
    error = None
    result = None # This will be a list of dictionaries
    if request.method == 'POST':
        try:
            current_annual_col = float(request.form['current_annual_col'])
            annual_col_inflation_rate = float(request.form['annual_col_inflation_rate'])
            child_related_annual_expense_increase_per_child = float(request.form['child_related_annual_expense_increase_per_child'])
            
            # Handle ages_of_children string
            ages_of_children_str = request.form.get('ages_of_children', '') # Use .get for optional field
            ages_of_children = []
            if ages_of_children_str: # If not empty
                try:
                    ages_of_children = [int(age.strip()) for age in ages_of_children_str.split(',') if age.strip()]
                except ValueError:
                    error = "Ages of children must be a comma-separated list of numbers (e.g., 2,5)."
                    # Render template immediately if there's an error here to avoid further processing
                    return render_template('col_projection_form.html', title='Cost of Living Projection', result=None, error=error)

            child_expense_start_age = int(request.form['child_expense_start_age'])
            child_expense_end_age = int(request.form['child_expense_end_age'])
            projection_years = int(request.form['projection_years'])

            # Basic Validations
            if not (current_annual_col >= 0 and child_related_annual_expense_increase_per_child >= 0):
                error = "Costs must be non-negative."
            if not (-0.1 < annual_col_inflation_rate < 1): # Allow small deflation but cap inflation
                 error = "CoL inflation rate should be realistic (e.g., 0.02 for 2%, between -0.1 and 1)."
            if not (0 < projection_years <= 50):
                 error = "Projection years must be between 1 and 50."
            if not (0 <= child_expense_start_age < 100 and 0 < child_expense_end_age <= 100 and child_expense_start_age < child_expense_end_age):
                error = "Child expense ages must be realistic (0-99 for start, 1-100 for end) and start age must be less than end age."
            for age_val in ages_of_children: # Renamed age to age_val to avoid conflict with html input field name
                if not (0 <= age_val < 100):
                    error = "Child ages must be realistic (0-99)."
                    break
            if error: # Re-check error before calling calculator
                return render_template('col_projection_form.html', title='Cost of Living Projection', result=None, error=error)


            if not error: # Final check before calling the core function
                result = project_cost_of_living(
                    current_annual_col=current_annual_col,
                    annual_col_inflation_rate=annual_col_inflation_rate,
                    child_related_annual_expense_increase_per_child=child_related_annual_expense_increase_per_child,
                    ages_of_children=ages_of_children, # Pass the list of integers
                    child_expense_start_age=child_expense_start_age,
                    child_expense_end_age=child_expense_end_age,
                    projection_years=projection_years
                )
        except ValueError: # Catches float/int conversion errors for other fields
            error = "Invalid input. Please ensure all cost, rate, age, and year fields are valid numbers."
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"
    
    return render_template('col_projection_form.html', title='Cost of Living Projection', result=result, error=error)

@app.route('/summary', methods=['GET', 'POST'])
def financial_summary_calculator():
    error = None
    result = None # This will be a list of dictionaries
    if request.method == 'POST':
        try:
            # Income params
            current_annual_income_user1 = float(request.form['current_annual_income_user1'])
            annual_growth_rate_user1 = float(request.form['annual_growth_rate_user1'])
            current_annual_income_user2 = float(request.form['current_annual_income_user2'])
            annual_growth_rate_user2 = float(request.form['annual_growth_rate_user2'])

            # CoL params
            current_annual_col = float(request.form['current_annual_col'])
            annual_col_inflation_rate = float(request.form['annual_col_inflation_rate'])
            child_related_annual_expense_increase_per_child = float(request.form['child_related_annual_expense_increase_per_child'])
            
            ages_of_children_str = request.form.get('ages_of_children', '')
            ages_of_children = []
            if ages_of_children_str:
                try:
                    ages_of_children = [int(age.strip()) for age in ages_of_children_str.split(',') if age.strip()]
                except ValueError:
                    error = "Ages of children must be a comma-separated list of numbers."
                    return render_template('financial_summary_form.html', title='Full Financial Summary', result=None, error=error)
            
            child_expense_start_age = int(request.form['child_expense_start_age'])
            child_expense_end_age = int(request.form['child_expense_end_age'])

            # Fixed expenses
            annual_education_savings_needed = float(request.form['annual_education_savings_needed'])
            annual_mortgage_payment = float(request.form['annual_mortgage_payment'])

            # Projection years
            projection_years = int(request.form['projection_years'])

            # Basic Validations (many of these are similar to individual calculators, could be refactored into helper validation functions later)
            if not (current_annual_income_user1 >= 0 and current_annual_income_user2 >= 0 and current_annual_col >= 0 and \
                    child_related_annual_expense_increase_per_child >= 0 and annual_education_savings_needed >= 0 and annual_mortgage_payment >= 0):
                error = "All monetary amounts (incomes, costs, savings, payments) must be non-negative."
            if not (-0.5 < annual_growth_rate_user1 < 1 and -0.5 < annual_growth_rate_user2 < 1 and \
                    -0.1 < annual_col_inflation_rate < 1):
                error = "Growth and inflation rates must be realistic (e.g., 0.03 for 3%). For growth rates between -0.5 and 1. For CoL inflation between -0.1 and 1."
            if not (0 < projection_years <= 50):
                error = "Projection years must be between 1 and 50."
            if not (0 <= child_expense_start_age < 100 and 0 < child_expense_end_age <= 100 and child_expense_start_age < child_expense_end_age): # Corrected: child_expense_start_age can be 0
                 error = "Child expense ages must be realistic and start age must be less than end age."
            for age_val in ages_of_children: # Renamed age to age_val
                if not (0 <= age_val < 100):
                    error = "Child ages must be realistic (0-99)."
                    break
            if error: # Re-check error before calling calculator
                return render_template('financial_summary_form.html', title='Full Financial Summary', result=None, error=error)

            if not error:
                result = generate_financial_summary(
                    current_annual_income_user1=current_annual_income_user1,
                    current_annual_income_user2=current_annual_income_user2,
                    annual_growth_rate_user1=annual_growth_rate_user1,
                    annual_growth_rate_user2=annual_growth_rate_user2,
                    current_annual_col=current_annual_col,
                    annual_col_inflation_rate=annual_col_inflation_rate,
                    child_related_annual_expense_increase_per_child=child_related_annual_expense_increase_per_child,
                    ages_of_children=ages_of_children,
                    child_expense_start_age=child_expense_start_age,
                    child_expense_end_age=child_expense_end_age,
                    annual_education_savings_needed=annual_education_savings_needed,
                    annual_mortgage_payment=annual_mortgage_payment,
                    projection_years=projection_years
                )
        except ValueError:
            error = "Invalid input. Please ensure all fields are valid numbers."
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"
    
    return render_template('financial_summary_form.html', title='Full Financial Summary', result=result, error=error)

if __name__ == '__main__':
    # Note: Debug mode should be False in a production environment
    app.run(debug=True)
