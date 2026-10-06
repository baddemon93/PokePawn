import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


def load_env():
    """Load PokePawn credentials from the local .env file."""

    env_file = Path(__file__).parent / ".env"

    if not env_file.exists():
        raise FileNotFoundError(
            "Could not find .env file in the PokePawn directory."
        )

    for line in env_file.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)

        key = key.strip()
        value = value.strip()

        os.environ.setdefault(key, value)


def send_email(subject, body):
    """Send a PokePawn notification through Gmail."""

    load_env()

    gmail_address = os.environ.get("GMAIL_ADDRESS")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    alert_email = os.environ.get("ALERT_EMAIL")

    if not gmail_address:
        raise RuntimeError("GMAIL_ADDRESS is missing from .env")

    if not app_password:
        raise RuntimeError("GMAIL_APP_PASSWORD is missing from .env")

    if not alert_email:
        raise RuntimeError("ALERT_EMAIL is missing from .env")

    # Google App Passwords are sometimes displayed with spaces.
    # Remove any spaces before authentication.
    app_password = app_password.replace(" ", "")

    msg = EmailMessage()

    msg["From"] = gmail_address
    msg["To"] = alert_email
    msg["Subject"] = subject

    msg.set_content(body)

    print("Connecting to Gmail...")

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:

        smtp.ehlo()

        print("Starting secure connection...")

        smtp.starttls()

        smtp.ehlo()

        print("Authenticating...")

        smtp.login(
            gmail_address,
            app_password,
            initial_response_ok=False
        )

        print("Sending email...")

        smtp.send_message(msg)

    print("Email sent successfully!")


if __name__ == "__main__":

    send_email(
        "PokePawn Test Alert",
        """
PokePawn email notifications are working!

Discord: ONLINE
Email: ONLINE

Your Pokemon TCG restock monitor can now send email alerts.

This is a test message from PokePawn.
""".strip()
    )
