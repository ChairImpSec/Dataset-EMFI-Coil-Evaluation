import os
import pandas as pd


# Define the specific filenames to process
filenames_to_process = [
    "coils-lvt-c0_polarity_0_merged.csv",
    "coils-lvt-c0_polarity_1_merged.csv",
    "coils-lvt-c1_polarity_0_merged.csv",
    "coils-lvt-c1_polarity_1_merged.csv",
    "coils-lvt-c2_polarity_0_merged.csv",
    "coils-lvt-c2_polarity_1_merged.csv",
    "coils-lvt-c3_polarity_0_merged.csv",
    "coils-lvt-c3_polarity_1_merged.csv",
    "coils-lvt-c4_polarity_0_merged.csv",
    "coils-lvt-c4_polarity_1_merged.csv",
    "coils-lvt-c5_polarity_0_merged.csv",
    "coils-lvt-c5_polarity_1_merged.csv",
    "coils-lvt-c6_polarity_0_merged.csv",
    "coils-lvt-c6_polarity_1_merged.csv",
    "coils-lvt-c7_polarity_0_merged.csv",
    "coils-lvt-c7_polarity_1_merged.csv",
    "coils-lvt-c8_polarity_0_merged.csv",
    "coils-lvt-c8_polarity_1_merged.csv",
    "coils-lvt-c9_polarity_0_merged.csv",
    "coils-lvt-c9_polarity_1_merged.csv",
    "coils-lvt-c10_polarity_0_merged.csv",
    "coils-lvt-c10_polarity_1_merged.csv",
]

# Merge files with the same name
for filename in filenames_to_process:
    combined_data = pd.DataFrame()
    data = pd.read_csv(filename, dtype={'Count': 'int64'})

    old =  'lvt'
    for type_ in ['std', 'hvt']:
        if os.path.exists(filename):
            # Read the CSV file and ensure the 'Count' column is numeric
            # Use concatenation and groupby to sum the counts
            combined_data = pd.concat([combined_data, data])
            combined_data = combined_data.groupby('V-Level', as_index=False).sum()

            new_filename = filename.replace(old, type_)
            data = pd.read_csv(filename, dtype={'Count': 'int64'})
            old = type_

    # Write the combined data to a new file
    output_filename = filename.replace(".csv", "_merged.csv")
    combined_data.to_csv(output_filename, index=False)
