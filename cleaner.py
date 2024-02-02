
import pandas as pd
from pathlib import Path
import click 

# Assign the path where the files exists
# Load the Excel file
def parse_work_tags_column(file_path):
    df = pd.read_excel(file_path)

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

# Using the click library to create a command line interface
@click.command()
@click.option('--expense', '-e', help='The expense file to process')
@click.option('--obligations', '-o', help='The obligations file to process')
def process_files(expense, obligations):
    expense_df = parse_work_tags_column(expense)
    obligation_df = parse_work_tags_column(obligations)

    # Create an Excel writer object
    with pd.ExcelWriter("results.xlsx") as writer:
        # Write the DataFrame to the Excel file in a new sheet
        expense_df.to_excel(writer, sheet_name='Expense', index=False)
        obligation_df.to_excel(writer, sheet_name='Obligations', index=False)

        # Write the pivot table to the Excel file
        expense_pivot.to_excel(writer, sheet_name='Expense Pivot')
        obligation_pivot.to_excel(writer, sheet_name='Obligations Pivot')


if __name__ == '__main__':
    process_files()