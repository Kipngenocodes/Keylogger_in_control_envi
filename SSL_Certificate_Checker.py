import ssl
import socket
from datetime import datetime, timezone
from OpenSSL import crypto
import smtplib
from email.mime.text import MIMEText

def get_certificate(hostname, port=443):
    """
    Retrieves the SSL certificate from the specified hostname and port.

    :param hostname: The domain name of the server to check.
    :param port: The port to connect to (default is 443 for HTTPS).
    :return: The SSL certificate in PEM format.
    """
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                der_cert = ssock.getpeercert(binary_form=True)
                pem_cert = ssl.DER_cert_to_PEM_cert(der_cert)
                return pem_cert
    except Exception as e:
        print(f"Error retrieving certificate for {hostname}: {e}")
        return None

def parse_certificate(pem_cert):
    """
    Parses the SSL certificate details from its PEM format.

    :param pem_cert: The SSL certificate in PEM format.
    :return: A dictionary containing certificate details.
    """
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, pem_cert)
    cert_details = {
        'issuer': dict(cert.get_issuer().get_components()),
        'subject': dict(cert.get_subject().get_components()),
        'serial_number': cert.get_serial_number(),
        'version': cert.get_version(),
        'not_before': datetime.strptime(cert.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ'),
        'not_after': datetime.strptime(cert.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ'),
        'fingerprint': cert.digest("sha256").decode('utf-8'),
    }
    return cert_details

from datetime import datetime, timezone

def check_ssl_certificate(hostname):
    """
    Checks the SSL certificate for the given hostname and logs its status.

    :param hostname: The domain name of the server to check.
    """
    pem_cert = get_certificate(hostname)
    if not pem_cert:
        return
    cert_details = parse_certificate(pem_cert)

    # Ensure 'not_after' is offset-aware
    not_after_aware = cert_details['not_after'].replace(tzinfo=timezone.utc)

    # Get the current date as offset-aware
    current_date = datetime.now(timezone.utc)

    # Calculate days remaining until expiration
    days_remaining = (not_after_aware - current_date).days

    # Display and log certificate details
    log_results = (
        f"SSL Certificate for {hostname}:\n"
        f"  Issuer: {cert_details['issuer']}\n"
        f"  Subject: {cert_details['subject']}\n"
        f"  Serial Number: {cert_details['serial_number']}\n"
        f"  Version: {cert_details['version']}\n"
        f"  Expiry Date: {cert_details['not_after']}\n"
        f"  Fingerprint (SHA256): {cert_details['fingerprint']}\n"
        f"  Days Until Expiration: {days_remaining} days\n"
    )

    print(log_results)
    log_to_file('ssl_certificate_log.txt', log_results)

    # Send an email if the certificate is about to expire
    if days_remaining <= 30:
        send_email_notification(hostname, cert_details, days_remaining)


def log_to_file(filename, message):
    """
    Logs the message to the specified file.

    :param filename: The file name to log to.
    :param message: The message to log.
    """
    with open(filename, 'a') as f:
        f.write(message + '\n')

def send_email_notification(hostname, cert_details, days_remaining):
    """
    Sends an email notification if the SSL certificate is about to expire.

    :param hostname: The domain name of the server to check.
    :param cert_details: The dictionary containing certificate details.
    :param days_remaining: Days remaining until the certificate expires.
    """
    smtp_server = "akcinfo.com"
    smtp_port = 587
    sender_email = "your_email@example.com"
    receiver_email = "admin@example.com"
    password = "your_email_password"

    subject = f"SSL Certificate Expiration Warning for {hostname}"
    body = (
        f"The SSL certificate for {hostname} is expiring soon!\n"
        f"Expiry Date: {cert_details['not_after']}\n"
        f"Days Until Expiration: {days_remaining} days\n"
        f"Please renew the certificate as soon as possible."
    )
    message = MIMEText(body)
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)
            print(f"Email notification sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email notification: {e}")

if __name__ == "__main__":
    domains = ["www.amazon.com", "www.facebook.com"]
    for domain in domains:
        check_ssl_certificate(domain)
