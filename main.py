import platform

system = platform.system()

if system == "Windows":
    try:
        import wmi
    except ImportError:
        import subprocess
        subprocess.run(["pip", "install", "wmi"])
        import wmi
    c = wmi.WMI()
    drives = []
    for physical_disk in c.Win32_DiskDrive():
        for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
            for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                drives.append(logical_disk.Caption)

else:
    import subprocess
    df = subprocess.check_output(["df", "-h"]).decode()
    drives = df.strip().split("\n")
    drives = [d for d in drives if "/" in d and not d.startswith("tmpfs") and not d.startswith("udev") and not d.startswith("overlay") and not d.startswith("aufs")]
    drives = [d.split()[0] + " " + d.split()[5] for d in drives]
    drives = [d for d in drives if "snapd" not in d and "docker" not in d ]
    drive_partition = [d.split()[0] for d in drives]
    drive_mount = [d.split()[1] for d in drives]

print("Partitionen: ",drive_partition)
print("Mountpoints: ",drive_mount)
