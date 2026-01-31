import os
import resend

# resend.api_key = os.getenv("RESEND_API_KEY")
resend.api_key="rre_j2EsWs3X_5inMqvEBv5fR9cCg5pgZBrLu"

# FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_EMAIL="rehaan@resend.dev"

def send_email_otp(email: str, otp: str):
    response = resend.Emails.send({
        "from": FROM_EMAIL,
        "to": email,
        "subject": "Your OTP Verification Code",
        "html": f"""
        <h3>Email Verification</h3>
        <p>Your OTP is:</p>
        <h2>{otp}</h2>
        <p>This OTP is valid for 5 minutes.</p>
        """
    })

    return response
