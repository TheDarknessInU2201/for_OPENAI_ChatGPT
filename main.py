import gc
import platform



system = platform.system()
def get_partition_and_mountpoints():
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
        return drives

    else:
        import subprocess
        df = subprocess.check_output(["df", "-h"]).decode()
        drives = df.strip().split("\n")
        drives = [d for d in drives if "/" in d and not d.startswith("tmpfs") and not d.startswith("udev") and not d.startswith("overlay") and not d.startswith("aufs")]
        drives = [d.split()[0] + " " + d.split()[5] for d in drives]
        drives = [d for d in drives if "snapd" not in d and "docker" not in d ]
        drive_partition = [d.split()[0] for d in drives]
        drive_mount = [d.split()[1] for d in drives]

        drive_partition = [d for d in drive_partition if d != "dev" and d != "run"]
        drive_mount = [d for d in drive_mount if d != "/dev" and d != "/run"]

        #print("Partitionen: ",drive_partition)
        #print("Mountpoints: ",drive_mount)
        return drive_partition, drive_mount

def main():

    partitions, mountpoints = get_partition_and_mountpoints()
    print("  ")
    print("Partitionen: ", partitions)
    print("Mountpoints: ", mountpoints)

    gc.collect()

if __name__ == "__main__":
    main()
