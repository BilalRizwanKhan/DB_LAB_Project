import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD, EMAIL_FROM

def send_email(to: str, subject: str, body: str):
    """Send an HTML email. Silently fails if email is not configured."""
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print(f"[EMAIL] Not configured — skipping email to {to}: {subject}")
        return
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = EMAIL_FROM
        msg["To"]      = to
        msg.attach(MIMEText(body, "html"))
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, to, msg.as_string())
        print(f"[EMAIL] Sent to {to}: {subject}")
    except Exception as e:
        print(f"[EMAIL] Failed to send to {to}: {e}")

# ── Email Templates ──────────────────────────────────────────────

def email_welcome(name: str, email: str):
    send_email(email, "Welcome to DreamHomes! 🏡", f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:30px;background:#f5f5f5;border-radius:10px;">
        <h2 style="color:#0d1b2a;">Welcome to DreamHomes, {name}!</h2>
        <p>Your account has been created successfully.</p>
        <p>You can now browse properties, save favorites, post listings, and more.</p>
        <a href="http://localhost:8000" style="background:#00b4d8;color:white;padding:12px 25px;text-decoration:none;border-radius:5px;display:inline-block;margin-top:15px;">
            Visit DreamHomes
        </a>
        <p style="color:gray;margin-top:20px;font-size:13px;">© 2026 DreamHomes</p>
    </div>""")

def email_inquiry_received(seller_name: str, seller_email: str, buyer_name: str, property_title: str):
    send_email(seller_email, f"New Inquiry on '{property_title}'", f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:30px;background:#f5f5f5;border-radius:10px;">
        <h2 style="color:#0d1b2a;">Hi {seller_name},</h2>
        <p><strong>{buyer_name}</strong> has sent an inquiry about your property <strong>"{property_title}"</strong>.</p>
        <a href="http://localhost:8000/static/inquiries.html" style="background:#00b4d8;color:white;padding:12px 25px;text-decoration:none;border-radius:5px;display:inline-block;margin-top:15px;">
            View Inquiry
        </a>
        <p style="color:gray;margin-top:20px;font-size:13px;">© 2026 DreamHomes</p>
    </div>""")

def email_inquiry_replied(buyer_name: str, buyer_email: str, property_title: str):
    send_email(buyer_email, f"Reply to your inquiry on '{property_title}'", f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:30px;background:#f5f5f5;border-radius:10px;">
        <h2 style="color:#0d1b2a;">Hi {buyer_name},</h2>
        <p>The seller has replied to your inquiry about <strong>"{property_title}"</strong>.</p>
        <a href="http://localhost:8000/static/inquiries.html" style="background:#00b4d8;color:white;padding:12px 25px;text-decoration:none;border-radius:5px;display:inline-block;margin-top:15px;">
            View Reply
        </a>
        <p style="color:gray;margin-top:20px;font-size:13px;">© 2026 DreamHomes</p>
    </div>""")

def email_appointment_booked(user_name: str, user_email: str, property_title: str, visit_date: str, visit_time: str):
    send_email(user_email, f"Appointment Confirmed — {property_title}", f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:30px;background:#f5f5f5;border-radius:10px;">
        <h2 style="color:#0d1b2a;">Hi {user_name},</h2>
        <p>Your visit appointment for <strong>"{property_title}"</strong> has been booked.</p>
        <table style="margin-top:15px;border-collapse:collapse;">
            <tr><td style="padding:8px;font-weight:bold;">Date:</td><td style="padding:8px;">{visit_date}</td></tr>
            <tr><td style="padding:8px;font-weight:bold;">Time:</td><td style="padding:8px;">{visit_time}</td></tr>
        </table>
        <a href="http://localhost:8000/static/appointments.html" style="background:#00b4d8;color:white;padding:12px 25px;text-decoration:none;border-radius:5px;display:inline-block;margin-top:15px;">
            View Appointments
        </a>
        <p style="color:gray;margin-top:20px;font-size:13px;">© 2026 DreamHomes</p>
    </div>""")
