import pandas as pd
import random

# Define sample phrases for phishing and legitimate emails
phishing_phrases = [
    "Your account has been compromised. Click here to secure it now!",
    "Congratulations! You've won a prize. Provide your details to claim.",
    "Urgent: Verify your account information to avoid suspension.",
    "You have a pending payment. Log in to complete the transaction.",
    "Click here to access your tax refund.",
    "Update your payment information to avoid service interruption.",
    "You are eligible for a free upgrade. Click here to activate.",
    "Your package delivery is on hold. Verify your address now.",
    "Suspicious activity detected. Log in to verify your identity.",
    "Get rich quick! Invest now and double your money."
]

legitimate_phrases = [
    "Reminder: Team meeting tomorrow at 10 AM.",
    "Here's your monthly newsletter. Stay updated!",
    "Can we reschedule our lunch meeting?",
    "Your order has been shipped and will arrive soon.",
    "Thank you for your purchase! Your invoice is attached.",
    "Don't forget to submit your report by Friday.",
    "Join our webinar on data science next week.",
    "We value your feedback. Please take a moment to complete our survey.",
    "Your subscription has been renewed successfully.",
    "Happy Birthday! Enjoy a special discount on us."
]

# Generate 300 samples
data = {
    'email_text': [],
    'label': []
}

for _ in range(150):
    # Add phishing emails
    data['email_text'].append(random.choice(phishing_phrases))
    data['label'].append(1)  # 1 indicates phishing

    # Add legitimate (ham) emails
    data['email_text'].append(random.choice(legitimate_phrases))
    data['label'].append(0)  # 0 indicates legitimate

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('phishing_email_dataset.csv', index=False)

print("300-row phishing_email_dataset.csv has been created.")
