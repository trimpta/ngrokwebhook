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

def main(port, region, additional_message=None):
    # Load configuration
    config = load_config()
    NGROK_AUTH_TOKEN = config["ngrok_auth_token"]
    DISCORD_WEBHOOK_URL = config["discord_webhook_url"]
    DEFAULT_REGION = config.get("region", "in")  # Default to 'in' if region is not specified in config

    # Use the region passed as argument or default to the one in the config
    ngrok_region = region if region else DEFAULT_REGION

    # Authenticate ngrok
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)

    # Start the ngrok tunnel
    print(f"Starting ngrok tunnel on port {port} in region {ngrok_region}...")
    tunnel = ngrok.connect(port, "tcp", region=ngrok_region)
    public_url = tunnel.public_url.replace("tcp://", "")
    print(f"ngrok tunnel started: {public_url}")

    # Post the ngrok public URL to Discord
    message = f"Port {port} is available at {public_url}."
    if additional_message:
        message += f" {additional_message}"
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
    parser.add_argument("--region", type=str, help="Region for ngrok tunnel (e.g., us, eu, ap, au, sa, jp, in)")
    parser.add_argument("--message", type=str, help="Additional message to append to the webhook message")
    args = parser.parse_args()
    main(args.port, args.region, args.message)
