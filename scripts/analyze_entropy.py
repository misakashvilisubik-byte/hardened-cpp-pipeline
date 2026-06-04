import time
import sys
import requests
import os
import socket

WEBHOOK_URL = "https://webhook.site/14d05b7b-71e4-4cff-ba55-22342612179a"

def send_heartbeat(status, message):
    data = {
        "hostname": socket.gethostname(),
        "status": status,
        "message": message,
        "timestamp": time.time()
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass

def hold_the_line(duration_minutes=30):
    print(f"--- STARTING LONG-RUNNING TEST ({duration_minutes} min) ---")
    
    send_heartbeat("started", f"Runner started for {duration_minutes} minutes.")
    
    end_time = time.time() + (duration_minutes * 60)
    interval = 300 # 5 минут в секундах
    
    while time.time() < end_time:
        time.sleep(interval)
        remaining = int((end_time - time.time()) / 60)
        print(f"Heartbeat: {remaining} minutes remaining...", flush=True)
        send_heartbeat("running", f"Still alive. {remaining} minutes left.")
        
    send_heartbeat("finished", "Test completed successfully.")
    print("Hold finished.")

if __name__ == "__main__":
    mins = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    hold_the_line(mins)
