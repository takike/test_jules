# Family Financial Planning CLI Tool

A command-line application to help with various aspects of personal financial planning.

## Features

This tool provides the following functionalities through an interactive command-line menu:

1.  **Calculate Maximum Affordable Housing Loan:**
    *   Estimates the maximum mortgage principal you might afford based on your income, other debts, desired loan term, interest rate, and estimated property taxes/insurance.
    *   Key assumptions: Uses a standard 28% front-end DTI (Debt-to-Income) ratio for housing costs (Principal, Interest, Taxes, Insurance - PITI).

2.  **Calculate Future Education Costs:**
    *   Projects the future cost of college for up to two children, considering current costs, education-specific inflation, and the number of years of college.
    *   Calculates the total inflated cost, the lump sum you would need to invest today, and the estimated annual savings required to meet those future costs, factoring in potential investment returns.

3.  **Project Future Income:**
    *   Forecasts combined future annual income for two individuals over a specified number of years, based on current incomes and estimated annual growth rates.

4.  **Project Future Cost of Living:**
    *   Estimates future annual cost of living, considering general inflation and additional expenses related to children within a specified age range.

5.  **Generate Full Financial Summary:**
    *   Provides a year-by-year projection combining income, cost of living, education savings, and housing payments to show net savings over a chosen period.
    *   Requires inputs for income, cost of living, education savings goals (derived from the education cost calculator), and planned annual mortgage payments.

## Getting Started

### Prerequisites

*   Python 3.x

### Running the Application

1.  Clone this repository or download the source files.
2.  Navigate to the root directory of the project in your terminal.
3.  Run the application using the following command:
    ```bash
    python app.py
    ```
4.  The application will then present you with a menu of options. Follow the on-screen prompts to input your financial details.

## How It Works

The application is structured into two main Python files:

*   `app.py`: Handles the command-line interface, user input, and orchestrates the calls to the financial logic.
*   `core/finance_calculator.py`: Contains all the core functions for performing the financial calculations.

Unit tests are located in `tests/test_finance_calculator.py`.

## Assumptions & Simplifications

This tool uses several assumptions and simplifications for its calculations:

*   **Income Growth:** Assumes a constant average annual growth rate. Real-world income can be more variable.
*   **Inflation Rates:** Uses constant average inflation rates. Actual rates vary.
*   **Investment Returns:** Assumes a constant average annual rate of return. Actual returns are not guaranteed and can fluctuate significantly.
*   **Housing Loan:** Primarily uses a 28% PITI-to-income ratio. Lender criteria can vary and may include total DTI limits (typically 36-43%). The current version simplifies total DTI considerations.
*   **Education Costs:** Projections are highly sensitive to assumed inflation and investment rates.
*   **Cost of Living:** Child-related expenses are added as a fixed amount (inflated over time) per child within a defined age range. Actual child-rearing costs can be more dynamic.
*   **Taxes (Income, Capital Gains):** The application does not currently factor in income taxes on earnings or taxes on investment returns for education savings. These can have a significant impact on real-world outcomes.
*   **No GUI:** This is a command-line tool.

This tool is for estimation and educational purposes only. Consult with a qualified financial advisor for personalized advice.
