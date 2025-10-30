import os
import pandas as pd

# Define the directories
directories = [
    "v3-10rep-1_1mx1_1mm",
    "v4-10rep-1_1mx1_1mm",
    "v5-10rep-1_1mx1_1mm"
]

# Define the specific filenames to process
filenames_to_process = [
    "polarity-comparison-results.csv"
]

# Merge files with the same name
for filename in filenames_to_process:
    combined_data = pd.DataFrame()
    for directory in directories:
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            # Read the CSV file without enforcing dtype
            data = pd.read_csv(filepath)

            # Convert the 'value' column to integers if necessary
            if 'value' in data.columns:
                data['value'] = data['value'].astype('int64')

            # Use concatenation and groupby to sum the counts
            combined_data = pd.concat([combined_data, data])
            combined_data = combined_data.groupby('coil', as_index=False).sum()
            combined_data['value'] =  combined_data['value']

    # Write the combined data to a new file
    output_filename = filename.replace(".csv", "-merged.csv")
    combined_data.to_csv(output_filename, index=False)
