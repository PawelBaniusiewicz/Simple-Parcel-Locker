from flask import Flask
from flask_mail import Mail, Message

class MailSender:
    _mail = None
    _sender = None

    def __init__(self, app: Flask, sender: str | None) -> None:
        MailSender._mail = Mail(app)
        MailSender._sender = sender

    @classmethod
    def send(cls, email: str, username: str , subject: str, activation_link: str) -> None:
        mail_content = f'''
                <html>
                    <head>
                        <meta charset="UTF-8">
                    </head>
                    <body style="margin: 0; padding: 0; background-color: #09090b; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #e5e5e5;">
                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #09090b; padding: 40px 20px;">
                            <tr>
                                <td align="center">
                                    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; background-color: #141417; border-radius: 16px; border: 1px solid #27272a; overflow: hidden;">
                                        <tr>
                                            <td align="center" style="padding: 40px 40px 20px 40px;">
                                                <h1 style="color: #ffffff; margin: 0; font-size: 28px; letter-spacing: -0.5px;">ParcelLocker</h1>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center" style="padding: 0 40px 30px 40px;">
                                                <h2 style="color: #ffffff; margin-top: 0; font-size: 20px; font-weight: normal;">HI, {username}! 👋</h2>
                                                <p style="font-size: 16px; line-height: 1.6; color: #a3a3a3; margin-bottom: 30px;">
                                                    Thank you for registering with ParcelLocker. To take full advantage of the system and receive your packages, please confirm your email address by clicking the button below.
                                                </p>  
                                                <a href="{activation_link}" style="display: inline-block; padding: 14px 32px; background-color: #4f46e5; color: #ffffff; text-decoration: none; border-radius: 50px; font-weight: 600; font-size: 16px;">
                                                    Active account
                                                </a>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center" style="background-color: #0d0d10; padding: 20px; border-top: 1px solid #27272a;">
                                                <p style="margin: 0; font-size: 12px; color: #737373;">
                                                    If you haven't created an account with ParcelLocker, please ignore this message.
                                                    The link is valid for 5 minutes.
                                                </p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </body>
                </html>
            '''
        message = Message(
            subject=subject,
            sender=cls._sender,
            recipients=[email],
            html=mail_content
        )

        cls._mail.send(message)