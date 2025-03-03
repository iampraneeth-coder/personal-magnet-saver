import subprocess
import os
from tqdm import tqdm
import time

def download_magnet_aria2(magnet_link, save_path):
    # Ensure the save path exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Command to run aria2c for downloading the magnet link
    command = [
        'aria2c',
        '--dir=' + save_path,       # Download directory
        '--continue=true',          # Continue incomplete downloads
        '--max-download-limit=0',   # No speed limit (change if needed)
        '--max-connection-per-server=4',  # Max connections per server
        '--console-log-level=error',   # Suppress extra logs
        '--enable-mmap=true',      # Enable memory mapping for larger files
        magnet_link                  # Magnet link
    ]
    
    # Run aria2c in subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Track download progress
    total_size = 0
    with tqdm(total=total_size, unit='B', unit_scale=True, ncols=100, desc="Downloading") as pbar:
        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                decoded_output = output.decode('utf-8').strip()

                # Look for the download progress pattern in aria2's output
                if 'Download progress' in decoded_output:
                    # Extract download progress from output
                    progress = decoded_output.split()[-2]  # Extract progress percentage
                    total_size = int(decoded_output.split()[-4])  # Get total size (in bytes)
                    
                    # Update tqdm progress bar
                    pbar.total = total_size  # Set the total size once known
                    pbar.update(int(progress))

                print(decoded_output)  # Optional: for debugging to see aria2's full output

    # Wait for the process to finish
    process.wait()

    print(f"Download completed! Files saved in: {save_path}")

def main():
    # Ask the user for the magnet link
    magnet_link = input("Please enter the magnet link: ")

    # Set the save path (can be changed as needed)
    save_path = os.path.expanduser("~/Downloads")  # Default download folder

    # Start the download
    download_magnet_aria2(magnet_link, save_path)

if __name__ == "__main__":
    main()
