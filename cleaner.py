import pandas as pd
from pathlib import Path
import click 
import warnings
import os

# To suppress the specific warning, uncomment the following line
warnings.filterwarnings("ignore", message="Workbook contains no default style, apply openpyxl's default")

# Assign the path where the files exists
# Load the Excel file
def parse_work_tags_column(file_path):
    df = pd.read_excel(file_path)

    # This function will parse the 'work tags' column into separate columns
    #  it's called as a vector operation on the 'work tags' column
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
@click.argument('input', required=True, type=click.Path(exists=True))
#@click.option('--input', '-i', required=True, type=click.Path(exists=True), help='The file to process')
@click.option('--output', '-o', default='results.xlsx', help='The output file to save the results')
@click.option('--sheet', '-s', default='expenses', help='The sheet name to save the results')
def process_files(input, output, sheet):
    # If no input file is provided, use the default file
    if input is None:
        raise click.UsageError("Please provide an input file.")
    
    if not Path.exists(Path(input)):
            raise click.UsageError(f"The default input file '{input}' does not exist. Please provide an input file.")
    
    # Proceed with processing the file
    print(f"Processing file: {input}")
    print(f"Results will be saved in: {output}, Sheet: {sheet}")
    expense_df = parse_work_tags_column(input)
    
    # Create an Excel writer object
    with pd.ExcelWriter(output) as writer:
        # Write the DataFrame to the Excel file in a new sheet
        expense_df.to_excel(writer, sheet_name='Expense', index=False)

    # Complete
    print("Processing complete.")
    
if __name__ == '__main__':
    process_files()