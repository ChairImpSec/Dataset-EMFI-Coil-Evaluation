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

### Flags in `read.py`
- **`clean` (line 1481):**
  Set `clean=False` to use cached data (included in this repository) instead of recomputing all steps.

- **`all` (line 1482):**
  Set `all=True` to compute all available plots.
- **['v3-10rep-1_1mx1_1mm', 'v4-10rep-1_1mx1_1mm','v5-10rep-1_1mx1_1mm'] (line 1492 to 1494)**:
  Experiments that are evaluated.

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
<!-- TODO:  In which order to execute? -->

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

## 📧 Contact

For questions or issues, please contact:
felix.uhle@rub.de or open an issue on the repository.

---
