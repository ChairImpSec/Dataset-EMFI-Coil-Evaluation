# 📊 Dataset EMFI Coil Evaluation

This repository contains the datasets and analysis scripts supporting the **CHES 2026** publication:
*"Coil-Based Detection and Concurrent Error Correction Against EMFI: An Experimental Case-Study on a Prototype ASIC"* ([eprint](https://eprint.iacr.org/2025/1923)).
It enables the reproduction of all results and plots presented in the paper.

---

## 📋 Table of Contents
- [🛠️ Prerequisites](#%EF%B8%8F-prerequisites)
- [📂 Repository Structure](#-repository-structure)
- [🚀 Reproducing Results](#-reproducing-results)
- [📈 Dataset Description](#-dataset-description)
- [💻 Implementation Files](#-implementation-files)
- [📄 Output Files](#-output-files)
- [✨ Post-Processing](#-post-processing)
- [📧 Contact](#-contact)

---

## 🛠️ Prerequisites

To reproduce the results, ensure that the [**Nix package manager**](https://nixos.org/download/) (for environment setup) is installed.
If you do not want to use Nix, you can install all dependencies listed in `shell.nix` using your preferred method.
However, we do not provide any support or guarantee for this approach.

---

## 📂 Repository Structure

```
Dataset-EMFI-Coil-Evaluation/
├── implementations/           # Target implementations source code
|   ├── v3                     # Design files τ₁ (Unprotected AES)
|   ├── v4                     # Design files τ₂ (AGEFA AES [3, 1, 3]-code)
|   ├── v5                     # Design files τ₃ (AGEFA AES [16, 8, 5]-code)
|   ├── aes-byte-serial-tb.vhd # Testbench for all designs
├── measurements/              # Raw measurement data
│   ├── v3-10rep-1_1mx1_1mm/   # Target τ₁ (Unprotected AES)
│   │   ├── Y0_X0_Z0/          # Probe position (Y=0, X=0, Z=0)
│   │   └── ...
│   ├── v4-10rep-1_1mx1_1mm/   # Target τ₂ (AGEFA AES [3, 1, 3]-code)
│   ├── v5-10rep-1_1mx1_1mm/   # Target τ₃ (AGEFA AES [16, 8, 5]-code)
│   └── ...
├── results/                   # Generated CSV files and plots
├── read.py                    # Main script for data processing
├── shell.nix                  # Nix environment configuration
└── README.md
```

---

## 🚀 Reproducing Results

### 1. Clone the Repository
```bash copy
git clone https://github.com/ChairImpSec/Dataset-EMFI-Coil-Evaluation
cd Dataset-EMFI-Coil-Evaluation
```

### 2. Set Up the Environment
Use the provided `shell.nix` to install all dependencies:
```bash copy
nix-shell
```

### 3. Run the Analysis Script
Execute the following command to generate CSV files and plots:
```bash copy
python read.py
```
This script processes the raw measurement data and generates CSV files for all plots in the paper.

### Command-Line Options
The script supports the following command-line arguments (use `python read.py --help` to see all options):

- **`--clean`:**
  Regenerate all files from raw measurement data instead of using cached preprocessed data.

  ```bash copy
  python read.py --clean
  ```

- **`--all {all,partial,minimal}`:**
  Set the level of analysis to perform (default: `partial`).
  - `all`: Generate all available heatmaps and plots
  - `partial`: Generate only pinout-based detection heatmaps
  - `minimal`: Generate minimal set of plots

  ```bash copy
  python read.py --all all
  ```

- **`--no-show-plots`:**
  Disable interactive plot display (useful for batch processing).

  ```bash copy
  python read.py --no-show-plots
  ```

**Example usage:**
```bash copy
# Command equivalent to the original submitted version
python read.py --clean --all partial

# Full analysis (required to run the sripts in `results`)
python read.py --clean --no-show-plots --all all

# Use cached data with partial analysis (default)
python read.py

# Regenerate without showing plots
python read.py --clean --no-show-plots
```

**Experiments evaluated:**
The script processes three target implementations: `v3-10rep-1_1mx1_1mm`, `v4-10rep-1_1mx1_1mm`, and `v5-10rep-1_1mx1_1mm`.

> [!NOTE]
> The script generates more plots than depicted in the publication.

---

## 📈 Dataset Description

### Measurement Folders
The `measurement` directory contains subfolders for each target, as described below:

| Folder                | Target Description                     |
|-----------------------|----------------------------------------|
| `v3-10rep-1_1mx1_1mm` | τ₁ (Unprotected AES)                   |
| `v4-10rep-1_1mx1_1mm` | τ₂ (AGEFA AES [3, 1, 3]-code)          |
| `v5-10rep-1_1mx1_1mm` | τ₃ (AGEFA AES [16, 8, 5]-code)         |

### File Naming Convention
Each measurement folder contains subfolders named `Yy_Xx_Z0`, where:
- `x, y ∈ [0, 11]`: Coordinates in the x-y plane.

Inside these subfolders, binary files follow the naming scheme:
`Expr_i_Cc_Xx_Yy_Z0_Vv_Pp_LJDd.dat`
- **`i`**: Experiment index (incremented per variable change).
- **`c`**: Cell type of the coil detection logic on the ASIC (configured via FPGA).
- **`x, y`**: Coordinates in the x-y plane (over the ASIC).
- **`v`**: Voltage for EMFI $v \in [50, 60, ..., 500]$.
- **`p`**: Polarity of the electromagnetic field (`0` = negative, `1` = positive).
- **`d`**: Low jitter delay (delay in $`d`\cdot 0.7$ ns after the trigger is raised by the control FPGA).

---

## 💻 Implementation Files
All target implementations are provided as RTL code in the `implementations` directory, along with a testbench that is compatible with all designs.

## 📄 Output Files

The `read.py` script generates CSV files for each plot in the paper.
These files are saved in the `result` directory, mirroring the structure of the `measurement` folder.

> [!NOTE]
> Some plots (e.g., the first four line plots per target) are not directly used in the publication, but post-processed.

---

## ✨ Post-Processing

For certain plots (e.g., **Plot 7a** and **Plot 7b**), additional post-processing is required.
The scripts for this are located in the `result` folder.
Run them after generating the initial CSV files:

```bash copy
cd result
python merge-coil-polarity-results.py
python merge-coil-results.py
python merge-coil-types-for-polarity.py
python merge-coil-polarity-first-reaction.py
```

> [!NOTE]
> For completeness, we provide the output of all scripts within the result folder.
---

## TODO
From the first comments of the CHES 2026 artifact review the following TODOs are extracted.
- [ ] Add requirement.txt to install with `pip`.
- [x] Fix problem with missing files:
     ```log
        File not found: v3-10rep-1_1mx1_1mm/detection-heatmap-coilcoils-lvt-c8-id-all.csv
        File not found: v4-10rep-1_1mx1_1mm/detection-heatmap-coilcoils-lvt-c8-id-all.csv
        File not found: v5-10rep-1_1mx1_1mm/detection-heatmap-coilcoils-lvt-c8-id-all.csv
        File not found: v3-10rep-1_1mx1_1mm/detection-heatmap-coilcoils-hvt-c1-id-all.csv
        File not found: v4-10rep-1_1mx1_1mm/detection-heatmap-coilcoils-hvt-c1-id-all.csv
        File not found: v5-10rep-1_1mx1_1mm/detection-heatmap-coilcoils-hvt-c1-id-all.csv
     ```
- [ ] Pin versions of the dependencies (suggested for python, but we might do this for nix with flakes as well)

## 📧 Contact

For questions or issues, please contact:
felix.uhle@rub.de or open an issue on the repository.

---
