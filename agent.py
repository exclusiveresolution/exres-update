#!/usr/bin/env python3
"""
Self-Updating Python AI Agent
"""
import os
import sys
import shutil
import requests

VERSION = "1.0.0"
UPDATE_URL = "https://yourdomain.com/agent.py"
VERSION_INFO_URL = "https://yourdomain.com/agent_version.txt"

def check_for_update():
    try:
        resp = requests.get(VERSION_INFO_URL, timeout=5)
        resp.raise_for_status()
        latest_version, description = resp.text.strip().split("|")
        if latest_version > VERSION:
            return latest_version, description
    except Exception as e:
        print(f"[Update] Could not retrieve version info: {e}")
    return None

def download_update():
    try:
        resp = requests.get(UPDATE_URL, timeout=10)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[Update] Failed to download update: {e}")
        return None

def apply_update(new_code):
    current_file = os.path.abspath(__file__)
    backup_file = current_file + ".bak"
    shutil.copy(current_file, backup_file)
    try:
        with open(current_file, "w", encoding="utf-8") as f:
            f.write(new_code)
    except Exception as e:
        shutil.copy(backup_file, current_file)
        print(f"[Update] Failed to write new code, rolled back: {e}")
        return False
    return True

def restart_agent():
    os.execv(sys.executable, [sys.executable] + sys.argv)

def propose_and_apply_update(latest_version, description):
    print(f"Update v{latest_version}: {description}")
    choice = input("Apply update? [y/N]: ").strip().lower()
    if choice != 'y':
        print("[Update] Canceled.")
        return False
    new_code = download_update()
    if new_code and apply_update(new_code):
        print("[Update] Restarting...")
        restart_agent()
    else:
        print("[Update] Update failed.")
    return False

if __name__ == "__main__":
    print(f"Running version {VERSION}")
    update_info = check_for_update()
    if update_info:
        latest_version, description = update_info
        propose_and_apply_update(latest_version, description)
    else:
        print("No update found.")