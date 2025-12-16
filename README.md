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

To reproduce the results, you need:
1. **[Git LFS](https://git-lfs.github.com/)** - Required for cloning large data files
2. **Environment setup** (choose one):
   - **[Nix package manager](https://nixos.org/download/)** (recommended for reproducibility)
   - **Python 3.13+** with pip (tested with Python 3.13.9, see `requirements.txt`)

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

### 1. Install Git LFS (if not already installed)
```bash copy
# On Ubuntu/Debian
sudo apt-get install git-lfs

# On macOS
brew install git-lfs

# On other systems, see: https://git-lfs.github.com/
```

Initialize Git LFS:
```bash copy
git lfs install
```

### 2. Clone the Repository
```bash copy
git clone https://github.com/ChairImpSec/Dataset-EMFI-Coil-Evaluation
cd Dataset-EMFI-Coil-Evaluation
```

> [!IMPORTANT]
> Due to Git LFS budget limitations, it is currently not possible to clone the preprocessed cached files (`.parquet` files in `results/`).
> The corresponding error can be ignored.
> However, **you must regenerate all temporary files** using the `make full-rebuild` command (see section 4 below).
> This will process the raw measurement data (~30 minutes) to generate all analysis results.

### 3. Set Up the Environment

**Option A: Using Nix Flakes (recommended - provides pinned dependencies):**
```bash copy
nix develop
```

For setups without experimental features enabled:
```bash copy
nix --extra-experimental-features 'nix-command flakes' develop
```

**Option B: Using traditional Nix:**
```bash copy
nix-shell
```

**Option C: Using pip (without Nix):**
```bash copy
pip install -r requirements.txt
```

### 4. Run the Analysis Script
Execute the following command to process cached data and generate CSV files:
```bash copy
python read.py
```
By default, this uses cached preprocessed data (included in the repository) and generates only pinout-based detection heatmaps. For full analysis from raw data, see the command-line options below.

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
# Quick start - use cached data with partial analysis (default)
python read.py

# Command equivalent to the original submitted version
python read.py --clean --all partial

# Full analysis - required to run the scripts in `results` (takes ~30 minutes)
python read.py --clean --no-show-plots --all all

# Regenerate with partial analysis without showing plots
python read.py --clean --no-show-plots
```

> [!NOTE]
> When all plots are generated, 4 of these plots will contain only zeros for all coordinates.
> The reason for this is a bug in the HDL implementation of the ASIC hosting the physical and algorithmic countermeasures:
> The four HVT registers with the highest index are not connected to the data bus correctly.

**Experiments evaluated:**
The script processes three target implementations: `v3-10rep-1_1mx1_1mm`, `v4-10rep-1_1mx1_1mm`, and `v5-10rep-1_1mx1_1mm`.

> [!NOTE]
> The script generates more plots than depicted in the publication.


---

## 📈 Dataset Description

### Measurement Folders
The `measurements` directory contains subfolders for each target, as described below:

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
These files are saved in the `results` directory, mirroring the structure of the `measurements` folder.

> [!NOTE]
> Some plots (e.g., the first four line plots per target) are not directly used in the publication, but post-processed.

---

## ✨ Reproduction Workflow

### Quick Start (Using Cached Data)

The repository includes preprocessed data for fast reproduction:

```bash copy
make              # Run post-processing with cached data (~1 minute)
```

### Complete Reproduction (From Raw Data)

To regenerate everything from scratch:

```bash copy
make full-rebuild    # Clean and regenerate everything (~30 minutes)
```

### Step-by-Step Workflow

```bash copy
make clean            # Remove all generated files
make analysis-clean   # Generate CSV files from raw measurements (~30 min)
make post-process     # Run post-processing scripts for merged plots
```

### Available Make Targets

- `make` - Quick run using cached data (default)
- `make full-rebuild` - Full regeneration from scratch
- `make analysis` - Generate results using cached preprocessed data
- `make analysis-clean` - Regenerate from raw measurement files
- `make post-process` - Run post-processing scripts only
- `make clean` - Remove all generated files
- `make help` - Show available targets

### Manual Execution (Without Make)

If you prefer to run scripts manually:

```bash copy
# Step 1: Generate initial CSV files
python read.py --clean --no-show-plots --all all

# Step 2: Run post-processing scripts
cd results
python ../merge-coil-polarity-results.py
python ../merge-coil-results.py
python ../merge-coil-types-for-polarity.py
python ../merge-coil-polarity-first-reaction.py
```

> [!NOTE]
> For completeness, we provide the output of all scripts within the results folder.

---

## 📊 Generating Paper Figures

Currently, no python script is available to generate exactly the same plot as shown in Figure 7a and Figure 7b,
due to manually post-processing and computations from within TikZ.

### Figure 7a (Voltage vs Polarity Counts)

Figure 7a data is generated automatically by the function `plot_coil_counts_by_vlevel_and_polarity(df, export_dir, id="")`.

**Generation pipeline:**

1. Generate initial data:
   ```bash
   python read.py --all partial
   ```
   This opens plots for each target and all three cell types.

2. Merge the data:
   - `merge-coil-polarity-results.py` merges the polarity results
   - `merge-coil-types-for-polarity.py` further merges across cell types

3. Final visualization:
   The resulting CSV is processed by a TikZ script that computes ratios by dividing the detection counts by the number of experiments conducted for each voltage level and polarity.

### Figure 7b (Polarity Comparison)

Figure 7b requires manual post-processing after running `merge-coil-polarity-first-reaction.py`.

The function `plot_polarity_start_comparison(df, export_dir, id="")` generates 3 versions of Figure 7b (one per target).
The final Figure 7b in the paper is the average of these 3 plots, with coil 9 manually adjusted.

The file `results/polarity-comparison-results-merged.csv` contains the merged results.
After post-processing the result is as follows:
   ```csv
   coil,value
   coils-lvt-c0,0
   coils-lvt-c1,0
   coils-lvt-c2,3
   coils-lvt-c3,0
   coils-lvt-c4,3
   coils-lvt-c5,3
   coils-lvt-c6,3
   coils-lvt-c7,0
   coils-lvt-c8,3
   coils-lvt-c9,1.5
   coils-lvt-c10,3
   ```
- **Value interpretation:**
   - `3` = "+" (positive polarity starts earlier)
   - `0` = "-" (negative polarity starts earlier)
   - `1.5` = neutral (no clear preference)

- **Special handling of coil 9:**
    The ninth coil is set to neutral (1.5) because we observed that the coil itself does not detect the EM field, but rather the wires connecting it.
    Therefore, the relationship between the winding direction and field polarity cannot be analyzed for this coil.

---

## 📧 Contact

For questions or issues, please contact:
felix.uhle@rub.de or open an issue on the repository.

---
