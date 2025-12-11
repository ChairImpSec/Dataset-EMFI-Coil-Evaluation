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
    "coils-lvt-c0_polarity_0.csv",
    "coils-lvt-c0_polarity_1.csv",
    "coils-lvt-c1_polarity_0.csv",
    "coils-lvt-c1_polarity_1.csv",
    "coils-lvt-c2_polarity_0.csv",
    "coils-lvt-c2_polarity_1.csv",
    "coils-lvt-c3_polarity_0.csv",
    "coils-lvt-c3_polarity_1.csv",
    "coils-lvt-c4_polarity_0.csv",
    "coils-lvt-c4_polarity_1.csv",
    "coils-lvt-c5_polarity_0.csv",
    "coils-lvt-c5_polarity_1.csv",
    "coils-lvt-c6_polarity_0.csv",
    "coils-lvt-c6_polarity_1.csv",
    "coils-lvt-c7_polarity_0.csv",
    "coils-lvt-c7_polarity_1.csv",
    "coils-lvt-c8_polarity_0.csv",
    "coils-lvt-c8_polarity_1.csv",
    "coils-lvt-c9_polarity_0.csv",
    "coils-lvt-c9_polarity_1.csv",
    "coils-lvt-c10_polarity_0.csv",
    "coils-lvt-c10_polarity_1.csv",

    "coils-std-c0_polarity_0.csv",
    "coils-std-c0_polarity_1.csv",
    "coils-std-c1_polarity_0.csv",
    "coils-std-c1_polarity_1.csv",
    "coils-std-c2_polarity_0.csv",
    "coils-std-c2_polarity_1.csv",
    "coils-std-c3_polarity_0.csv",
    "coils-std-c3_polarity_1.csv",
    "coils-std-c4_polarity_0.csv",
    "coils-std-c4_polarity_1.csv",
    "coils-std-c5_polarity_0.csv",
    "coils-std-c5_polarity_1.csv",
    "coils-std-c6_polarity_0.csv",
    "coils-std-c6_polarity_1.csv",
    "coils-std-c7_polarity_0.csv",
    "coils-std-c7_polarity_1.csv",
    "coils-std-c8_polarity_0.csv",
    "coils-std-c8_polarity_1.csv",
    "coils-std-c9_polarity_0.csv",
    "coils-std-c9_polarity_1.csv",
    "coils-std-c10_polarity_0.csv",
    "coils-std-c10_polarity_1.csv",

    "coils-hvt-c0_polarity_0.csv",
    "coils-hvt-c0_polarity_1.csv",
    "coils-hvt-c1_polarity_0.csv",
    "coils-hvt-c1_polarity_1.csv",
    "coils-hvt-c2_polarity_0.csv",
    "coils-hvt-c2_polarity_1.csv",
    "coils-hvt-c3_polarity_0.csv",
    "coils-hvt-c3_polarity_1.csv",
    "coils-hvt-c4_polarity_0.csv",
    "coils-hvt-c4_polarity_1.csv",
    "coils-hvt-c5_polarity_0.csv",
    "coils-hvt-c5_polarity_1.csv",
    "coils-hvt-c6_polarity_0.csv",
    "coils-hvt-c6_polarity_1.csv",
    "coils-hvt-c7_polarity_0.csv",
    "coils-hvt-c7_polarity_1.csv",
    "coils-hvt-c8_polarity_0.csv",
    "coils-hvt-c8_polarity_1.csv",
    "coils-hvt-c9_polarity_0.csv",
    "coils-hvt-c9_polarity_1.csv",
    "coils-hvt-c10_polarity_0.csv",
    "coils-hvt-c10_polarity_1.csv"
]

# Merge files with the same name
for filename in filenames_to_process:
    combined_data = pd.DataFrame()
    for directory in directories:
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            # Read the CSV file and ensure the 'Count' column is numeric
            data = pd.read_csv(filepath, dtype={'Count': 'int64'})
            # Use concatenation and groupby to sum the counts
            combined_data = pd.concat([combined_data, data])
            combined_data = combined_data.groupby('V-Level', as_index=False).sum()

    # Write the combined data to a new file
    output_filename = filename.replace(".csv", "_merged.csv")
    combined_data.to_csv(output_filename, index=False)
