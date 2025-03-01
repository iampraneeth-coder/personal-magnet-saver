#!/usr/bin/env python3

import libtorrent as lt
import time
import os
import argparse

def download_magnet_libtorrent(magnet_link, download_dir):
    """Downloads a magnet link using libtorrent with a progress bar.

    Args:
        magnet_link (str): The magnet link to download.
        download_dir (str): The directory to save the downloaded files.
    """
    try:
        # Create a session
        session = lt.session()

        # Add magnet link
        params = {
            'save_path': download_dir,
            'storage_mode': lt.storage_mode_t.storage_mode_sparse, #Allocate space as needed
        }

        handle = lt.add_magnet_uri(session, magnet_link, params)

        print(f"Downloading to: {download_dir}")
        print(f"Magnet link: {magnet_link}")

        # Start the download
        session.start_dht() #DHT is needed for P2P to work, so enabling this first.

        print("\nStarting download...")

        # Track progress
        while (handle.status().state != lt.torrent_status.seeding): #While the torrent is still running
            s = handle.status() #Torrent status

            downloaded = s.total_done  # Bytes downloaded
            total = s.total  # Total bytes in torrent

            percentage = downloaded * 100 / total #percentage calculation

            print(f"Progress: {percentage:.1f}%  |  Down: {get_readable_size(downloaded)}  |  Total: {get_readable_size(total)}  |  Peers: {s.num_peers}", end='\r') #Overwrite
            time.sleep(1) #Sleep for a second

        print(f"\nDownload complete for: {handle.name()}")

    except Exception as e:
        print(f"An error occurred: {e}")

def get_readable_size(num_bytes):
    """Converts bytes to a human-readable format (KB, MB, GB)."""
    units = ['bytes', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while num_bytes >= 1024:
        num_bytes /= 1024
        i += 1
    return f"{num_bytes:.2f} {units[i]}"

if __name__ == "__main__":
    default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    print("Magnet Link Downloader (libtorrent)")
    magnet_link = input("Enter the magnet link: ")
    download_dir = input(f"Enter the download directory (default: {default_download_dir}): ")
    if not download_dir:
        download_dir = default_download_dir

    download_magnet_libtorrent(magnet_link, download_dir)
