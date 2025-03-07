# README

## Overview

This script is designed for fitting Lorentzian models to magnetic resonance data, particularly for analyzing the magnetic properties of materials. It processes data, fits models to the peaks of the magnetic resonance spectra, and applies different anisotropy models such as In-Plane (IP), Out-of-Plane (OP), and Ultrathin110 (U110). The script calculates key magnetic parameters like the Gilbert damping factor and the material's saturation magnetization.

## Dependencies

The script requires the following Python libraries:

- `math`
- `scipy`
- `pylab`
- `matplotlib`
- `re`
- `operator`
- `time`
- `lmfit`
- `numpy`
- `tqdm`
- `pyqtgraph`

You can install the necessary libraries using pip:

```bash
pip install numpy scipy matplotlib lmfit tqdm pyqtgraph
```

## Script Structure

### 1. **Material Variables**

- Defines material-specific constants such as saturation magnetization (`Ms`), anisotropy constants (`K4`, `K2`), and intrinsic field values (`Hintrinsic`).
- The anisotropy type can be set to "IP", "OP", or "U110".

### 2. **Modeling and Fitting**

- The script fits Lorentzian models to the peaks in the magnetic resonance data.
- It uses the `lmfit` library to fit a custom function that combines symmetric and asymmetric Lorentzian components.
- A model based on the Kittel equation is used to analyze the data depending on the selected anisotropy type.

### 3. **Data Processing**

- It reads data from `.txt` files in the current directory.
- The data is assumed to be in two columns: magnetic field (x-axis) and signal (y-axis).
- The script finds peaks in the y-axis data using `scipy.signal.find_peaks`.

### 4. **Damping Calculation**

- The script calculates the Gilbert damping coefficient from the fits to the data, both for individual peaks and overall damping behavior.
- The fitting models include a damping function based on the magnetic field and frequency.

### 5. **Output and Visualization**

- The script generates plots showing the magnetic field vs. peak positions, full-width at half maximum (FWHM), damping values, and fitted curves.
- The results are saved in CSV files, which include the fit parameters, peak values, FWHM, and damping coefficients.
- It also saves fit reports in text files.

### 6. **Customization**

- The anisotropy type (IP, OP, U110) can be customized by changing the `Anisotropy` variable.
- The error tolerance for fits can be adjusted through the variables like `erromaxlorentzfwhm` and `erromaxlorentzpeak`.

## Running the Script

To run the script:

1. Place your magnetic resonance data files (`*.txt`) in the same directory as the script.
2. Run the script in your Python environment:

```bash
python script_name.py
```

The script will process the data, fit models, generate plots, and save the results in CSV and image files.

## Output Files

- **Fit_PeakX.png**: Images of the fitted peaks and their corresponding fits.
- **fields_fwhm_peak_X.csv**: CSV file containing magnetic field, peak, and FWHM values for each peak.
- **DampingsX.csv**: CSV file with detailed damping calculations, including peak frequencies, dH, and damping parameters.
- **Fit_Values_PeakX.csv**: CSV file with the fit reports from the Lorentzian and damping fits.

## License

This script is provided for research and educational purposes. This project is open-source and available under the MIT License.
