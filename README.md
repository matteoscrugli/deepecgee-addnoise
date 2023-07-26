
# ECG Noise Addition and Processing Scripts

This repository contains two Python scripts that are designed for processing Electrocardiogram (ECG) signals by adding noise and extracting useful data. 

## Table of Contents

- [Requirements](#requirements)
- [nst_method.py](#script-1-file-processor)
  - [Process Files Function](#process-files-function)
- [snr_method.py](#script-2-record-processor)
  - [Get Record Names Function](#get-record-names-function)
  - [Add Noise Function](#add-noise-function)
  - [Process Record Function](#process-record-function)
  - [Main Function](#main-function)
- [License](#license)

## Requirements

Both scripts require the following Python packages:
- numpy
- wfdb
- os
- json

You can install them using pip:

```bash
pip install numpy wfdb os json
```

## [nst_method.py](nst_method.py)

The `nst` script, part of the WFDB library, provides a noise stress test for ECG analysis programs. It works by taking a clean ECG signal, adding calibrated amounts of noise from a specified noise record, and creating an output record in the WFDB format. This allows users to evaluate the noise tolerance of different analysis programs.

The output signals are generated by pairing each clean signal with a noise signal, combining them with a gain and offset. The initial gain and offset values are set to zero, meaning no noise is added initially. However, the gain values can be adjusted over time as defined in the protocol annotation file. 

The `nst` script also includes an option to calculate and adjust the signal-to-noise ratio (SNR). The SNR calculation in this script takes into consideration the difficulties of defining and measuring signal power in the ECG. The script uses sigamp(1) to read the reference annotation file for the ECG record and measures the peak-to-peak amplitude of each of the first 300 normal QRS complexes, from which the power of the signal (S) is estimated. The power of the noise (N) is determined from the unscaled noise signals. 

### Process Files Function

Here's the brief flow of the `nst_method.py` function:

1. **Copy Noise Files**: It copies a series of noise files into the input folder.

2. **Command Execution**: For each file in the input folder, it executes a command using the subprocess module.

3. **Header Modification**: After that, it modifies a header file associated with each file. This involves reading the contents of the header file, modifying the lines to remove the output folder path, and writing the modified lines back to the file.

4. **Output Folder Relocation**: Finally, it moves the output folder to a different location. 

To run the script, simply run the following command in your terminal:

```bash
python nst_method.py
```

You can modify the input folder, the noise file, and other parameters directly in the script.

## [snr_method.py](snr_method.py)

The second script (`snr_method.py`) is used to add noise to ECG signals to achieve a desired Signal-to-Noise Ratio (SNR). It then writes the result (the noisy ECG signals and their corresponding annotations) to a JSON file.

### Get Record Names Function

The `get_record_names` function fetches all the record names from the given database path.

### Add Noise Function

The `add_noise` function adds noise to a signal to achieve a desired SNR. It first calculates the signal and noise power, then computes the scaling factor needed to achieve the desired SNR, and finally adds the scaled noise to the original signal.

### Process Record Function

The `process_record` function processes a single record, adding noise to the clean signal if a desired SNR is specified, and writes the noisy signal and its corresponding annotations into a JSON file.

### Main Function

The `main` function specifies the desired SNRs, sets the database and output paths, and processes each record in the database. 

To run the script, use the following command:

```bash
python snr_method.py
```

You can modify the desired SNR, database path, and other parameters directly in the script.

## License

This project is open-source, made available under the [MIT License](LICENSE).
