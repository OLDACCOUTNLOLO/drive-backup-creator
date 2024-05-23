import os
import subprocess
import platform
import string
import random

def get_available_drive_letter():
    used_drives = subprocess.check_output('wmic logicaldisk get name', shell=True).decode().split()
    used_drives = [drive.strip(':') for drive in used_drives if drive]
    for letter in string.ascii_uppercase:
        if letter not in used_drives:
            return letter
    raise RuntimeError("No available drive letters.")

def create_virtual_drive_windows():
    # Define a unique folder path and drive letter
    unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    folder_path = f"C:\\dummy_drive_{unique_id}"
    drive_letter = get_available_drive_letter() + ":"

    # Create the folder
    os.makedirs(folder_path)

    # Use the subst command to create a virtual drive
    os.system(f"subst {drive_letter} {folder_path}")

    # Set the label of the virtual drive
    os.system(f"label {drive_letter} New Disk")

    print(f"Virtual drive {drive_letter} created and labeled 'New Disk'.")

def create_virtual_drive_linux():
    # Define a unique image file and mount point
    unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    image_file = f"dummy_{unique_id}.img"
    mount_point = f"/mnt/dummy_drive_{unique_id}"

    # Create a 1GB empty file
    subprocess.run(["dd", "if=/dev/zero", f"of={image_file}", "bs=1M", "count=1024"])

    # Format the file with a filesystem
    subprocess.run(["mkfs.ext4", image_file])

    # Label the filesystem
    subprocess.run(["e2label", image_file, "New Disk"])

    # Create the mount point
    os.makedirs(mount_point)

    # Mount the file as a loopback device
    subprocess.run(["sudo", "mount", "-o", "loop", image_file, mount_point])

    print(f"Loopback device mounted at {mount_point} and labeled 'New Disk'.")

if __name__ == "__main__":
    os_type = platform.system()
    if os_type == "Windows":
        create_virtual_drive_windows()
    elif os_type == "Linux":
        create_virtual_drive_linux()
    else:
        print(f"Unsupported operating system: {os_type}")
