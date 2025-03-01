#!/usr/bin/env python3

import subprocess
import os
import time
import argparse
import re

def get_readable_size(num_bytes):
    """Converts bytes to a human-readable format (KB, MB, GB)."""
    units = ['bytes', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while num_bytes >= 1024:
        num_bytes /= 1024
        i += 1
    return f"{num_bytes:.2f} {units[i]}"

def download_magnet(magnet_link, download_dir, timeout=3600):
    """Downloads a magnet link using transmission-cli with progress and timeout.

    Args:
        magnet_link (str): The magnet link to download.
        download_dir (str): The directory to save the downloaded files.
        timeout (int): Maximum download time in seconds (default: 1 hour).
    """
    try:
        # Create the download directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)

        # Construct the transmission-cli command
        command = [
            "transmission-cli",
            magnet_link,
            "-w", download_dir,  # Set the download directory
        ]

        print(f"Starting download: {magnet_link} to {download_dir}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) #Combined output

        start_time = time.time()
        downloaded_bytes = 0
        previous_line = "" #Used to prevent repeats

        while True:
            line = process.stdout.readline() #Get combined output instead of error
            if not line:
                return_code = process.poll()
                if return_code is not None:
                    if return_code == 0:
                        print("Download completed successfully.")
                    else:
                        print(f"Download failed with return code: {return_code}")
                    break
                elif time.time() - start_time > timeout:
                    print(f"Download timed out after {timeout} seconds.")
                    process.terminate()
                    break
                else:
                    time.sleep(1)  # Check every 1 second if no new output is available

            else: #Output Exists
               if line != previous_line: #Check if the current line isn't the previous line, to stop repeat messages
                   previous_line = line
                   match = re.search(r"(\d+(\.\d+)?)\s*(MB|GB)\s*of\s*(\d+(\.\d+)?)\s*(MB|GB)\s*\((\d+(\.\d+)?)%\)", line) #Regex from the transmission CLI Output
                   if match:
                       downloaded_size = float(match.group(1))
                       downloaded_unit = match.group(3)
                       total_size = float(match.group(4))
                       total_unit = match.group(6)
                       percentage = float(match.group(7))

                       print(f"Downloaded: {downloaded_size:.2f} {downloaded_unit} of {total_size:.2f} {total_unit} ({percentage:.2f}%)", end='\r') #Overwrite line.

        process.wait() #Wait for process to complete to kill process, to prevent zombie processes

    except FileNotFoundError:
        print("Error: transmission-cli not found. Please install it.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads") #Sets to current user.
    print("Magnet Link Downloader")
    magnet_link = input("Enter the magnet link: ")
    download_dir = input(f"Enter the download directory (default: {default_download_dir}): ")
    if not download_dir:
        download_dir = default_download_dir

    try:
        timeout = int(input("Enter the timeout in seconds (default: 3600): ") or 3600) #Defaults to 3600, or 1 hour
    except ValueError:
        print("Invalid timeout value. Using default timeout of 3600 seconds.")
        timeout = 3600

    download_magnet(magnet_link, download_dir, timeout)
