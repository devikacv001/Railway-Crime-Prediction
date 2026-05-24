import os
import requests
from tkinter import messagebox
from dotenv import load_dotenv

load_dotenv()  # optional: reads .env in project root

# Replace hard-coded secrets with environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

# Allow multiple recipients via comma-separated env var (TWILIO_TO_NUMBER or TWILIO_RECIPIENTS)
_recipients_env = os.getenv("TWILIO_TO_NUMBER") or os.getenv("TWILIO_RECIPIENTS") or ""
RECIPIENTS = [n.strip() for n in _recipients_env.split(",") if n.strip()]

# Optional IP geolocation key (do NOT commit real key)
IPSTACK_ACCESS_KEY = os.getenv("IPSTACK_ACCESS_KEY")

if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER and RECIPIENTS):
    def send_emergency_alert(*args, **kwargs):
        # Minimal safe behavior when Twilio or recipients aren't configured
        msg = ("Twilio credentials or recipient numbers are not configured. "
               "Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER and TWILIO_TO_NUMBER in environment (do NOT commit .env).")
        try:
            messagebox.showwarning("Configuration Missing", msg)
        except Exception:
            print(msg)
else:
    from twilio.rest import Client

    def send_emergency_alert(message="Emergency! Please respond."):
        """
        Sends an emergency SMS using Twilio.
        Environment variables used:
         - TWILIO_ACCOUNT_SID
         - TWILIO_AUTH_TOKEN
         - TWILIO_FROM_NUMBER
         - TWILIO_TO_NUMBER (comma-separated) or TWILIO_RECIPIENTS
         - IPSTACK_ACCESS_KEY (optional) — DO NOT commit this key
        """
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        try:
            loc_msg = ""
            if IPSTACK_ACCESS_KEY:
                try:
                    url = f"http://api.ipstack.com/check?access_key={IPSTACK_ACCESS_KEY}"
                    response = requests.get(url, timeout=5)
                    data = response.json()
                    if 'latitude' in data and 'longitude' in data:
                        lat, lon = data['latitude'], data['longitude']
                        maps_url = f"https://www.google.com/maps?q={lat},{lon}"
                        loc_msg = f"\nLocation: {maps_url}"
                except Exception:
                    # don't fail the entire flow if location fetch fails
                    loc_msg = "\nLocation: (unavailable)"

            final_message = f"🚨 Panic Button Triggered!{loc_msg}\n{message}"

            for number in RECIPIENTS:
                client.messages.create(
                    body=final_message,
                    from_=TWILIO_FROM_NUMBER,
                    to=number
                )

            try:
                messagebox.showinfo("Success", "SMS alerts sent successfully!")
            except Exception:
                print("SMS alerts sent successfully!")
        except Exception as e:
            try:
                messagebox.showerror("Error", f"Failed to send SMS: {str(e)}")
            except Exception:
                print("Failed to send SMS:", e)
