import numpy as np
import wfdb
import os
import json

# Function to get record names in a given database path.
def get_record_names(database_path):
    record_names = []
    for file in os.listdir(database_path):
        if file.endswith('.dat'):
            record_names.append(file[:-4])
    return record_names

# Function to add noise to a signal to achieve a desired SNR.
def add_noise(signal, noise, desired_snr):
    signal_power = np.mean(np.abs(signal)**2, axis=0)
    noise_power = np.mean(np.abs(noise)**2, axis=0)
    scaling_factor = np.sqrt(signal_power / (noise_power * 10**(desired_snr/10)))
    noisy_signal = signal + scaling_factor * noise
    return noisy_signal

# Function to process a record, adding noise if specified, and writing the result to a JSON file.
def process_record(clean_record_name, database_path, noise_signal, output_path, desired_snr):
    # Read the clean signal record from the database
    clean_signal_record = wfdb.rdrecord(os.path.join(database_path, clean_record_name))
    clean_signal = clean_signal_record.p_signal
    
    # Add noise to the clean signal if desired SNR is specified
    if desired_snr == 'inf':
        noisy_ecg_signal = clean_signal
    elif desired_snr.isdigit():
        if clean_record_name != '114':
            noisy_ecg_signal = add_noise(clean_signal, noise_signal, desired_snr)
        else:
            # Special case for record '114' where the noise signal is reversed
            noisy_ecg_signal = add_noise(clean_signal, noise_signal[:, ::-1], desired_snr)
    else:
        # Return False if desired SNR is not a number or 'inf'
        return False
    
    # Read annotations from the record
    clean_annotations = wfdb.rdann(os.path.join(database_path, clean_record_name), 'atr')
    annotation_data = {
        'record_name': f'{clean_record_name}',
        'extension': clean_annotations.extension,
        'sample': clean_annotations.sample.tolist(),
        'symbol': clean_annotations.symbol,
        'subtype': clean_annotations.subtype.tolist(),
        'chan': clean_annotations.chan.tolist(),
        'num': clean_annotations.num.tolist(),
        'aux_note': clean_annotations.aux_note,
        'signal': noisy_ecg_signal.tolist()
    }
    
    # Write the annotation data to a JSON file
    output_filename = os.path.join(output_path, f'{clean_record_name}.json')
    with open(output_filename, 'w') as outfile:
        json.dump(annotation_data, outfile)
    
    return True

# Main function that specifies the desired SNRs, sets the database and output paths, and processes each record in the database.
def main():
    # Define the desired SNRs
    desired_snrs = ['inf']
    
    for desired_snr in desired_snrs:
        print('SNR:', desired_snr)
        
        # Set the paths for the database and output
        database_path = './dataset/mit-bih-arrhythmia-database-1.0.0'
        output_path = f'./dataset/mit-bih-arrhythmia-database-1.0.0_em{desired_snr}'
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Get the names of the records in the database
        record_names = get_record_names(database_path)
        
        # Read the noise record
        noise_record = wfdb.rdrecord('/home/matteo/Documents/projects/work/dataset/mit-bih-noise-stress-test-database-1.0.0/em')
        noise_signal = noise_record.p_signal

        # Process each record in the database
        for record_name in record_names:
            if process_record(record_name, database_path, noise_signal, output_path, desired_snr):
                print(record_name, end='\r')
            else:
                print('SNR value error')

# If the script is run (instead of imported), call the main function.
if __name__ == '__main__':
    main()
