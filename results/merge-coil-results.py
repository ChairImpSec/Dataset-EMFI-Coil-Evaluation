import os
import pandas as pd
from itertools import product

def compute_and_save_coil_differences(directory, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the coil types and X values of interest
    coil_types = ['lvt', 'std', 'hvt', 'pinout-hvt', 'pinout-std', 'pinout-lvt']
    x_values = range(11)  # X \in [0, 10]

    # Dictionary to store dataframes for each coil type and X value
    coil_data = {ct: {x: None for x in x_values} for ct in coil_types}

    # Load data for each coil type and X value
    for ct in coil_types:
        for x in x_values:
            if ct.startswith('pinout'):
                # New file naming convention for pinout coils
                file_name = f'merged-detection-heatmap-coilcoils-pinout-c{x}-{ct.split("-")[1]}-pinout-based-id-all.csv'
            else:
                # Old file naming convention
                file_name = f'merged-detection-heatmap-coilcoils-{ct}-c{x}-id-all.csv'

            file_path = os.path.join(directory, file_name)
            try:
                coil_data[ct][x] = pd.read_csv(file_path)
                print(f"Loaded: {file_path}")
            except FileNotFoundError:
                print(f"File not found: {file_path}")

    # Initialize dictionaries to keep track of min and max differences
    min_differences = {
        # Standard comparisons
        'lvt_std': {'min_diff': None, 'file_name': ""},
        'lvt_hvt': {'min_diff': None, 'file_name': ""},
        'std_hvt': {'min_diff': None, 'file_name': ""},

        # Standard vs pinout comparisons
        'lvt_pinout-lvt': {'min_diff': None, 'file_name': ""},
        'std_pinout-std': {'min_diff': None, 'file_name': ""},
        'hvt_pinout-hvt': {'min_diff': None, 'file_name': ""},

        # Pinout vs pinout comparisons
        'pinout-lvt_pinout-std': {'min_diff': None, 'file_name': ""},
        'pinout-lvt_pinout-hvt': {'min_diff': None, 'file_name': ""},
        'pinout-std_pinout-hvt': {'min_diff': None, 'file_name': ""}
    }

    max_differences = {
        # Standard comparisons
        'lvt_std': {'max_diff': None, 'file_name': ""},
        'lvt_hvt': {'max_diff': None, 'file_name': ""},
        'std_hvt': {'max_diff': None, 'file_name': ""},

        # Standard vs pinout comparisons
        'lvt_pinout-lvt': {'max_diff': None, 'file_name': ""},
        'std_pinout-std': {'max_diff': None, 'file_name': ""},
        'hvt_pinout-hvt': {'max_diff': None, 'file_name': ""},

        # Pinout vs pinout comparisons
        'pinout-lvt_pinout-std': {'max_diff': None, 'file_name': ""},
        'pinout-lvt_pinout-hvt': {'max_diff': None, 'file_name': ""},
        'pinout-std_pinout-hvt': {'max_diff': None, 'file_name': ""}
    }

    # Function to compute differences between two coil types
    def compute_difference(ct1, ct2, x):
        # Skip hvt comparisons for x > 6
        if ((ct1 == 'hvt' or ct2 == 'hvt' or
             ct1 == 'pinout-hvt' or ct2 == 'pinout-hvt') and x > 6):
            return None
        else:
            if coil_data[ct1][x] is not None and coil_data[ct2][x] is not None:
                difference = coil_data[ct1][x]['value'] - coil_data[ct2][x]['value']
                difference_df = pd.DataFrame({
                    'x-idx': coil_data[ct1][x]['x-idx'],
                    'y-idx': coil_data[ct1][x]['y-idx'],
                    'value': difference
                })
                return difference_df
            else:
                print(f"Missing data for {ct1} or {ct2} at X={x}")
                return None

    # Compute differences for standard comparisons
    standard_differences = {
        'lvt_std': {x: compute_difference('lvt', 'std', x) for x in x_values},
        'lvt_hvt': {x: compute_difference('lvt', 'hvt', x) for x in x_values},
        'std_hvt': {x: compute_difference('std', 'hvt', x) for x in x_values}
    }

    # Compute differences for standard vs pinout comparisons
    standard_pinout_differences = {
        'lvt_pinout-lvt': {x: compute_difference('lvt', 'pinout-lvt', x) for x in x_values},
        'std_pinout-std': {x: compute_difference('std', 'pinout-std', x) for x in x_values},
        'hvt_pinout-hvt': {x: compute_difference('hvt', 'pinout-hvt', x) for x in x_values if x <= 6}
    }

    # Compute differences between pinout types
    pinout_differences = {
        'pinout-lvt_pinout-std': {x: compute_difference('pinout-lvt', 'pinout-std', x) for x in x_values},
        'pinout-lvt_pinout-hvt': {x: compute_difference('pinout-lvt', 'pinout-hvt', x) for x in x_values if x <= 6},
        'pinout-std_pinout-hvt': {x: compute_difference('pinout-std', 'pinout-hvt', x) for x in x_values if x <= 6}
    }

    # Combine all differences
    all_differences = {**standard_differences, **standard_pinout_differences, **pinout_differences}

    # Save all differences and track min/max
    for diff_type, diff_values in all_differences.items():
        for x, diff_df in diff_values.items():
            if diff_df is not None:
                output_file_path = os.path.join(output_dir, f'difference_{diff_type}_X{x}.csv')
                diff_df.to_csv(output_file_path, index=False)
                print(f"Saved differences for {diff_type} at X={x} to {output_file_path}")

                # Update min and max differences
                current_min_diff = diff_df['value'].min()
                current_max_diff = diff_df['value'].max()

                if min_differences[diff_type]['min_diff'] is None or current_min_diff < min_differences[diff_type]['min_diff']:
                    min_differences[diff_type]['min_diff'] = current_min_diff
                    min_differences[diff_type]['file_name'] = output_file_path

                if max_differences[diff_type]['max_diff'] is None or current_max_diff > max_differences[diff_type]['max_diff']:
                    max_differences[diff_type]['max_diff'] = current_max_diff
                    max_differences[diff_type]['file_name'] = output_file_path

    # Print summary of min and max differences
    print("\nSummary of Minimum Differences:")
    for diff_type in min_differences:
        if min_differences[diff_type]['min_diff'] is not None:
            print(f"{diff_type}: {min_differences[diff_type]['min_diff']} (in {min_differences[diff_type]['file_name']})")

    print("\nSummary of Maximum Differences:")
    for diff_type in max_differences:
        if max_differences[diff_type]['max_diff'] is not None:
            print(f"{diff_type}: {max_differences[diff_type]['max_diff']} (in {max_differences[diff_type]['file_name']})")

    return all_differences

# Rest of the script remains the same...
dirs2merge = [f'v{i}-10rep-1_1mx1_1mm' for i in range(3,6)]

coil_columns = [
    f'detection-heatmap-coilcoils-{CT}-c{X}-id-all.csv' for X in range(11) for CT in ['lvt', 'std', 'hvt']
] + [
    f'detection-heatmap-coilcoils-pinout-c{X}-{CT}-pinout-based-id-all.csv' for X in range(11) for CT in ['hvt', 'std', 'lvt']
]

max_values = {
    'lvt': {'max_value': 0, 'file_name': ""},
    'std': {'max_value': 0, 'file_name': ""},
    'hvt': {'max_value': 0, 'file_name': ""},
    'pinout-lvt': {'max_value': 0, 'file_name': ""},
    'pinout-std': {'max_value': 0, 'file_name': ""},
    'pinout-hvt': {'max_value': 0, 'file_name': ""}
}

max_values_over_all_positions = {
    'lvt': {'max_value': 0, 'file_name': ""},
    'std': {'max_value': 0, 'file_name': ""},
    'hvt': {'max_value': 0, 'file_name': ""},
    'pinout-lvt': {'max_value': 0, 'file_name': ""},
    'pinout-std': {'max_value': 0, 'file_name': ""},
    'pinout-hvt': {'max_value': 0, 'file_name': ""}
}

for file_name in set(coil_columns):
    category = None
    if 'lvt' in file_name:
        category = 'lvt' if not file_name.startswith('detection-heatmap-coilcoils-pinout') else 'pinout-lvt'
    elif 'std' in file_name:
        category = 'std' if not file_name.startswith('detection-heatmap-coilcoils-pinout') else 'pinout-std'
    elif 'hvt' in file_name:
        category = 'hvt' if not file_name.startswith('detection-heatmap-coilcoils-pinout') else 'pinout-hvt'

    if not category:
        continue

    dfs = []
    for directory in dirs2merge:
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            dfs.append(df)
        else:
            print(f"File not found: {file_path}")

    if dfs:
        combined_df = pd.concat(dfs)
        summed_df = combined_df.groupby(['x-idx', 'y-idx'], as_index=False)['value'].sum()
        summed_df = summed_df.sort_values(by=['y-idx', 'x-idx']).reset_index(drop=True)
        total_detections = summed_df['value'].sum()
        max_value = summed_df['value'].max()
        print(f"In {file_name} max value: {max_value}")
        print(f"In {file_name} sum of detections: {total_detections}")

        if max_value > max_values[category]['max_value']:
            max_values[category]['max_value'] = max_value
            max_values[category]['file_name'] = file_name

        if total_detections > max_values_over_all_positions[category]['max_value']:
            max_values_over_all_positions[category]['max_value'] = total_detections
            max_values_over_all_positions[category]['file_name'] = file_name

        output_file_name = f'merged-{file_name}'
        output_file_path = os.path.join('.', output_file_name)
        summed_df.to_csv(output_file_path, index=False)

print("Files merged and saved successfully.")

for category in max_values:
    print(f"{category}: {max_values[category]['file_name']}: {max_values[category]['max_value']}")
    print(f"{category} over all positions: {max_values_over_all_positions[category]['file_name']}: {max_values_over_all_positions[category]['max_value']}")

print("Compute differences...")
directory = '.'  # Replace with your directory path
differences = compute_and_save_coil_differences(directory, ".")
