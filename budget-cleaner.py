import pandas as pd

# Load the Excel file
file_path = 'your_excel_file.xlsx'  # Replace with your file path
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
df['work tags'] = df['work tags'].apply(parse_work_tags).apply(pd.Series)

# Concatenate the original DataFrame with the parsed work tags columns
result_df = pd.concat([df, df['work tags']], axis=1)

# Drop the original 'work tags' column if needed
result_df.drop(columns=['work tags'], inplace=True)

# Save the result to a new Excel file
result_df.to_excel('output_excel_file.xlsx', index=False)
