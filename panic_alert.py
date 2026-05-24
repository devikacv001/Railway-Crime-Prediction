from twilio.rest import Client
from tkinter import messagebox
import requests

def send_emergency_alert():
    try:
        # Use ipstack API to get location
        access_key = '.........'
        url = f"http://api.ipstack.com/check?access_key={access_key}"
        response = requests.get(url)
        data = response.json()

        if 'latitude' in data and 'longitude' in data:
            lat, lon = data['latitude'], data['longitude']
            maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            message = f"🚨 Panic Button Triggered!\nLocation: {maps_url}"

            # Twilio SMS setup
            account_sid = '..................'
            auth_token = '........................'
            client = Client(account_sid, auth_token)

            # List of recipient phone numbers
            recipients = ['+.........']

            for number in recipients:
                client.messages.create(
                    body=message,
                    from_='+16674014493',  # Twilio number
                    to=number
                )

            messagebox.showinfo("Success", "SMS alerts sent successfully!")
        else:
            messagebox.showerror("Error", "Unable to fetch location.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send SMS: {str(e)}")
