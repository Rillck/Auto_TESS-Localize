
# 🚀 Auto TESS-Localize

**Auto TESS-Localize** is an automated tool built on top of the [`TESS-Localize`](https://github.com/Higgins21/TESS-Localized) package (Higgins et al. 2022). It allows systematic analysis of a list of TESS targets with known sector and orbital period.

---

## 🧭 Purpose

To streamline and speed up the use of `TESS-Localize` on multiple TESS targets (TICs), providing a clean Python interface that converts periods into frequencies and automates the process of locating the origin of periodic signals observed in TESS light curves.

---

## ⚙️ Features

- Input: list of targets with `TIC`, `Sector`, and `Period (in days)`;
- Automatic conversion of period to frequency (`1 / period`);
- Batch execution of the localization analysis using `tl.Localize`;
- Retrieval of the **best-matching Gaia DR3 source** using `astroquery.vizier`;
- Comparison with the **Gaia DR3 source ID associated with the TIC** (via MAST);
- Automatic generation of visual outputs:
  - SNR maps with the input TIC highlighted in **red**;
  - Light curve plots with fitted model;
- Results compiled in a structured output.

---

## 📁 Outputs

- **`TESS-Localize images/`**:  
  Contains two figures per TIC:
  - `TIC<id>_setor<sector>_SNR.png`: SNR map with Gaia sources and best-fit location;
  - `TIC<id>_setor<sector>_LCfit.png`: light curve with fitted model.

- **Optional CSV file**:
  ```csv
  TIC, Sector, Period (days), Frequency, Gaia DR3 Source (TIC), Best Source (Localize), Match?
  ```

---

## 🧪 Requirements

- Python 3.8+
- Packages:
  - `lightkurve`
  - `astropy`
  - `matplotlib`
  - `astroquery`
  - `pandas`
  - `TESS-Localize` (from Higgins et al.2022)

Install with:

```bash
pip install lightkurve astropy matplotlib astroquery pandas
```

Make sure the `TESS_Localize` module is installed and available in your environment.

---

## 🙌 Citation & Acknowledgments

This project was developed as an automated extension of `TESS-Localize`, designed to support large-scale photometric studies involving stellar variability and periodic signal localization.
If you use this tool in your research, please cite the original author (Higgins et al. 2022) and consider acknowledging this repository by referencing its GitHub link.
Community contributions and feedback are always welcome!


---

## 📚 Reference

> Higgins, A., et al. (2022). *TESS-Localized: A tool for identifying the spatial origin of periodic signals in TESS pixel data*.  
> [`2022ascl.soft04005H`](https://ui.adsabs.harvard.edu/abs/2022ascl.soft04005H/abstract) 

---

