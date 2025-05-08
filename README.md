# 🚀 Auto TESS-Localize

**Auto TESS-Localize** is an automated extension of the [`TESS-Localize`](https://github.com/Higgins21/TESS-Localized) package (Higgins et al. 2022).  
It enables batch analysis of multiple TESS targets (TICs), given known sectors and periods, producing high-resolution outputs and formatted results.

---

## 🧭 Purpose

To streamline and accelerate the application of `TESS-Localize` across multiple targets, converting orbital periods into frequencies and automating the identification of the origin of periodic signals in TESS light curves.

---

## ⚙️ Features

- **User input via file selection** (`.txt` format with headers: `TIC, Sector, Period`);
- **Automatic period-to-frequency conversion** (`1 / period`);
- **Integration with TESS-Localize** for target localization;
- **Gaia DR3 source comparison** using `astroquery.vizier` and `mast`;
- **SNR maps with target highlighted in red**;
- **Light curve plots** with fitted model;
- **Numerical outputs** saved with 6 decimal precision;
- **Progress tracking** for batch execution.

- **Optional local mode (`Auto_TESS-Localize_local.py`)**: skips online Gaia ID lookup and instead requires a `DR3Name` column in the input file.


---

## 📁 Outputs

- **Folder:** `TESS-Localize images/`
  - `TIC<id>_<sector>_SNR.png`: SNR map with Gaia stars and fitted source;
  - `TIC<id>_<sector>_LCfit.png`: Light curve with best-fit model.

- **CSV Output:** `result Auto TESS_Localize.csv`
  ```csv
  TIC, Sector, Period (days), Frequency (1/day),
  Source Gaia DR3 (TIC), Best Gaia Source (Localize),
  p-value, Relative Likelihood, Match?
  ```

## 🛠️ Alternative Version: Auto_TESSLocalize_local.py

This version of the script is designed for users who **already have the Gaia DR3 source IDs** for their TIC targets and want to avoid performing online queries.

### ✅ Key Differences:
- Skips the Gaia ID query via `astroquery`.
- Requires an additional column named `DR3Name` in the input `.txt` file:
  
  ```csv
  TIC, Sector, Period, DR3Name```
  
- The script uses the DR3Name directly for comparison and analysis.
- This is especially useful when working to reduce query time for large datasets.
  
---

## 🧪 Requirements

- Python 3.8+
- Required packages:
  - `lightkurve`
  - `astropy`
  - `matplotlib`
  - `astroquery`
  - `pandas`
  - `inquirer`
  - `TESS_Localize` (from Higgins et al. 2022)

Install them with:

```bash
pip install lightkurve astropy matplotlib astroquery pandas inquirer TESS_Localize
```

---

## 🙌 Citation & Acknowledgments

This project was developed as a batch-processing extension of `TESS-Localize`, tailored for large-scale photometric analysis in stellar variability.  
If you use this tool in your research, please **cite Higgins et al. (2022)** and consider referencing this GitHub repository to support continued development.

---

## 📚 Reference

> Higgins, A., et al. (2022). *TESS-Localized: A tool for identifying the spatial origin of periodic signals in TESS pixel data*.  
> [`2022ascl.soft04005H`](https://ui.adsabs.harvard.edu/abs/2022ascl.soft04005H/abstract)
