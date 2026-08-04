import os
import logging
from email.message import EmailMessage
import aiosmtplib
from jinja2 import Template
import base64

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

async def send_email(to_email: str, subject: str, html_content: str, inline_images: dict = None):
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning(f"SMTP credentials missing. Would have sent email to {to_email} with subject: {subject}")
        return

    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content("Please enable HTML to view this email.")
    message.add_alternative(html_content, subtype="html")

    if inline_images:
        html_part = message.get_payload()[1]
        for cid, b64_data in inline_images.items():
            img_data = base64.b64decode(b64_data)
            html_part.add_related(img_data, maintype='image', subtype='png', cid=f"<{cid}>")

    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            use_tls=True if SMTP_PORT == 465 else False,
            start_tls=True if SMTP_PORT == 587 else False,
        )
        logger.info(f"Email sent successfully to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")

async def send_verification_email(to_email: str, token: str):
    import time
    from datetime import datetime
    
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    verification_url = f"{FRONTEND_URL}/verify-email?token={token}"
    
    template = Template("""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f5; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h2 style="color: #1e3a8a; margin-top: 0;">Welcome to Advance eSIM!</h2>
                <p style="color: #4b5563; font-size: 16px; line-height: 1.5;">
                    Please confirm your email address by clicking the button below. This ensures you can securely receive your eSIM QR codes.
                </p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{{ url }}" style="background-color: #2563eb; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
                        Verify Email Address
                    </a>
                </div>
                <p style="color: #9ca3af; font-size: 14px; text-align: center; margin-bottom: 0;">
                    Request generated at: {{ time }}<br/>
                    If you did not request this, you can safely ignore this email.
                </p>
            </div>
        </body>
    </html>
    """)
    
    html_content = template.render(url=verification_url, time=current_time_str)
    # Using a unique subject prevents Gmail from threading and collapsing the entire content
    await send_email(to_email, f"Verify your Advance eSIM account [{int(time.time())}]", html_content)



async def send_receipt_email(to_email: str, order_details: dict):
    # order_details should contain country_name, data_gb, duration_days, iccid, activation_code, qr_code_base64
    template = Template("""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f5; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h2 style="color: #1e3a8a; margin-top: 0; text-align: center;">Your eSIM is Ready! 🚀</h2>
                
                <p style="color: #4b5563; font-size: 16px; line-height: 1.5;">
                    Thank you for your purchase! Your <strong>{{ country }} {{ data }}GB / {{ duration }} Days</strong> eSIM has been successfully activated.
                </p>
                
                <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #334155; font-size: 16px; text-transform: uppercase;">Installation Details</h3>
                    <p style="margin: 8px 0; color: #475569;"><strong>ICCID:</strong> <code style="background-color: #e2e8f0; padding: 2px 6px; border-radius: 4px;">{{ iccid }}</code></p>
                    <p style="margin: 8px 0; color: #475569;"><strong>Activation Code:</strong> <code style="background-color: #e2e8f0; padding: 2px 6px; border-radius: 4px;">{{ activation_code }}</code></p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <h4 style="margin-bottom: 16px; color: #475569;">Scan to Install</h4>
                    <img src="cid:qr_code" alt="eSIM QR Code" style="width: 250px; height: 250px; border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px; background: white;" />
                </div>
                
                <p style="color: #64748b; font-size: 14px; line-height: 1.5;">
                    <strong>To install:</strong> Go to your phone's Settings > Cellular/Mobile Data > Add eSIM, and scan the QR code above.
                </p>
            </div>
        </body>
    </html>
    """)
    
    html_content = template.render(
        country=order_details.get("country_name"),
        data=order_details.get("data_gb"),
        duration=order_details.get("duration_days"),
        iccid=order_details.get("esim_iccid"),
        activation_code=order_details.get("esim_activation_code")
    )
    
    inline_images = None
    qr_b64 = order_details.get("esim_qr_code")
    if qr_b64:
        inline_images = {"qr_code": qr_b64}
    
    await send_email(to_email, f"Your {order_details.get('country_name')} eSIM", html_content, inline_images=inline_images)
