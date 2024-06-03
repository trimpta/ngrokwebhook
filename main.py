import os
import time
import json
import argparse
import requests
from pyngrok import ngrok

# Load configuration from config.json
def load_config():
    with open("config.json", "r") as config_file:
        return json.load(config_file)

# Function to post message to Discord webhook
def post_to_discord(webhook_url, message):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Successfully posted to Discord")
    else:
        print(f"Failed to post to Discord: {response.status_code}, {response.text}")

def main(port):
    # Load configuration
    config = load_config()
    NGROK_AUTH_TOKEN = config["ngrok_auth_token"]
    DISCORD_WEBHOOK_URL = config["discord_webhook_url"]
    
    # Authenticate ngrok
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    
    # Start the ngrok tunnel
    print(f"Starting ngrok tunnel on port {port}...")
    tunnel = ngrok.connect(port, "tcp")
    public_url = tunnel.public_url.replace("tcp://", "")
    print(f"ngrok tunnel started: {public_url}")
    
    # Post the ngrok public URL to Discord
    message = f"Remote Desktop is available at: {public_url}"
    post_to_discord(DISCORD_WEBHOOK_URL, message)
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down ngrok tunnel...")
        ngrok.disconnect(tunnel.public_url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start ngrok tunnel and post URL to Discord.")
    parser.add_argument("--port", type=int, required=True, help="Port to expose via ngrok")
    args = parser.parse_args()
    main(args.port)