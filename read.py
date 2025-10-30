import struct
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import re

# v3 = {'version' : 24}
acum_status_array = 16*[0]

def read_struct(fileContent, repetition_idx:int, struct_size:int, offset:int):
  measured = {}

  struct_idx = offset + (repetition_idx*struct_size)
  head = struct_idx

  print("Start reading at Byte:", head)

  # Read Position
  next = head+8
  x_cord = struct.unpack("d", fileContent[head:next])[0]
  measured["x-cord"] = x_cord

  head = next
  next = head+8
  y_cord = struct.unpack("d", fileContent[head:next])[0]
  measured["y-cord"] = y_cord

  head = next
  next = head+8
  z_cord = struct.unpack("d", fileContent[head:next])[0]
  measured["z-cord"] = z_cord

  # Read Position Index
  head = next
  next = head+4
  x_idx = struct.unpack("i", fileContent[head:next])[0]
  measured["x-idx"] = x_idx

  head = next
  next = head+4
  y_idx = struct.unpack("i", fileContent[head:next])[0]
  measured["y-idx"] = y_idx

  head = next
  next = head+4
  z_idx = struct.unpack("i", fileContent[head:next])[0]
  measured["z-idx"] = z_idx

  # Read Voltage Level
  head = next
  next = head+4
  voltage_level = struct.unpack("i", fileContent[head:next])[0]
  measured["v-level"] = voltage_level

  # Read Polarity
  head = next
  next = head+1
  polarity = struct.unpack("B", fileContent[head:next])[0]
  measured["polarity"] = polarity

  # Read Coil Type based on submitted Info
  head = next
  next = head+1
  coil_sel = struct.unpack("B", fileContent[head:next])[0]
  measured["coil-type-in"] = coil_sel

  # Read Plaintext based on submitted Info
  head = next
  next = head+16
  input = struct.unpack(16*"B", fileContent[head:next])
  input_hex = "0x"
  for i in input:
    input_hex +=  f"{i:02x}"
  measured["plain-in"] = input_hex
  print(measured["plain-in"])

  # Read Ciphertext
  head = next
  next = head+16
  cipher_output = struct.unpack(16*"B", fileContent[head:next])
  cipher_output_hex = "0x"
  for i in cipher_output:
    cipher_output_hex +=  f"{i:02x}"
  measured["ctxt"] = cipher_output_hex
  print(measured["ctxt"])

  # Read Plaintext based on received Info
  head = next
  next = head+16
  plain_output = struct.unpack(16*"B", fileContent[head:next])
  plain_output_hex = ""
  for i in plain_output:
    plain_output_hex = f"{i:02x}" + plain_output_hex
  plain_output_hex = "0x" + plain_output_hex
  measured["plain-out"] = plain_output_hex
  print(measured["plain-out"])

  # Read Status based on received Info
  head = next
  next = head+16
  status_output = struct.unpack(16*"B", fileContent[head:next])
  status_output_hex = []
  for i in status_output:
    status_output_hex.append(hex(i))

  for i in range(0,16):
    print(i, "\t", status_output_hex[i])
    acum_status_array[i] = acum_status_array[i] | status_output[i]
  print(acum_status_array)

  # coils_lvt = {}
  # coils_mvt = {}
  # coils_hvt = {}


  # M2_1,
  # M4_1,
  # M4_2,
  # M4_3,
  # M4_5,
  # M7_1,
  # M7_2,
  # M7_3,
  # M7_4,
  # M7_5,
  # M7_6,

  # measured["coils-lvt-c10"]= (status_output[0] & 0b10000000) >> 7
  # measured["coils-lvt-c9"] = (status_output[0] & 0b01000000) >> 6
  # measured["coils-lvt-c8"] = (status_output[0] & 0b00100000) >> 5
  # measured["coils-lvt-c7"] = (status_output[0] & 0b00010000) >> 4
  # measured["coils-lvt-c6"] = (status_output[0] & 0b00001000) >> 3
  # measured["coils-lvt-c5"] = (status_output[0] & 0b00000100) >> 2
  # measured["coils-lvt-c4"] = (status_output[0] & 0b00000010) >> 1
  # measured["coils-lvt-c3"] = (status_output[0] & 0b00000001) >> 0
  # measured["coils-lvt-c2"] = (status_output[1] & 0b10000000) >> 7
  # measured["coils-lvt-c1"] = (status_output[1] & 0b01000000) >> 6
  # measured["coils-lvt-c0"] = (status_output[1] & 0b00100000) >> 5

  # measured["coils-std-c6"] = (status_output[1] & 0b00000001) >> 0
  # measured["coils-std-c5"] = (status_output[2] & 0b10000000) >> 7
  # measured["coils-std-c4"] = (status_output[2] & 0b01000000) >> 6
  # measured["coils-std-c3"] = (status_output[2] & 0b00100000) >> 5
  # measured["coils-std-c2"] = (status_output[2] & 0b00010000) >> 4
  # measured["coils-std-c1"] = (status_output[2] & 0b00001000) >> 3
  # measured["coils-std-c0"] = (status_output[2] & 0b00000100) >> 2
  # measured["coils-std-c10"]= (status_output[1] & 0b00010000) >> 4
  # measured["coils-std-c9"] = (status_output[1] & 0b00001000) >> 3
  # measured["coils-std-c8"] = (status_output[1] & 0b00000100) >> 2
  # measured["coils-std-c7"] = (status_output[1] & 0b00000010) >> 1

  # measured["coils-hvt-c10"]= (status_output[2] & 0b00000010) >> 1
  # measured["coils-hvt-c9"] = (status_output[2] & 0b00000001) >> 0
  # measured["coils-hvt-c8"] = (status_output[3] & 0b10000000) >> 7
  # measured["coils-hvt-c7"] = (status_output[3] & 0b01000000) >> 6
  # measured["coils-hvt-c6"] = (status_output[3] & 0b00100000) >> 5
  # measured["coils-hvt-c5"] = (status_output[3] & 0b00010000) >> 4
  # measured["coils-hvt-c4"] = (status_output[3] & 0b00001000) >> 3
  # measured["coils-hvt-c3"] = (status_output[3] & 0b00000100) >> 2
  # measured["coils-hvt-c2"] = (status_output[3] & 0b00000010) >> 1
  # measured["coils-hvt-c1"] = (status_output[3] & 0b00000001) >> 0
  # measured["coils-hvt-c0"] = (status_output[4] & 0b10000000) >> 7

# reg (original): |c10|c9|c8|c7|c6|c5|c4|c3 | c2|c1|c0
#
# reg (correct) : | c6|c5|c4|c3|c2|c1|c0|c10| c9|c8|c7


  measured["coils-lvt-c6"] = (status_output[0] >> 7) & 0b1
  measured["coils-lvt-c5"] = (status_output[0] >> 6) & 0b1
  measured["coils-lvt-c4"] = (status_output[0] >> 5) & 0b1
  measured["coils-lvt-c3"] = (status_output[0] >> 4) & 0b1
  measured["coils-lvt-c2"] = (status_output[0] >> 3) & 0b1
  measured["coils-lvt-c1"] = (status_output[0] >> 2) & 0b1
  measured["coils-lvt-c0"] = (status_output[0] >> 1) & 0b1
  measured["coils-lvt-c10"]= (status_output[0] >> 0) & 0b1
  measured["coils-lvt-c9"] = (status_output[1] >> 7) & 0b1
  measured["coils-lvt-c8"] = (status_output[1] >> 6) & 0b1
  measured["coils-lvt-c7"] = (status_output[1] >> 5) & 0b1

  measured["coils-std-c6"] = (status_output[1] >> 4) & 0b1
  measured["coils-std-c5"] = (status_output[1] >> 3) & 0b1
  measured["coils-std-c4"] = (status_output[1] >> 2) & 0b1
  measured["coils-std-c3"] = (status_output[1] >> 1) & 0b1
  measured["coils-std-c2"] = (status_output[1] >> 0) & 0b1
  measured["coils-std-c1"] = (status_output[2] >> 7) & 0b1
  measured["coils-std-c0"] = (status_output[2] >> 6) & 0b1
  measured["coils-std-c10"]= (status_output[2] >> 5) & 0b1
  measured["coils-std-c9"] = (status_output[2] >> 4) & 0b1
  measured["coils-std-c8"] = (status_output[2] >> 3) & 0b1
  measured["coils-std-c7"] = (status_output[2] >> 2) & 0b1

  measured["coils-hvt-c6"] = (status_output[2] >> 1) & 0b1
  measured["coils-hvt-c5"] = (status_output[2] >> 0) & 0b1
  measured["coils-hvt-c4"] = (status_output[3] >> 7) & 0b1
  measured["coils-hvt-c3"] = (status_output[3] >> 6) & 0b1
  measured["coils-hvt-c2"] = (status_output[3] >> 5) & 0b1
  measured["coils-hvt-c1"] = (status_output[3] >> 4) & 0b1
  measured["coils-hvt-c0"] = (status_output[3] >> 3) & 0b1
  measured["coils-hvt-c10"]= (status_output[3] >> 2) & 0b1
  measured["coils-hvt-c9"] = (status_output[3] >> 1) & 0b1
  measured["coils-hvt-c8"] = (status_output[3] >> 0) & 0b1
  measured["coils-hvt-c7"] = (status_output[4] >> 7) & 0b1

  for i in range(0,7):
    if (status_output[4] >> i) & 0x1 == 1:
      print(f"At bit position {i} in byte 4 an unexpected 1 was found")
      return -1
  # coils = {}
  # coils["hvt"] = coils_hvt
  # coils["mvt"] = coils_mvt
  # coils["lvt"] = coils_lvt
  # measured["coils"] = coils

  measured["coil-type-out"] = status_output[8]

  version = status_output[10] >> 3
  measured["version"]   = version

  # The Pinout is exposed through Byte 10 and 11.
  # Byte 11 is solely related to coils, while only 3 bit (the lsb) of Byte 10
  # are related to the coils.
  # coils_pinout = {}
  measured["coils-pinout-c10"]= (status_output[10] & 0b00000100) >> 2
  measured["coils-pinout-c9"] = (status_output[10] & 0b00000010) >> 1
  measured["coils-pinout-c8"] = (status_output[10] & 0b00000001) >> 0
  measured["coils-pinout-c7"] = (status_output[11] & 0b10000000) >> 7
  measured["coils-pinout-c6"] = (status_output[11] & 0b01000000) >> 6
  measured["coils-pinout-c5"] = (status_output[11] & 0b00100000) >> 5
  measured["coils-pinout-c4"] = (status_output[11] & 0b00010000) >> 4
  measured["coils-pinout-c3"] = (status_output[11] & 0b00001000) >> 3
  measured["coils-pinout-c2"] = (status_output[11] & 0b00000100) >> 2
  measured["coils-pinout-c1"] = (status_output[11] & 0b00000010) >> 1
  measured["coils-pinout-c0"] = (status_output[11] & 0b00000001) >> 0
  # measured["coils-pout"] = coils_pinout

  measured["check-sum"] = (status_output[12] << 16) | (status_output[13] << 8) | status_output[14]
  # print("Check sum: ", hex(measured["check-sum"]>>3)) # must be shifted for 1co5ef
  measured["timeout"] = status_output[15]




  head = next
  next = head+2
  # NOTE: Why do I have here pinout again?
  # Do I process it in c++ already?
  # NOTE: For now I am going to ignore that
  coil_pinout = struct.unpack("BB", fileContent[head:next])
  coil_pinout_hex = [coil_pinout[1], coil_pinout[0]]

  head = next
  next = head+1
  hasResponse = struct.unpack("B", fileContent[head:next])[0]
  measured["has-response"] = hasResponse

  # I think this is the place holder for the number of entries in a file thing
  # which is only used once per file in the beginning.
  # head = next
  # next = head+3
  # padding = struct.unpack(3*"B", fileContent[head:next])
  DEBUG=0
  if DEBUG==1:
    print("\nX Position: ", x_cord)
    print("y Position: ", y_cord)
    print("z Position: ", z_cord)
    print("X Idx: ", x_idx)
    print("y Idy: ", y_idx)
    print("z Idz: ", z_idx)
    print("Voltage Level: ", voltage_level)
    print("Polarity: ", polarity)
    print("Input: " , input)
    print("hex(Input): " , input_hex)
    print("cipher_output: " , cipher_output)
    print("hex(cipher_output): " , cipher_output_hex)
    print("plain_output: " , plain_output)
    print("hex(plain_output): " , plain_output_hex)
    print("status_output: " , status_output)
    print("hex(status_output): " , status_output_hex)
    print("coil_pinout:", coil_pinout)
    print("coil_pinout_hex :", coil_pinout_hex)
    print("Was response received (0:Yes, -1:No): ", hasResponse)
    print(measured)
  return measured


def read_all_structs_in_file(start_byte_idx:int, struct_size:int,
                             num_measurments, low_jitter_delay ,fileContent):
  measurments = []
  for i in range(0,num_measurments):
    print("\n")
    measured = read_struct(fileContent, i, struct_size, start_byte_idx)
    measured["rep-idx"] = i
    measured["low-jitter-delay"] = low_jitter_delay
    measurments.append(measured)
    print("\n")
  return measurments

def process_file(file_path):
    with open(file_path, mode='rb') as file:
        fileContent = file.read()

 # Extract the number after "LJD" and before ".dat" from the file_path
    pattern = re.compile(r"LJD(\d+)\.dat")
    match = pattern.search(file_path)
    low_jitter_delay = 0
    if match:
        low_jitter_delay = match.group(1)
        print(f"Extracted LJD number from file {file_path}: {low_jitter_delay }")
    else:
        print(f"No LJD number found in file {file_path}")

    num_measurments = struct.unpack("i", fileContent[:4])[0]
    print(f"Number of measurements in file {file_path}: {num_measurments}")

    start_byte_idx = 4
    struct_size = 0x70
    print("\n\n\n")
    measurements = read_all_structs_in_file(start_byte_idx, struct_size,
                                            num_measurments, low_jitter_delay, fileContent)
    print("\n\n\n")
    return measurements

def process_directory(root_dir):
    all_measurements = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.dat'):  # Check if the file is a .dat file
                file_path = os.path.join(dirpath, filename)
                print("Parsing ", file_path)
                measurements = process_file(file_path)
                all_measurements.extend(measurements)
    return all_measurements

def invert_x_idx(max_x_idx, x_idx):
    return max_x_idx - x_idx

# Function to perform XOR operation
def xor_binary_strings(binary_str1, binary_str2):
    # Convert binary strings to integers
    int1 = int(binary_str1, 2)
    int2 = int(binary_str2, 2)

    # Perform XOR
    xor_result = int1 ^ int2

    # Convert the result back to a binary string, removing the '0b' prefix
    return bin(xor_result)[2:].zfill(max(len(binary_str1), len(binary_str2)))

def check_detection_reg(row):
  columns_to_check = [
      'coils-hvt-c10', 'coils-hvt-c9', 'coils-hvt-c8', 'coils-hvt-c7',
      'coils-hvt-c6', 'coils-hvt-c5', 'coils-hvt-c4', 'coils-hvt-c3',
      'coils-hvt-c2', 'coils-hvt-c1', 'coils-hvt-c0', 'coils-std-c10',
      'coils-std-c9', 'coils-std-c8', 'coils-std-c7', 'coils-std-c6',
      'coils-std-c5', 'coils-std-c4', 'coils-std-c3', 'coils-std-c2',
      'coils-std-c1', 'coils-std-c0', 'coils-lvt-c10', 'coils-lvt-c9',
      'coils-lvt-c8', 'coils-lvt-c7', 'coils-lvt-c6', 'coils-lvt-c5',
      'coils-lvt-c4', 'coils-lvt-c3', 'coils-lvt-c2', 'coils-lvt-c1',
      'coils-lvt-c0'
  ]
  if any(row[col] == 1 for col in columns_to_check):
      return "Detected"
  else:
      return "Undetected"

def check_detection_pin(row):
  columns_to_check = [
    'coils-pinout-c10', 'coils-pinout-c9', 'coils-pinout-c8',
    'coils-pinout-c7' , 'coils-pinout-c6', 'coils-pinout-c5',
    'coils-pinout-c4' , 'coils-pinout-c3', 'coils-pinout-c2',
    'coils-pinout-c1' , 'coils-pinout-c0'
  ]
  if any(row[col] == 1 for col in columns_to_check):
      return "Detected"
  else:
      return "Undetected"

def detect_corrupted_plaintext_register(df:pd.DataFrame):
  print("Checking if a plaintext was corrupted in the input register...")
  df['ptx-corrupted'] = np.where(df['plain-in'] == df['plain-out'], 0, 1)

def detect_faulted_ciphertext_computetation(df:pd.DataFrame):
  print("Checking if encryption was corrupted...")
  df['ctx-computation-faulted'] = np.where(df['ctxt'] ==
                                   "0x3925841d02dc09fbdc118597196a0b32",
                                   0, 1)

def detect_if_coils_observed_emfi(df:pd.DataFrame):
  print("Checking if coils detected emfi...")

  df['coil-reg-detection'] = df.apply(check_detection_reg, axis=1)
  df['coil-pin-detection'] = df.apply(check_detection_pin, axis=1)


def preprocessing(df:pd.DataFrame, clean, results_dir, experiment_directory):
  preprocessed_df_cache_file = results_dir +'/'+experiment_directory + '/' +'dataframe_preprocessed'

  if not clean:
    try:
      cached = os.path.exists(preprocessed_df_cache_file  + ".parquet")
      cached = cached and os.path.exists(preprocessed_df_cache_file  + ".csv")

      if cached:
        print("[*] Reading preprocessed data frame...")
        df = pd.read_parquet(preprocessed_df_cache_file+ ".parquet", engine='pyarrow')
      else:
        clean = True


    except Exception as e:
      print(f"Error reading cache files: {e}")
      clean = True  # Force recomputation if reading fails

  if clean:

    print("Invert x-idx for y-idx%2==1 ...")
    max_x_idx = df['x-idx'].max()
    max_y_idx = df['y-idx'].max()
    df.loc[df['y-idx'] % 2 == 1, 'x-idx'] = df.loc[df['y-idx'] % 2 == 1, 'x-idx'].apply(lambda x: invert_x_idx(max_x_idx,x))

    print("Rotate ...")
    df['x-idx'] = max_x_idx - df['x-idx']
    df['y-idx'] = max_y_idx - df['y-idx']

    detect_corrupted_plaintext_register(df)
    detect_faulted_ciphertext_computetation(df)
    detect_if_coils_observed_emfi(df)

  print("[*] Writing preprocessed data frame...")
  df.to_csv(preprocessed_df_cache_file+ ".csv")
  df.to_parquet(preprocessed_df_cache_file+ ".parquet", engine='pyarrow')

  print("The keys of preprocessed dataframe are:")
  keys = df.columns
  print(keys)
  print("\n")

  return df


def get_number_of_corrupted_plaintext(df:pd.DataFrame):
  number_of_corrupterd_plaintext = df['ptx-corrupted'].sum()
  print(f"Number of faulted input registers: {number_of_corrupterd_plaintext}\n")
  return number_of_corrupterd_plaintext


def get_number_of_corrupted_ciphertext(df:pd.DataFrame):
  number_of_corrupted_encryptions = df['ctx-computation-faulted'].sum()
  print(f"Number of faulted encryptions: {number_of_corrupted_encryptions}\n")
  return number_of_corrupted_encryptions


def get_number_of_coil_detections(df:pd.DataFrame):
  detection_reg_count = df['coil-reg-detection'].value_counts().get('Detected', 0)
  print("Coil emfi observation count (reg): ", detection_reg_count)
  detection_pin_count = df['coil-pin-detection'].value_counts().get('Detected', 0)
  print("Coil emfi observation count (pin): ", detection_pin_count)
  return detection_reg_count, detection_pin_count

def get_number_of_measurments(df:pd.DataFrame, measurment_type=""):
  print("[*] Counting number of measurments" + measurment_type +"...")
  num_measurments = df.shape[0]
  print("[+] Count: ", num_measurments)
  return num_measurments

def get_number_of_measurments_per_position(df:pd.DataFrame):
  print("Computing the number of measurments per position...")
  pair_counts = df.groupby(['x-idx', 'y-idx']).size().reset_index(name='count')
  most_common_count = pair_counts['count'].mode()
  num_diff_counts = len(most_common_count)
  print("Measurments per position: ")
  print(f"{most_common_count[0]} (num dif counts {num_diff_counts})")

  return most_common_count[0]


def add_kosef_indicator_to_heatmap(plt, heatmap_data):
  # Add the "KOSEF" indicator
  rotation_angle = 0
  plt.text(x=heatmap_data.columns.max() + 1, y=heatmap_data.index.max()+1 ,
           s='KOSEF', rotation=rotation_angle, fontsize=12, color='black')


def compute_voltage_vs_effective_faults_and_timeout_plot(df:pd.DataFrame, export_table:bool):
  print("Computing count of effective faults per voltage level...")
  grouped = df.groupby(['v-level'])['ctx-computation-faulted'].sum().reset_index()
  grouped_timeout = df.groupby(['v-level'])['timeout'].sum().reset_index()
  grouped.merge(grouped_timeout, on='v-level', how='left')
  grouped["ratio"] = grouped['ctx-computation-faulted'] / grouped_timeout['timeout']
  if(export_table):
    print(grouped)

  plt.figure(figsize=(12, 6))
  plt.plot(grouped['v-level'], grouped['ctx-computation-faulted'], marker='o', linestyle='-')
  plt.title('Plot of ctx-computation-faulted vs v-level')
  plt.xlabel('Voltage EM Emitter')
  plt.ylabel('Effective Fault Count')
  plt.grid(True)
  # plt.show()


def compute_low_jitter_delay_vs_faults_effective_and_timeout_plot(df:pd.DataFrame, export_table:bool):
  print("Computing count of effective fault per low jitter delay...")
  grouped_effective_faults = df.groupby(['low-jitter-delay'])['ctx-computation-faulted'].sum().reset_index()
  grouped_timeout = df.groupby(['low-jitter-delay'])['timeout'].sum().reset_index()
  grouped = grouped_effective_faults.merge(grouped_timeout,on='low-jitter-delay')
  grouped["ratio"] = grouped['timeout'] / grouped['ctx-computation-faulted']
  if(export_table):
    print(grouped)

  plt.figure(figsize=(12, 6))
  plt.plot(grouped_effective_faults['low-jitter-delay'], grouped_effective_faults['ctx-computation-faulted'], marker='o', linestyle='-')
  plt.xlabel('Low Jitter Delay [ns]')
  plt.ylabel('Effective Fault Count')
  plt.grid(True)
  # plt.show()


def compute_coordinates_detection_heatmap(df:pd.DataFrame, coil:str, export_dir,
                                          id="", clean=False):
  heatmap_data = None
  filename = f'detection-heatmap-coil{coil}-id-{id}'
  csv_filename = os.path.join(export_dir, f'{filename}.csv')
  parquet_filename = os.path.join(export_dir, f'{filename}.parquet')

  clean = clean or not os.path.exists(csv_filename)
  clean = clean or not os.path.exists(parquet_filename)

  if clean:
    print("Computing coordinates-detection-heatmap-" + coil + "...")
    grouped = df.groupby(['x-idx', 'y-idx'])[coil].sum().reset_index()
    heatmap_data = grouped.pivot(index='y-idx', columns='x-idx', values=coil).fillna(0)


    wide_df = heatmap_data.reset_index().melt(id_vars='y-idx',
                                              var_name='x-idx',
                                              value_name='value')
    wide_df = wide_df[['x-idx', 'y-idx', 'value']]
    wide_df = wide_df.sort_values(by=['y-idx','x-idx'])

    wide_df.to_csv(csv_filename, index=False)
    heatmap_data.to_parquet(parquet_filename)
    print(f"Exported data for {id} to {csv_filename} and {parquet_filename}")

  else:
    heatmap_data = pd.read_parquet(parquet_filename, engine='pyarrow')


 # Calculate total accumulation
  total_accumulation = heatmap_data.sum().sum()
  print(f"{coil} has reacted: {total_accumulation} times")

  plt.figure(figsize=(10, 10))
  sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='viridis')

  add_kosef_indicator_to_heatmap(plt, heatmap_data)


  plt.title('Heatmap of Detecting Faults ' + coil)
  plt.xlabel('X Coordinate')
  plt.ylabel('Y Coordinate')
  # plt.show()

  return heatmap_data


def compute_coordinates_detection_heatmap_pinout_based(df:pd.DataFrame,
                                                      type_:str,
                                                      coil:str,
                                                      export_dir,
                                                      id="", clean=False):
  heatmap_data = None
  filename = f'detection-heatmap-coil{coil}-{type_}-pinout-based-id-{id}'
  csv_filename = os.path.join(export_dir, f'{filename}.csv')
  parquet_filename = os.path.join(export_dir, f'{filename}.parquet')

  clean = clean or not os.path.exists(csv_filename)
  clean = clean or not os.path.exists(parquet_filename)

  if clean:
    print("Computing coordinates-detection-heatmap-pinout-based" + coil + "...")
    cell_type = None

    # HVT = 0,
    # SVT = 1,
    # LVT = 2
    if type_ == 'lvt':
      cell_type = 2
    elif type_ == 'std':
      cell_type = 1
    elif type_ == 'hvt':
      cell_type = 0
    else:
      print("Wrong cell type")
      exit(-1)

    df_filtered_by_cell_type = df.loc[df['coil-type-in'] == cell_type]
    grouped = df_filtered_by_cell_type.groupby(['x-idx', 'y-idx'])[coil].sum().reset_index()
    heatmap_data = grouped.pivot(index='y-idx', columns='x-idx', values=coil).fillna(0)


    wide_df = heatmap_data.reset_index().melt(id_vars='y-idx',
                                              var_name='x-idx',
                                              value_name='value')
    wide_df = wide_df[['x-idx', 'y-idx', 'value']]
    wide_df = wide_df.sort_values(by=['y-idx','x-idx'])

    wide_df.to_csv(csv_filename, index=False)
    heatmap_data.to_parquet(parquet_filename)
    print(f"Exported data for {id} to {csv_filename} and {parquet_filename}")

  else:
    heatmap_data = pd.read_parquet(parquet_filename, engine='pyarrow')


 # Calculate total accumulation
  total_accumulation = heatmap_data.sum().sum()
  print(f"{coil} has reacted: {total_accumulation} times")

  plt.figure(figsize=(10, 10))
  sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='viridis')

  add_kosef_indicator_to_heatmap(plt, heatmap_data)


  plt.title('Heatmap of Detecting Faults ' + coil + type_)
  plt.xlabel('X Coordinate')
  plt.ylabel('Y Coordinate')
  # plt.show()

  return heatmap_data







def compute_coordinates_effective_faults_heatmap(df: pd.DataFrame, export_dir, id="", clean=False):
    heatmap_data = None
    filename = f'effective-fault-heatmap-id-{id}'
    csv_filename = os.path.join(export_dir, f'{filename}.csv')
    parquet_filename = os.path.join(export_dir, f'{filename}.parquet')

    clean = clean or not os.path.exists(csv_filename)
    clean = clean or not os.path.exists(parquet_filename)

    if clean:
        print("Computing coordinates-effective-faults-heatmap-" + id + "...")
        grouped = df.groupby(['x-idx', 'y-idx'])['ctx-computation-faulted'].sum().reset_index()
        heatmap_data = grouped.pivot(index='y-idx', columns='x-idx', values='ctx-computation-faulted').fillna(0)

        # Determine the complete range of x and y indices
        x_idx_range = range(grouped['x-idx'].min(), grouped['x-idx'].max() + 1)
        y_idx_range = range(grouped['y-idx'].min(), grouped['y-idx'].max() + 1)

        print(heatmap_data)
        heatmap_data = heatmap_data.reindex(index=y_idx_range, columns=x_idx_range, fill_value=0)
        print(heatmap_data)

        wide_df = heatmap_data.reset_index().melt(id_vars='y-idx', var_name='x-idx', value_name='value')
        wide_df = wide_df[['x-idx', 'y-idx', 'value']]
        wide_df = wide_df.sort_values(by=['y-idx', 'x-idx'])
        wide_df.to_csv(csv_filename, index=False)
        heatmap_data.to_parquet(parquet_filename)
        print(f"Exported data for {id} to {csv_filename} and {parquet_filename}")
    else:
        heatmap_data = pd.read_parquet(parquet_filename, engine='pyarrow')

    plt.figure(figsize=(10, 10))
    sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='viridis')
    plt.title('Heatmap of Effective Faults in the Ciphertext ' + id)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()



def compute_coordinates_timeout_heatmap(df:pd.DataFrame,
                                        export_dir,
                                        id="",
                                        clean=False):

  heatmap_data = None
  filename = f'timeout-heatmap-id-{id}'
  csv_filename = os.path.join(export_dir, f'{filename}.csv')
  parquet_filename = os.path.join(export_dir, f'{filename}.parquet')

  clean = clean or not os.path.exists(csv_filename)
  clean = clean or not os.path.exists(parquet_filename)

  if clean:
    print("Computing coordinates-timeouts-heatmap...")
    grouped = df.groupby(['x-idx', 'y-idx'])['timeout'].sum().reset_index()
    heatmap_data = grouped.pivot(index='y-idx', columns='x-idx', values='timeout').fillna(0)

    wide_df = heatmap_data.reset_index().melt(id_vars='y-idx', var_name='x-idx', value_name='value')

    wide_df = wide_df[['x-idx', 'y-idx', 'value']]
    wide_df = wide_df.sort_values(by=['y-idx','x-idx'])

    wide_df.to_csv(csv_filename, index=False)
    heatmap_data.to_parquet(parquet_filename)
    print(f"Exported data for {id} to {csv_filename} and {parquet_filename}")

  else:
    heatmap_data = pd.read_parquet(parquet_filename, engine='pyarrow')

  plt.figure(figsize=(10, 10))
  sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='viridis')

  add_kosef_indicator_to_heatmap(plt, heatmap_data)

  plt.title('Heatmap of Timeouts')
  plt.xlabel('X Coordinate')
  plt.ylabel('Y Coordinate')
  plt.show()


def compute_coordinates_effective_faults_timeout_ratio_heatmap(df:pd.DataFrame):
  print("Computing coordinates-effective-faults-timeout-ratio-heatmap...")
  # Group by x-idx and y-idx and sum both columns at once
  grouped = df.groupby(['x-idx', 'y-idx']).agg({
      'ctx-computation-faulted': 'sum',
      'timeout': 'sum'
  }).reset_index()


  # Compute the ratio
  grouped["q"] = grouped['ctx-computation-faulted'] / grouped['timeout']

  # Fill NaN values (which occur when ctx-computation-faulted is 0)
  grouped["q"] = grouped["q"].fillna(0)

  # Find the maximum 'q' excluding infinity
  max_q = grouped["q"][~np.isinf(grouped["q"])].max()
  max_q_value = max_q.item() if pd.notna(max_q) else 0
  print(f"The maximum 'q' excluding infinity is: {max_q}")

  heatmap_data = grouped.pivot(index='y-idx', columns='x-idx', values='q').fillna(0)

  vmin = 0
  vmax = max_q_value
  plt.figure(figsize=(10, 10))
  sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='viridis', vmin=vmin,
              vmax=vmax)
  plt.title('Heatmap of Effective Faults / Timeout Ratio for Coordinates')
  plt.xlabel('X Coordinate')
  plt.ylabel('Y Coordinate')
  # plt.show()


def compute_voltage_low_jitter_delay_effective_faults_timeout_ratio_heatmap(df:pd.DataFrame):
  print("Computing voltage-low-jitter-delay-effective-faults-timeout-ratio-heatmap...")
  # Group by x-idx and y-idx and sum both columns at once
  grouped = df.groupby(['v-level', 'low-jitter-delay']).agg({
      'ctx-computation-faulted': 'sum',
      'timeout': 'sum'
  }).reset_index()


  # Compute the ratio
  grouped["q"] = grouped['ctx-computation-faulted'] / grouped['timeout']

  # Fill NaN values (which occur when ctx-computation-faulted is 0)
  grouped["q"] = grouped["q"].fillna(0)

  heatmap_data = grouped.pivot(index='v-level', columns='low-jitter-delay', values='q').fillna(0)

  vmin = 0
  vmax = 50
  plt.figure(figsize=(10, 10))
  sns.heatmap(heatmap_data, annot=True, fmt='g',
              cmap='viridis',vmin=vmin,vmax=vmax)
  plt.title('Heatmap of Effective Faults / Timeout Ratio for Voltage and Low Jitter Delay')
  plt.xlabel('Low Jitter Delay')
  plt.ylabel('Voltage')
  # plt.show()


def compute_voltage_low_jitter_delay_effective_faults_heatmap(df:pd.DataFrame,
                                                              export_dir,
                                                              id="",
                                                              clean=False):

  filename = f'voltage-vs-low-jitter-delay-effective-faults-heatmap-{id}'
  csv_filename = os.path.join(export_dir, f'{filename}.csv')
  parquet_filename = os.path.join(export_dir, f'{filename}-.parquet')

  clean = clean or not os.path.exists(csv_filename)
  clean = clean or not os.path.exists(parquet_filename)

  if clean:
    print("Computing voltage-low-jitter-effective-faults-heatmap"+id+"...")
    grouped = df.groupby(['v-level', 'low-jitter-delay'])['ctx-computation-faulted'].sum().reset_index()
    heatmap_data = grouped.pivot(index='v-level', columns='low-jitter-delay', values='ctx-computation-faulted').fillna(0)

    x_idx_range = [15,20,25,30,35]
    y_idx_range = range(50,510,10)
    heatmap_data.columns = heatmap_data.columns.astype(int)

    print(heatmap_data)
    heatmap_data = heatmap_data.reindex(index=y_idx_range, columns=x_idx_range, fill_value=0)
    print(heatmap_data)

    wide_df = heatmap_data.reset_index().melt(id_vars='v-level', var_name='low-jitter-delay', value_name='value')
    wide_df = wide_df[['v-level', 'low-jitter-delay', 'value']]
    wide_df = wide_df.sort_values(by=['low-jitter-delay','v-level'])
    wide_df.to_csv(csv_filename, index=False)

    heatmap_data.to_parquet(parquet_filename)
    print(f"Exported data for {id} to {csv_filename} and {parquet_filename}")

  else:
    heatmap_data = pd.read_parquet(parquet_filename, engine='pyarrow')

  plt.figure(figsize=(10, 10))
  sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='viridis')
  plt.title('Heatmap of Effective Faults in the Ciphertext ' + id)
  plt.xlabel('Low Jiiter Delay')
  plt.ylabel('Voltage')
  plt.show()

def compute_voltage_low_jitter_delay_timeout_heatmap(df: pd.DataFrame, export_dir, id="", clean=False):
    filename = f'voltage-vs-low-jitter-delay-timeout-heatmap-{id}'
    csv_filename = os.path.join(export_dir, f'{filename}.csv')
    parquet_filename = os.path.join(export_dir, f'{filename}.parquet')

    clean = clean or not os.path.exists(csv_filename)
    clean = clean or not os.path.exists(parquet_filename)

    if clean:
        print("Computing voltage-low-jitter-timeouts-heatmap...")
        grouped = df.groupby(['v-level', 'low-jitter-delay'])['timeout'].sum().reset_index()
        heatmap_data = grouped.pivot(index='v-level', columns='low-jitter-delay', values='timeout').fillna(0)

        # Define the complete range of indices
        v_level_range = range(50, 501, 10)  # From 50 to 500 in steps of 10
        low_jitter_delay_range = [15, 20, 25, 30, 35]

        # Reindex the heatmap_data to include all combinations of v-level and low-jitter-delay indices
        heatmap_data = heatmap_data.reindex(index=v_level_range, columns=low_jitter_delay_range, fill_value=0)

        wide_df = heatmap_data.reset_index().melt(id_vars='v-level', var_name='low-jitter-delay', value_name='value')
        wide_df.to_csv(csv_filename, index=False)
        heatmap_data.to_parquet(parquet_filename)
        print(f"Exported data for {id} to {csv_filename} and {parquet_filename}")
    else:
        heatmap_data = pd.read_parquet(parquet_filename, engine='pyarrow')

    plt.figure(figsize=(10, 10))
    sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='viridis')
    plt.title('Heatmap of Timeouts')
    plt.xlabel('Low Jitter Delay')
    plt.ylabel('Voltage')
    # plt.show()


def compute_no_detection_reg_but_effective_fault_cases(df:pd.DataFrame,
                                                       export_dir, id="",
                                                       log=False, clean=False):

  undetected_effective_faults = None
  filename = f'effective-fault-and-no-detection-by-reg-{id}'
  csv_filename = os.path.join(export_dir, f'{filename}.csv')
  parquet_filename = os.path.join(export_dir, f'{filename}-.parquet')

  clean = clean or not os.path.exists(csv_filename)
  clean = clean or not os.path.exists(parquet_filename)

  if clean:
    print("Computing undetected effective faults (reg) ...")
    undetected_effective_faults = df.loc[(df['ctx-computation-faulted'] == 1) & (df['coil-reg-detection'] != 'Detected')]

    undetected_effective_faults.to_csv(csv_filename)
    undetected_effective_faults.to_parquet(parquet_filename)

  else:
    print("Reading undetected effective faults (reg) ...")
    undetected_effective_faults = pd.read_parquet(parquet_filename, engine='pyarrow')

  if log:
    print(undetected_effective_faults)

  return undetected_effective_faults;


def compute_no_detection_pin_but_effective_fault_cases(df:pd.DataFrame,
                                                       export_dir, id="",
                                                       log=False, clean=False):

  undetected_effective_faults = None
  filename = f'effective-fault-and-no-detection-by-pin-{id}'
  csv_filename = os.path.join(export_dir, f'{filename}.csv')
  parquet_filename = os.path.join(export_dir, f'{filename}.parquet')

  clean = clean or not os.path.exists(csv_filename)
  clean = clean or not os.path.exists(parquet_filename)

  if clean:
    print("Computing undetected effective faults (pin) ...")
    undetected_effective_faults = df.loc[(df['ctx-computation-faulted'] == 1) & (df['coil-pin-detection'] != 'Detected')]

    undetected_effective_faults.to_csv(csv_filename)
    undetected_effective_faults.to_parquet(parquet_filename)

  else:
    print("Reading undetected effective faults (pin) ...")
    undetected_effective_faults = pd.read_parquet(parquet_filename, engine='pyarrow')

  if log:
    print(undetected_effective_faults)

  return undetected_effective_faults;


def compute_pin_and_reg_no_detection_but_effective_fault_cases(df:pd.DataFrame,
                                                               export_dir,
                                                               id="",
                                                               log=False,
                                                               clean=False):
  undetected_effective_faults = None
  filename = f'effective-fault-and-no-detection-{id}'
  csv_filename = os.path.join(export_dir, f'{filename}.csv')
  parquet_filename = os.path.join(export_dir, f'{filename}.parquet')

  clean = clean or not os.path.exists(csv_filename)
  clean = clean or not os.path.exists(parquet_filename)

  if clean:
    print("Computing undetected effective faults (all) ...")
    undetected_effective_faults = df.loc[(df['ctx-computation-faulted'] == 1) &
    ((df['coil-pin-detection'] != 'Detected') & (df['coil-reg-detection'] != 'Detected'))]

    undetected_effective_faults.to_csv(csv_filename)
    undetected_effective_faults.to_parquet(parquet_filename)

  else:
    print("Reading undetected effective faults (all) ...")
    undetected_effective_faults = pd.read_parquet(parquet_filename, engine='pyarrow')

  if log:
    print(undetected_effective_faults)

  return undetected_effective_faults;


def filter_df_no_timeout(df:pd.DataFrame,
                          export_dir,
                          id="",
                          clean=False):

  filename = f'no-timeout-filtered-{id}'
  csv_filename = os.path.join(export_dir, f'{filename}.csv')
  parquet_filename = os.path.join(export_dir, f'{filename}.parquet')

  clean = clean or not os.path.exists(csv_filename)
  clean = clean or not os.path.exists(parquet_filename)

  if clean:
    no_timeouts_df = df.loc[df['timeout'] != 1]
    no_timeouts_df.to_csv(csv_filename)
    no_timeouts_df.to_parquet(parquet_filename)

  else:
    no_timeouts_df = pd.read_parquet(parquet_filename, engine='pyarrow')

  return no_timeouts_df

def compute_parameters_with_most_effetive_faults(df:pd.DataFrame,
                                                 id="",
                                                 log=False):
  print("Computing parameters with most effective faults " +id+" ...")
  # Group by the specified columns and sum the 'ctx-computation-faulted' column
  result = df.groupby(['x-idx', 'y-idx', 'v-level', 'low-jitter-delay', 'polarity'], as_index=False)['ctx-computation-faulted'].sum()

  result_sorted = result.sort_values(by='ctx-computation-faulted', ascending=False)

  print(result_sorted)


def filter_by_polarity(df:pd.DataFrame, polarity_value):
    """
    Filters the DataFrame based on the polarity column.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    polarity_value (int): The polarity value to filter by (0 or 1).

    Returns:
    pd.DataFrame: A DataFrame containing only rows with the specified polarity.
    """
    # Check if the polarity value is valid
    if polarity_value not in [0, 1]:
        raise ValueError("polarity_value must be either 0 or 1.")

    # Filter the DataFrame
    filtered_df = df[df['polarity'] == polarity_value]

    return filtered_df

def compute_coil_counts_by_vlevel_plot(df):
    """
    Plots the count of ones in each of the coils-hvt-cX columns for each v-level.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the columns of interest.
    """
    # Define the columns of interest
    coil_columns = [f'coils-lvt-c{X}' for X in range(11)]

    # Ensure the columns exist in the DataFrame
    for col in coil_columns:
        if col not in df.columns:
            raise ValueError(f"Column {col} not found in the DataFrame.")

    # Create a figure for the plot
    plt.figure(figsize=(12, 8))

    # Iterate over each coil column and plot
    for col in coil_columns:
        # Group by 'v-level' and count the ones in the coil column
        counts = df[df[col] == 1].groupby('v-level').size()

        # Plot the counts
        plt.plot(counts.index, counts.values, label=col)

    # Add labels and legend
    plt.xlabel('V-Level')
    plt.ylabel('Count of Ones')
    plt.title('Count of Ones in Coil Columns by V-Level')
    plt.legend()
    plt.grid(True)

    # Show the plot
    # plt.show()



def plot_coil_counts_by_vlevel_and_polarity(df, export_dir, id=""):
    """
    Plots the count of ones in each of the coils-lvt-cX columns for each v-level and polarity.
    Parameters:
    df (pd.DataFrame): The input DataFrame containing the columns of interest.
    export_dir (str): Directory to export CSV files.
    id (str): Identifier for the output files.
    """
    # Define the columns of interest
    coil_columns = [f'coils-{type_}-c{X}' for X in range(11) for type_ in ['lvt', 'hvt', 'std']]

    # Ensure the columns exist in the DataFrame
    for col in coil_columns:
        if col not in df.columns:
            raise ValueError(f"Column {col} not found in the DataFrame.")

    # Create a figure for the plot
    plt.figure(figsize=(12, 8))

    # Define colors for each coil
    colors = plt.colormaps.get_cmap('tab20')

    # Filter data for polarity=1 and polarity=0
    df_polarity_1 = df[df['polarity'] == 1]
    df_polarity_0 = df[df['polarity'] == 0]
    print(f"Elements with positive (1) polarity: {df_polarity_1.shape[0]}")
    print(f"Elements with negative (0) polarity: {df_polarity_0.shape[0]}")

    # Group by 'v-level' and count the total elements for each v-level
    total_counts = df.groupby('v-level').size()

    # Iterate over each coil column and plot for each polarity
    for idx, col in enumerate(coil_columns):


        # Group by 'v-level' and count the ones in the coil column for polarity=1
        counts_polarity_1 = df_polarity_1[df_polarity_1[col] == 1].groupby('v-level').size()
        # Group by 'v-level' and count the ones in the coil column for polarity=0
        counts_polarity_0 = df_polarity_0[df_polarity_0[col] == 1].groupby('v-level').size()

        # Plot the counts for polarity=1 with dashed line
        plt.plot(counts_polarity_1.index, counts_polarity_1.values,
                 color=colors(idx), linestyle='--', label=f'{col} (Polarity=1)')
        # Plot the counts for polarity=0 with dotted line
        plt.plot(counts_polarity_0.index, counts_polarity_0.values,
                 color=colors(idx), linestyle=':', label=f'{col} (Polarity=0)')

        # Create DataFrames for CSV export
        csv_data_polarity_1 = pd.DataFrame({
            'V-Level': counts_polarity_1.index,
            'Count': counts_polarity_1.values,
            'Total_Elements': [total_counts.get(level, 0) for level in counts_polarity_1.index]
        })
        csv_data_polarity_0 = pd.DataFrame({
            'V-Level': counts_polarity_0.index,
            'Count': counts_polarity_0.values,
            'Total_Elements': [total_counts.get(level, 0) for level in counts_polarity_0.index]
        })

        # Export to CSV
        csv_data_polarity_1.to_csv(os.path.join(export_dir, f'{id}{col}_polarity_1.csv'), index=False)
        csv_data_polarity_0.to_csv(os.path.join(export_dir, f'{id}{col}_polarity_0.csv'), index=False)

    # Add labels and legend
    plt.xlabel('V-Level')
    plt.ylabel('Count of Ones')
    plt.title('Count of Ones in Coil Columns by V-Level and Polarity')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)


def plot_polarity_start_comparison(df,
                                   export_dir,
                                   id=""
                                   ):
    """
    Plots a bar chart comparing which polarity starts earlier for each coil.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the columns of interest.
    """
    # Define the columns of interest
    coil_columns = [f'coils-lvt-c{X}' for X in range(11)]

    # Ensure the columns exist in the DataFrame
    for col in coil_columns:
      if col not in df.columns:
        raise ValueError(f"Column {col} not found in the DataFrame.")

    # Prepare data for plotting
    comparison_results = []

    for col in coil_columns:
      # Filter data for polarity=1 and polarity=0
      df_polarity_1 = df[df['polarity'] == 1]
      df_polarity_0 = df[df['polarity'] == 0]

      # Find the starting v-level for polarity=1 and polarity=0
      starting_vlevel_1 = df_polarity_1[df_polarity_1[col] == 1]['v-level'].min()
      starting_vlevel_0 = df_polarity_0[df_polarity_0[col] == 1]['v-level'].min()

      # Compare the starting v-levels
      if starting_vlevel_1 < starting_vlevel_0:
        comparison_results.append(1)
      elif starting_vlevel_1 > starting_vlevel_0:
        comparison_results.append(0)
      else:
        comparison_results.append(0.5)


    # Create a figure for the plot
    plt.figure(figsize=(12, 8))

    # Create a bar chart
    y = np.arange(len(coil_columns))
    heights = [result - 0.5 for result in comparison_results]  # Adjust heights to be around 0.5 baseline

    bars = plt.barh(y, heights, color='skyblue')

    # Customize the plot
    plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8)  # Baseline at 0.5
    plt.yticks(y, coil_columns)
    plt.xlabel('Polarity Starting Comparison')
    plt.title('Comparison of Starting Polarity for Each Coil')
    plt.xlim(-0.5, 0.5)
    plt.grid(True, axis='x')

    # Show the plot
    plt.tight_layout()
    # plt.show()

    comparison_df = pd.DataFrame({
        'coil': coil_columns,
        'value': comparison_results
    })
    comparison_df.to_csv(f'{export_dir}/polarity-comparison-results{id}.csv', index=False)


def identify_zero_coils(df, cell_type:str):
    """
    Identifies coils where only zeros are present in their columns.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing the columns of interest.

    Returns:
    list: A list of coil columns that contain only zeros.
    """
    # Define the columns of interest
    coil_columns = [f'coils-{cell_type}-c{X}' for X in range(11)]

    # Ensure the columns exist in the DataFrame
    for col in coil_columns:
        if col not in df.columns:
            raise ValueError(f"Column {col} not found in the DataFrame.")

    # Identify columns with only zeros
    zero_coils = [col for col in coil_columns if df[col].sum() == 0]

    return zero_coils


def compute_difference_and_count_ones(df, com, pin, cell_type):
  """
  Compute the difference between pinout and asic-fpga communication of the
  detected events for given cell_type, and count the number of differences.

  Parameters:
  df (pd.DataFrame): The DataFrame containing the data.
  com (str): The name of the coil reported via the asic2fpga communication.
  col_y (str): The name of the coil reported via pin.
  col_z (str): The name of the cell type used to filter the results of the
  pin column to only match hvt to hvt, std to std and lvt to lvt.

  Returns:
  int: The number of 1s in the XOR result column for the filtered rows.
  """
  # print(df['coil-type-in'])
  # print(df['coil-type-out'])
  # if df['coil-type-out'] != df['coil-type-in']:
  #   print('coil-type-out does not match coil-type-in')
  #   return -1

  filtered_df = df[df['coil-type-in'] == 1].copy()

  xor_result_col = f'{com}_xor_{pin}'
  filtered_df[xor_result_col] = filtered_df[com] ^ filtered_df[pin]

  number_of_ones = filtered_df[xor_result_col].sum()

  return number_of_ones

def compute_difference_heatmap(heatmap_data1, heatmap_data2, title, export_dir, id=""):
    difference_heatmap = heatmap_data1.subtract(heatmap_data2)

    wide_df = difference_heatmap.reset_index().melt(id_vars='y-idx',
                                                     var_name='x-idx',
                                                     value_name='value')
    wide_df = wide_df[['x-idx', 'y-idx', 'value']]
    wide_df = wide_df.sort_values(by=['y-idx', 'x-idx'])

    filename = f'difference-heatmap-id-{id}'
    csv_filename = os.path.join(export_dir, f'{filename}.csv')

    wide_df.to_csv(csv_filename, index=False)
    print(f"Exported difference data for {id} to {csv_filename}")

    plt.figure(figsize=(10, 10))
    sns.heatmap(difference_heatmap, annot=True, fmt='g', cmap='coolwarm', center=0)
    plt.title(title)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    # plt.show()

    return difference_heatmap

def analysis(df:pd.DataFrame, clean:bool, results_dir:str,
             experiment_directory:str, all:bool):
  result_cache_file = results_dir +'/'+experiment_directory + '-results_cache'
  results_df = None

  no_detection_reg_but_effective_faults_df = compute_no_detection_reg_but_effective_fault_cases(df,
                                                     export_dir=(results_dir+"/"+experiment_directory),
                                                     id="all",log=False,
                                                     clean=clean)
  no_detection_pin_but_effective_faults_df = compute_no_detection_pin_but_effective_fault_cases(df,
                                                     export_dir=(results_dir+"/"+experiment_directory),
                                                     id="all",log=False,
                                                     clean=clean)

  no_detection_but_effective_faults_df = compute_pin_and_reg_no_detection_but_effective_fault_cases(df,
                                                     export_dir=(results_dir+"/"+experiment_directory),
                                                     id="all",log=False,
                                                     clean=clean)

  no_detection_no_timeout_but_effective_faults_df = filter_df_no_timeout(
    no_detection_but_effective_faults_df, export_dir=(results_dir+"/"+experiment_directory),
    id="no_detection_but_effective_faults", clean=clean)

  no_timeouts_df = filter_df_no_timeout(df, results_dir+"/"+experiment_directory)

  if not clean:
    try:
      cached = os.path.exists(result_cache_file + ".parquet")
      cached = cached and os.path.exists(result_cache_file + ".csv")

      if cached:
        results_df = pd.read_parquet(result_cache_file + ".parquet", engine='pyarrow')

    except Exception as e:
      print(f"Error reading cache files: {e}")
      clean = True  # Force recomputation if reading fails

  if clean or results_df is None:
    # Statistics
    num_measurements = get_number_of_measurments(df)
    num_measurements_per_position = get_number_of_measurments_per_position(df)

    num_corrupted_plaintext = get_number_of_corrupted_plaintext(df)
    num_faulted_ciphertext = get_number_of_corrupted_ciphertext(df)

    num_faulted_ciphertext_no_timeout = get_number_of_corrupted_ciphertext(no_timeouts_df)

    num_reg_emfi_observations, num_pin_emfi_observations = get_number_of_coil_detections(df)

    num_no_detection_by_reg_but_effective_faults = get_number_of_measurments(
      no_detection_reg_but_effective_faults_df,
      ", where coils report detected emfi through the asic-fpga communication")

    num_no_detection_by_pin_but_effective_faults = get_number_of_measurments(
      no_detection_pin_but_effective_faults_df,
      ", where coils report detected emfi through the pinout")

    num_no_detection_by_pin_and_reg_but_effective_faults = get_number_of_measurments(
      no_detection_but_effective_faults_df ,
      ", where coils report detected emfi through the pinout or asic-fpga communication...")

    num_no_detection_no_timeout_but_effective_faults  = get_number_of_measurments(
      no_detection_no_timeout_but_effective_faults_df,
      ", where coils report detected emfi through the pinout or asic-fpga communication and do not timeout...")


    results_df = pd.DataFrame({
      'num_measurements': [num_measurements],
      'num_measurements_per_position': [num_measurements_per_position],
      'num_corrupted_plaintext': [num_corrupted_plaintext],
      'num_faulted_ciphertext': [num_faulted_ciphertext],
      'num_faulted_ciphertext_no_timeout': [num_faulted_ciphertext_no_timeout],
      'num_reg_emfi_observations': [num_reg_emfi_observations],
      'num_pin_emfi_observations': [num_pin_emfi_observations],
      'num_no_detection_by_reg_but_effective_faults' : [num_no_detection_by_reg_but_effective_faults],
      'num_no_detection_by_pin_but_effective_faults' : [num_no_detection_by_pin_but_effective_faults],
      'num_no_detection_by_pin_and_reg_but_effective_faults' : [num_no_detection_by_pin_and_reg_but_effective_faults],
      'num_no_detection_no_timeout_but_effective_faults' : [num_no_detection_no_timeout_but_effective_faults]
    })

    results_df.to_csv(result_cache_file + ".csv")
    results_df.to_parquet(result_cache_file + ".parquet", engine='pyarrow')


  print("Results: ")
  print(results_df.T)
  # compute_parameters_with_most_effetive_faults(df, "(all)")
  # compute_parameters_with_most_effetive_faults(no_detection_but_effective_faults_df,
  #                                              "(undetected)")

  compute_coil_counts_by_vlevel_plot(df)
  polarity_one_df = filter_by_polarity(df, 1)
  compute_coil_counts_by_vlevel_plot(polarity_one_df)

  polarity_zero_df = filter_by_polarity(df, 0)
  compute_coil_counts_by_vlevel_plot(polarity_zero_df)

  plot_coil_counts_by_vlevel_and_polarity(no_timeouts_df,
                                          results_dir + '/' + experiment_directory,
                                          )
  plot_polarity_start_comparison(no_timeouts_df,
                                 results_dir + '/' + experiment_directory,
                                 )

  # Headmaps
  compute_coordinates_effective_faults_heatmap(no_timeouts_df,
                                               results_dir + '/' + experiment_directory,
                                               id="effective-no-timeout-faults",
                                               clean=clean
                                               )
  compute_coordinates_timeout_heatmap(df,
                                      results_dir + '/' + experiment_directory,
                                      id="all"
                                      )


  # # Define the columns of interest
  # coil_columns = [f'coils-{CT}-c{X}' for X in range(11) for CT in ['lvt', 'std',
  #                                                                  'hvt',
  #                                                                  'pinout']]
  #
  # for col in coil_columns:
  #     if col not in df.columns:
  #         raise ValueError(f"Column {col} not found in the DataFrame.")
  #
  # heatmap_data_lvt = []
  # heatmap_data_std = []
  # heatmap_data_hvt = []
  # heatmap_data_pinout = []
  # for col in coil_columns:
  #   single_heatmap_data = compute_coordinates_detection_heatmap(no_timeouts_df,
  #                                         col,
  #                                         results_dir + '/' + experiment_directory,
  #                                         id="all",
  #                                         clean=clean)
  #   if 'lvt' in col:
  #     heatmap_data_lvt.append(single_heatmap_data)
  #   if 'std' in col:
  #     heatmap_data_std.append(single_heatmap_data)
  #   if 'hvt' in col:
  #     heatmap_data_hvt.append(single_heatmap_data)
  #   if 'pinout' in col:
  #     heatmap_data_pinout.append(single_heatmap_data)
  #
  #  compute_difference_heatmap(heatmap_data_lvt[0],
  #                             heatmap_data_hvt[0],
  #                             "LVT-C0 - HVT-C0",
  #                             results_dir + '/' + experiment_directory,
  #                             id="lvt-hvt-c0-difference")
  #
  coil_columns = []
  if all:
    coil_columns = [f'coils-pinout-c{X}' for X in range(11)]
  else:
    coil_columns = [f'coils-pinout-c{4}']

  for col in coil_columns:
    if all:
      for t in ['lvt', 'std', 'hvt']:
        compute_coordinates_detection_heatmap_pinout_based(df,
                                            t,
                                            col,
                                            results_dir + '/' + experiment_directory,
                                            id="all",
                                            clean=clean)
    else:
      compute_coordinates_detection_heatmap_pinout_based(df,
                                          'lvt',
                                          col,
                                          results_dir + '/' + experiment_directory,
                                          id="all",
                                          clean=clean)



  # includes timeouts
  # compute_coordinates_effective_faults_heatmap(no_detection_but_effective_faults_df,
  #                                              results_dir + '/' + experiment_directory,
  #                                              id="no-detection",
  #                                              clean=clean)

  if no_detection_no_timeout_but_effective_faults_df is not None:
    compute_coordinates_effective_faults_heatmap(no_detection_no_timeout_but_effective_faults_df,
                                               results_dir + '/' + experiment_directory,
                                               id="no-timeout-no-detection",
                                               clean=clean)
  else:
    print("Data not available")
    return -1


  compute_voltage_low_jitter_delay_effective_faults_heatmap(no_timeouts_df,
                                                            results_dir + '/' + experiment_directory,
                                                            id="no-timeouts",
                                                            clean=clean)
  compute_voltage_low_jitter_delay_effective_faults_heatmap(no_detection_no_timeout_but_effective_faults_df,
                                                            results_dir + '/' + experiment_directory,
                                                            id="no-timeouts-undetected",
                                                            clean=clean)


  # compute_voltage_low_jitter_delay_timeout_heatmap(df,
  #                                                  results_dir + '/' + experiment_directory,
  #                                                  id="all",
  #                                                  clean=clean)
  #
  # compute_voltage_low_jitter_delay_timeout_heatmap(no_detection_but_effective_faults_df,
  #                                                  results_dir + '/' + experiment_directory,
  #                                                  id="no-detection",
  #                                                  clean=clean)

  # Graphs
  # compute_voltage_vs_effective_faults_and_timeout_plot(df, True)
  # compute_low_jitter_delay_vs_faults_effective_and_timeout_plot(df, True)


###############################################################################
#                               SETTING
###############################################################################
positions_on_x = 11
repetitions = 10
root_directory = 'measurements'
results_dir = 'results'


###############################################################################

def main():
  """Main function that serves as the entry point of the program."""

  clean = True
  all = False

  for exp in ['v3-10rep-1_1mx1_1mm',
              'v4-10rep-1_1mx1_1mm',
              'v5-10rep-1_1mx1_1mm']:

    experiment_directory = exp
    cache_file = results_dir +'/'+experiment_directory + '/' +'dataframe.parquet'
    csv_file = results_dir +'/'+experiment_directory + '/' +'dataframe.csv'

    # Check if the cache file exists
    if os.path.exists(cache_file) and not clean:
      # Load the DataFrame from the cache file
      df = pd.read_parquet(cache_file, engine='pyarrow')

    else:
      # Save the DataFrame to the cache file

      all_measurements = process_directory(root_directory+'/'+experiment_directory)
      for i in range(0,16):
        print(acum_status_array[i])

      print(f"Total measurements: {len(all_measurements)}")

      df = pd.DataFrame(all_measurements)

      df.to_parquet(cache_file, engine='pyarrow')
      df.to_csv(csv_file)

    df = preprocessing(df, clean, results_dir, experiment_directory)

    analysis(df, clean, results_dir, experiment_directory, all)



if __name__ == "__main__":
    main()


