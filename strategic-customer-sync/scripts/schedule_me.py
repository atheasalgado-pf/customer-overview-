import os
import sys
import subprocess

def schedule_mac_linux():
    # Get the absolute path of the daily_sync script
    project_dir = os.getcwd()
    sync_script = os.path.join(project_dir, "strategic-customer-sync", "scripts", "daily_sync.py")
    python_path = sys.executable
    log_path = os.path.join(project_dir, "sync.log")

    if not os.path.exists(sync_script):
        print(f"Error: Could not find sync script at {sync_script}")
        print("Please run this script from the root of the 'customer-overview' repository.")
        return

    # The crontab entry (Runs at 2:00 AM daily)
    cron_entry = f"0 2 * * * cd {project_dir} && {python_path} {sync_script} >> {log_path} 2>&1"

    try:
        # Get existing crontab
        current_cron = subprocess.check_output("crontab -l", shell=True, stderr=subprocess.DEVNULL).decode()
    except subprocess.CalledProcessError:
        current_cron = ""

    if sync_script in current_cron:
        print("Daily sync is already scheduled in crontab.")
        return

    # Add new entry
    new_cron = current_cron + cron_entry + "\n"
    
    # Write back to crontab
    process = subprocess.Popen("crontab -", stdin=subprocess.PIPE, shell=True)
    process.communicate(input=new_cron.encode())

    if process.returncode == 0:
        print(f"[SUCCESS] Daily sync scheduled for 2:00 AM.")
        print(f"Logs will be written to: {log_path}")
    else:
        print("[ERROR] Failed to update crontab.")

def main():
    print("--- Strategic Customer Sync: Auto-Scheduler ---")
    
    if sys.platform == "darwin" or sys.platform.startswith("linux"):
        schedule_mac_linux()
    elif sys.platform == "win32":
        print("Windows detected. Auto-scheduling for Windows is currently a manual step via Task Scheduler.")
        print("Please see the instructions in SKILL.md under 'Windows (Task Scheduler)'.")
    else:
        print(f"Unsupported platform: {sys.platform}")

if __name__ == "__main__":
    main()
