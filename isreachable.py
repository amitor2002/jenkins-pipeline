import requests

def check_url(name, url):
    try:
        print(f"🔍 Checking {name} at {url}")
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            print(f"✅ {name} is UP!")
            return True
        else:
            print(f"⚠️ {name} responded with status code: {res.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name} is DOWN! Error: {e}")
        return False

if __name__ == "__main__":
    REMOTE_IP = '3.93.188.22'
    local_ok = check_url("Local Container", "http://localhost:5000")
    remote_ok = check_url("Remote Production", f"http://{REMOTE_IP}:5000")

    if not local_ok or not remote_ok:
        exit(1)
        
