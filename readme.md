# Remote Desktop Access via Ngrok and Discord Notification

This project allows you to set up a remote desktop access tunnel using ngrok and notifies you via a Discord webhook with the public URL.

## Prerequisites

- Python 3.x
- Pip (Python package installer)

## Setup

1. **Clone the Repository**
   ```sh
   git clone https://your-repository-url.git
   cd your-repository-folder
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure Settings**
   - Create a file named `config.json` in the project directory.
   - Add your ngrok authentication token and Discord webhook URL to `config.json`:

     ```json
     {
         "ngrok_auth_token": "your_ngrok_auth_token_here",
         "discord_webhook_url": "your_discord_webhook_url_here"
     }
     ```

## Usage

1. **Run the Script**
   ```sh
   python your_script_name.py --port PORT_NUMBER
   ```

   Replace `PORT_NUMBER` with the port you want to expose via ngrok.

2. **Access Remote Desktop**
   - The script will start an ngrok tunnel on the specified port and post the public URL to your Discord webhook.
   - Use the URL provided in the Discord message to connect to your remote desktop.
