import subprocess
import requests
import random

# Constants
stop_script = 'scripts/stop.sh'
saving_folder = 'nessus_reports'

# Step 1 : SAVE -    download all *.nessus reports
# Step 2 : STOP -    stop daemon and rm -rf /opt/nessus
# Step 3 : INSTALL - re install from .deb (download if wrong checksum) and start daemon
# Step 4 : SET -     generate trial code, activate and set eveyrthing
# Step 5 : RESTORE - restore all *.nessus reports

def save():
    print("Saving Nessus reports")
    try:
        # todo
        pass
    except subprocess.CalledProcessError as e:
        print("Erreur :", e.stderr)

def stop():
    print("Stopping Nessus daemon")
    try:
        result = subprocess.run(['sudo', 'bash', stop_script], check=True, capture_output=True, text=True)
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Erreur :", e.stderr)


def main():
    stop()

if __name__ == '__main__':
    main()