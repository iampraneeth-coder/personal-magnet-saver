#!/usr/bin/env python3

import subprocess
import os
import time
import argparse

def download_magnet(magnet_link, download_dir, timeout=3600):
    """Downloads a magnet link using transmission-cli with a timeout.

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
            "-w", download_dir, # Set the download directory
            "-b"  # Run in background (optional)
        ]

        print(f"Starting download: {magnet_link} to {download_dir}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        start_time = time.time()
        while True:
            #Check if the download completed or time out
            return_code = process.poll()
            if return_code is not None:
                if return_code == 0:
                    print("Download completed successfully.")
                else:
                    print(f"Download failed with return code: {return_code}")
                    print("Stderr:", process.stderr.read()) # print out error messages
                break

            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print(f"Download timed out after {timeout} seconds.")
                process.terminate() # Terminate the process
                break

            time.sleep(10) #Check every 10 seconds

    except FileNotFoundError:
        print("Error: transmission-cli not found. Please install it.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a magnet link using transmission-cli.")
    parser.add_argument("magnet_link", help="The magnet link to download")
    parser.add_argument("download_dir", help="The directory to save the downloaded files")
    parser.add_argument("--timeout", type=int, default=3600, help="Maximum download time in seconds (default: 3600)")
    args = parser.parse_args()

    download_magnet(args.magnet_link, args.download_dir, args.timeout)
