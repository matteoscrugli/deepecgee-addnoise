import os
import subprocess
import shutil
import fnmatch

def process_files(input_folder, snr, noise_file, format_code):

    # Output nsf folder
    command_output_name = "out"

    # Get the list of files in the folder
    file_list = [file for file in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, file)) and '.dat' in file] #  not in ['ANNOTATORS', 'RECORDS', 'SHA256SUMS.txt']

    # Filter the list of files to get a unique set of filenames without extensions
    input_files = sorted(list(set([os.path.splitext(file)[0] for file in file_list])))

    # Get the list of noise files with different extensions
    noise_folder = os.path.dirname(noise_file)
    noise_file_base = os.path.basename(noise_file)
    noise_files = fnmatch.filter(os.listdir(noise_folder), f"{noise_file_base}.*")

    # Copy the noise files to the input_folder
    copied_noise_files = []
    for nf in noise_files:
        shutil.copy(os.path.join(noise_folder, nf), os.path.join(input_folder, nf))

    # Change the working directory to the specified input_folder
    os.chdir(os.path.join(input_folder))

    # Iterate through the files and run the command for each file
    for file in input_files:
        input_file = file
            
        # Create the command as a list of strings
        command = ["nst", "-i", input_file, noise_file_base, "-o", os.path.join(command_output_name, input_file), "-s", str(snr)] #, "-F", str(format_code)

        # Run the command
        subprocess.run(command)

        # Header fix
        headerfile = os.path.join(command_output_name, input_file) + '.hea'

        # Read the contents of the file into memory
        with open(headerfile, 'r') as file:
            lines = file.readlines()

        # Modify the lines by removing "{output folder}/"
        modified_lines = [line.replace(os.path.join(command_output_name, ''), '') for line in lines]

        # Overwrite the original file with the modified lines
        with open(headerfile, 'w') as file:
            file.writelines(modified_lines)

        # break

    try:
        # Rename and move the "out" folder to "../{os.path.basename(input_folder)}_{os.path.basename(noise_file)}_{snr}" #_{format_code}
        output_folder = os.path.dirname(input_folder)
        os.makedirs(output_folder, exist_ok=True)
        if os.path.exists(os.path.join(output_folder, command_output_name)):
            shutil.rmtree(os.path.join(output_folder, command_output_name))
        shutil.move(os.path.join(input_folder, command_output_name), output_folder)
        os.rename(os.path.join(output_folder, command_output_name), os.path.join(output_folder, f"{os.path.basename(input_folder)}_{os.path.basename(noise_file)}_{snr}")) #_{format_code}
    except Exception as e:
        print(f"WARNING: {e}")
        
    try:
        # Remove the noise files from the input_folder
        noise_files = fnmatch.filter(os.listdir(), f"{noise_file_base}.*")
        for nf in noise_files:
            os.remove(os.path.join(input_folder, nf))
    except Exception as e:
        print(f"WARNING: {e}")

# Replace the paths below with the paths to your desired folders
snr = 2
format_code = 212
noise_file = "./dataset/mit-bih-noise-stress-test-database-1.0.0/em"
input_folder = "./dataset/mit-bih-arrhythmia-database-1.0.0"
process_files(input_folder, snr, noise_file, format_code)
