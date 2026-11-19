import email.message
import logging
import os
import smtplib
from typing import Any, Dict, List, Optional

logger = logging.getLogger("eventflow.email")


class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.smtp_from = os.getenv("SMTP_FROM", "EventFlow Campus Portal <no-reply@campus-eventflow.edu>")
        self.is_enabled = os.getenv("SMTP_ENABLED", "false").lower() in ("true", "1", "yes")

        # In-memory test/audit log of sent emails
        self.sent_emails: List[Dict[str, Any]] = []

    def clear_sent_box(self):
        self.sent_emails.clear()

    def send_email(self, to_email: str, subject: str, html_body: str) -> bool:
        """
        Send an HTML email via SMTP, or log to in-memory sent box if SMTP is not configured.
        """
        email_record = {
            "to": to_email,
            "subject": subject,
            "body": html_body,
            "status": "sent"
        }
        self.sent_emails.append(email_record)

        if not self.is_enabled or not self.smtp_user or not self.smtp_password:
            logger.info(f"[Email Preview] To: {to_email} | Subject: {subject} | HTML length: {len(html_body)}")
            return True

        try:
            msg = email.message.EmailMessage()
            msg["Subject"] = subject
            msg["From"] = self.smtp_from
            msg["To"] = to_email
            msg.set_content(html_body, subtype="html")

            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
                logger.info(f"Successfully sent live email via SMTP to {to_email}")
            return True
        except Exception as e:
            logger.warning(f"SMTP send failed to {to_email}: {e}. Retaining email in audit log.")
            return False


email_service = EmailService()


def send_registration_confirmation(
    to_email: str,
    participant_name: str,
    event_title: str,
    ticket_code: str,
    event_date: str = "TBD",
    event_time: str = "TBD",
    event_venue: str = "Campus Hall",
    qr_data_url: Optional[str] = None,
) -> bool:
    """
    Generate and dispatch a styled HTML registration pass email.
    """
    subject = f"Registration Confirmed: {event_title} ({ticket_code})"
    qr_img_tag = (
        f'<div style="text-align: center; margin: 20px 0;"><img src="{qr_data_url}" alt="Ticket QR Code" style="width: 180px; height: 180px; border-radius: 8px; border: 1px solid #CBD5E1; padding: 6px; background: #fff;" /></div>'
        if qr_data_url
        else ""
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>{subject}</title>
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #F8FAFC; padding: 24px; color: #1E293B;">
      <div style="max-width: 580px; margin: 0 auto; background: #FFFFFF; border-radius: 12px; overflow: hidden; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
        <div style="background: linear-gradient(135deg, #1A365D 0%, #2563EB 100%); padding: 24px; text-align: center; color: white;">
          <h1 style="margin: 0; font-size: 22px; font-weight: 700; letter-spacing: -0.02em;">EVENTFLOW CAMPUS PASS</h1>
          <p style="margin: 6px 0 0 0; opacity: 0.9; font-size: 13px;">Official Digital Registration Pass</p>
        </div>
        <div style="padding: 24px;">
          <p style="margin-top: 0; font-size: 15px;">Dear <strong>{participant_name}</strong>,</p>
          <p style="font-size: 14px; line-height: 1.5; color: #475569;">
            Your registration for <strong>{event_title}</strong> has been confirmed. Please present your digital pass or QR ticket at the venue entrance for optical check-in.
          </p>

          <div style="background: #EEF2FF; border: 1px solid #C7D2FE; border-radius: 8px; padding: 16px; margin: 20px 0;">
            <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #4338CA; font-weight: 700;">TICKET IDENTIFIER</div>
            <div style="font-size: 24px; font-weight: 800; color: #1E1B4B; letter-spacing: 0.05em; margin: 4px 0;">{ticket_code}</div>
            <div style="font-size: 13px; color: #475569;"><strong>Date:</strong> {event_date} | <strong>Time:</strong> {event_time}</div>
            <div style="font-size: 13px; color: #475569;"><strong>Venue:</strong> {event_venue}</div>
          </div>

          {qr_img_tag}

          <p style="font-size: 12px; color: #94A3B8; text-align: center; margin-bottom: 0;">
            This pass is unique and non-transferable. Generated by Smart Campus Event Portal.
          </p>
        </div>
      </div>
    </body>
    </html>
    """
    return email_service.send_email(to_email, subject, html)


def send_broadcast_alert(recipients: List[str], title: str, message: str, priority: str = "info") -> int:
    """
    Dispatch priority alert to a list of student recipients.
    """
    prefix = "[URGENT BULLETIN]" if priority == "urgent" else "[CAMPUS NOTICE]"
    subject = f"{prefix} {title}"
    color = "#E11D48" if priority == "urgent" else "#2563EB"

    html = f"""
    <div style="font-family: sans-serif; max-width: 580px; margin: 0 auto; padding: 20px; border-left: 4px solid {color}; background: #FFF;">
      <h2 style="color: {color}; margin-top: 0;">{title}</h2>
      <p style="font-size: 14px; line-height: 1.6; color: #334155;">{message}</p>
      <hr style="border: none; border-top: 1px solid #E2E8F0; margin: 20px 0;" />
      <small style="color: #64748B;">Smart Campus Event Portal Automated Notification</small>
    </div>
    """

    count = 0
    for r in recipients:
        if email_service.send_email(r, subject, html):
            count += 1
    return count
