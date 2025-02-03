
import subprocess
import shutil
import sys
import time
import signal
import threading
import os
import json
import requests

# Configuration
model_name = "deepseek-r1:8b"
ngrok_auth_token = None
ngrok_url = None

# Step 1: Install Ollama
def install_ollama():
    print("📥 Installing Ollama...")
    try:
        subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
        print("✅ Ollama installed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install Ollama:", e)
        sys.exit(1)

def check_ollama_installed():
    if shutil.which("ollama") is None:
        print("⚠️ Ollama is not installed. Installing now...")
        install_ollama()
    else:
        print("✅ Ollama is already installed.")

# Step 2: Start Ollama Server
def start_ollama_server():
    print("🚀 Starting Ollama Server...")
    process = subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    max_retries = 10
    for _ in range(max_retries):
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama server is running.")
                return process
        except requests.exceptions.ConnectionError:
            print("⏳ Waiting for Ollama server...")
            time.sleep(5)
    print("❌ Ollama server failed to start.")
    process.terminate()
    sys.exit(1)

# Step 3: Download Model
def check_model_downloaded():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        models = response.json().get("models", [])
        return any(model["name"] == model_name for model in models)
    except requests.exceptions.RequestException:
        return False

def pull_model():
    print(f"📥 Downloading model: {model_name}")
    try:
        response = requests.post("http://localhost:11434/api/pull", json={"name": model_name}, stream=True, timeout=300)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                try:
                    json_data = json.loads(decoded)
                    if 'status' in json_data:
                        print(f"🔄 Status: {json_data['status']}")
                except json.JSONDecodeError:
                    continue
        print(f"✅ Model '{model_name}' downloaded successfully.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading model: {e}")
        sys.exit(1)

# Step 4: Install Open WebUI
def install_open_webui():
    print("📥 Installing Open WebUI...")
    try:
        subprocess.run("curl -LsSf https://astral.sh/uv/install.sh | sh", shell=True, check=True)
        print("✅ Open WebUI installed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install Open WebUI:", e)
        sys.exit(1)

# Step 5: Start Open WebUI on Port 8081
def start_open_webui():
    print("🚀 Starting Open WebUI on port 8081...")
    process = subprocess.Popen(
        "DATA_DIR=~/.open-webui uvx --python 3.11 open-webui@latest serve --host 0.0.0.0 --port 8081",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(5)
    print("✅ Open WebUI is running on port 8081.")
    return process

# Step 6: Install ngrok
def install_ngrok():
    print("📥 Installing ngrok...")
    try:
        subprocess.run("curl -fsSL https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-amd64.zip -o ngrok.zip", shell=True, check=True)
        subprocess.run("unzip -o ngrok.zip", shell=True, check=True)
        subprocess.run("mv ngrok /usr/local/bin", shell=True, check=True)
        print("✅ ngrok installed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install ngrok:", e)
        sys.exit(1)

def check_ngrok_installed():
    if shutil.which("ngrok") is None:
        print("⚠️ ngrok is not installed. Installing now...")
        install_ngrok()
    else:
        print("✅ ngrok is already installed.")

# Step 7: Start ngrok
def get_ngrok_auth_token():
    global ngrok_auth_token
    ngrok_auth_token = os.environ.get("NGROK_AUTH_TOKEN")
    if not ngrok_auth_token:
        ngrok_auth_token = input("Enter Your Ngrok Token").strip()
        os.environ["NGROK_AUTH_TOKEN"] = ngrok_auth_token
    return ngrok_auth_token

def start_ngrok():
    global ngrok_url
    print("🚀 Starting ngrok tunnel for Open WebUI (port 8081)...")

    auth_token = get_ngrok_auth_token()
    subprocess.run(f"ngrok config add-authtoken {auth_token}", shell=True, check=True)

    ngrok_process = subprocess.Popen(["ngrok", "http", "8081"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(5)
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        tunnels = response.json().get("tunnels", [])
        if tunnels:
            ngrok_url = tunnels[0]["public_url"]
            print(f"✅ ngrok is running at: {ngrok_url}")
            return ngrok_process
    except requests.exceptions.RequestException:
        print("❌ Failed to retrieve ngrok URL.")
        sys.exit(1)

# Clean shutdown
def handle_exit(signum, frame):
    print("\n🛑 Stopping services...")
    sys.exit(0)

# Initialize and run all services
def initialize_services():
    check_ollama_installed()
    check_ngrok_installed()
    install_open_webui()

    ollama_process = start_ollama_server()
    if not check_model_downloaded():
        pull_model()

    open_webui_process = start_open_webui()
    ngrok_process = start_ngrok()

    return ollama_process, open_webui_process, ngrok_process

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    ollama_process, open_webui_process, ngrok_process = initialize_services()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle_exit(None, None)
