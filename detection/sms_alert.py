# detection/sms_alert.py

from twilio.rest import Client
import config  
import time

LAST_SMS_TIME = 0
COOLDOWN_PERIOD = 300 

def send_drowsiness_alert():
    global LAST_SMS_TIME

    current_time = time.time()

    if (current_time - LAST_SMS_TIME) > COOLDOWN_PERIOD:
        try:
            LAST_SMS_TIME = current_time

          
            client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

            message = client.messages.create(
                body="ALERT: Drowsiness detected in driver!",
                from_=config.TWILIO_PHONE_NUMBER,
                to=config.MY_PHONE_NUMBER
            )

            print(f"[INFO] SMS Alert Sent! SID: {message.sid}")

        except Exception as e:
            print(f"[ERROR] Failed to send SMS: {e}")
    else:
        print("[INFO] SMS on cooldown, not sending alert.")