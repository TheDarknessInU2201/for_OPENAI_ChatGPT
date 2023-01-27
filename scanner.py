import os
import json
import platform
import subprocess

def find_files_by_type(directory, file_type):
    current_system = platform.system()
    admin_access = False
    if current_system == 'Windows':
        # Anfordern von Adminrechten
        try:
            subprocess.check_call(['runas', '/user:Administrator', 'python', '-c', 'import os; print(os.geteuid())'])
            admin_access = True
        except:
            pass
    elif current_system == 'Linux':
        try:
            subprocess.check_call(['pkexec', 'python', '-c', 'import os; print(os.geteuid())'])
            admin_access = True
        except:
            pass
    elif current_system == 'Darwin': # MacOS
        try:
            subprocess.check_call(['osascript', '-e', 'do shell script "python -c \\"import os; print(os.geteuid())\\"" with administrator privileges'])
            admin_access = True
        except:
            pass
    else:
        print("Unsupported platform")
        return
    if admin_access:
        matches = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(file_type):
                    matches.append(os.path.join(root, file))
        try:
            with open("found_files.json", "r") as json_file:
                existing_data = json.load(json_file)
                existing_data.extend(matches)
                matches = existing_data
        except:
            pass
        with open("found_files.json", "w") as json_file:
            json.dump(matches, json_file, indent=4)
    else:
        print("Admin access is required to run this function")
    return matches
