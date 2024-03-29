# %%
import pandas as pd
from pathlib import Path
import pandas as pd

EXPENSE_FILE = "ProMIS Expense.xlsx"
OBLIGATIONS_FILE = "ProMIS Obligations.xlsx"
DATA = Path("data")

# %% Cell 1
# Assign the path where the files exists
# Load the Excel file
def parse_work_tags_column(file_path):
    df = pd.read_excel(DATA/file_path)

    # Create a function to parse the work tags column
    def parse_work_tags(work_tags):
        tag_dict = {}
        lines = work_tags.split('\n')
        for line in lines:
            if line.strip():  # Skip empty lines
                tag_name, tag_value = line.strip().split(': ')
                tag_dict[tag_name] = tag_value
        return tag_dict

    # Apply the parse_work_tags function to the 'work tags' column and expand it into separate columns
    df_worktags = df['Worktags'].apply(parse_work_tags).apply(pd.Series)

    # Concatenate the original DataFrame with the parsed work tags columns
    result_df = pd.concat([df, df_worktags], axis=1)

    # Drop the original 'work tags' column if needed
    columns_to_drop = ['Worktags','Accounting Date', 'Operational Transaction', 'Journal',
       'Revenue Category','AASIS Code', 'Cost Center', 'Designated','Earning', 'Employee Type', 'Fund', 'Job Profile',
       'Location', 'NACUBO Function', 'Pay Group', 'Pay Rate Type','Personnel Services Restrictions', 'Position', 'Deduction (Workday Owned)', 'Fringe Basis']
    result_df.drop(columns=columns_to_drop, inplace=True,errors='ignore')

    return result_df

expense_df = parse_work_tags_column(EXPENSE_FILE)
obligation_df = parse_work_tags_column(OBLIGATIONS_FILE)
# %%

# Create an Excel writer object
with pd.ExcelWriter(DATA/"results.xlsx") as writer:
    # Write the DataFrame to the Excel file in a new sheet
    expense_df.to_excel(writer, sheet_name='Expense', index=False)
    obligation_df.to_excel(writer, sheet_name='Obligations', index=False)
    
    # # Create a sheet with a pivot table of the expense data
    # expense_pivot = pd.pivot_table(expense_df, index=["Ledger Account","Spend Category", "Employee"], values='Transaction Amount', aggfunc='sum')
    # obligation_pivot = pd.pivot_table(obligation_df, index=["Ledger Account","Spend Category", "Employee"], values='Transaction Amount', aggfunc='sum')
    
    # # Write the pivot table to the Excel file
    # expense_pivot.to_excel(writer, sheet_name='Expense Pivot')
    # obligation_pivot.to_excel(writer, sheet_name='Obligations Pivot')
    

# %%
