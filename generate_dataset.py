import pandas as pd
import random

scam_templates = [
    "URGENT! Your KYC is expired. Call {phone} now or account BLOCKED!!! Claim reward at bit.ly/scam{rand}",
    "Congratulations! You have won Rs {amount} lottery reward from KBC. Click bit.ly/claim{rand} to receive money.",
    "Dear customer, your SBI account is suspended due to missing PAN. Verify immediately at http://sbi-pan{rand}.click",
    "Khata band hone wala hai! Abhi turant {phone} pe call karein aur inam claim karein.",
    "Electricity bill unpaid! Your power connection will be disconnected tonight at 9:30 PM. Call official {phone}",
    "Y0U w0n p.r.i.z.e. cl1ck h3re http://reward-{rand}.xyz",
    "Dear Sir, ur HDFC credit card limit is approved for Rs {amount}. Click here to activate: bit.ly/hdfc{rand}",
    "Aapka loan pass ho gaya hai. Abhi {phone} par call karein. File charge 500rs. No hidden charges.",
    "Jio Free Recharge offer! Click this link to get 3 months free data: jio-offer-{rand}.top",
    "Your package from Amazon is pending delivery. Pay customs fee Rs {small_amount} here: amazon-track-{rand}.click",
    "RBI alert: Your bank account will freeze in 24 hours. Submit documents at rbi-verify-{rand}.online",
    "Congratulations! U have been selected for work from home job. Salary Rs {amount}/day. Message {phone} on WhatsApp",
    "Action required: Update your Apple ID payment method to avoid suspension. Apple-support-{rand}.com",
    "Netflix account hold! Payment failed. Update details immediately: netflix-billing-{rand}.site",
    "You won an iPhone 14 Pro Max! Provide shipping address and pay Rs {small_amount} delivery fee: claim-iphone-{rand}.top",
    "Income Tax refund of Rs {amount} is approved. Verify your bank details to claim: incometax-refund-{rand}.online",
]

legit_templates = [
    "Hey, let's catch up tomorrow at 5 PM for coffee near the campus library!",
    "Your Amazon order #408-1234567-8901234 has been dispatched and will arrive tomorrow.",
    "Please review the attached project proposal draft and let me know your thoughts.",
    "Good morning! Don't forget to submit the assignment before midnight today.",
    "Happy Birthday! Wishing you a fantastic year filled with health, happiness and success!",
    "Hi, I will be late by 15 mins for the meeting. Please start without me.",
    "OTP for login to your account is {rand}. Do not share this with anyone.",
    "Your payment of Rs {small_amount} to Swiggy was successful. Reference: {rand}",
    "Dear Customer, your account balance is Rs {amount}. Thanks for banking with us.",
    "Reminder: Dentist appointment tomorrow at 10 AM. Reply YES to confirm.",
    "Flight 6E-{rand} is on time. Boarding starts at 17:30. Have a safe journey!",
    "Can you please send me the report from last week? Thanks.",
    "Your mobile bill of Rs {small_amount} is generated and due by 5th. Pay via app.",
    "Netflix: We just added new seasons of your favorite shows. Watch now!",
    "Hello, are we still on for lunch today?",
    "Your Uber driver is arriving in 5 minutes. Vehicle: KA-01-AB-{rand}",
]

data = []
for _ in range(500):
    for label, templates in [(1, scam_templates), (0, legit_templates)]:
        t = random.choice(templates)
        t = t.replace("{phone}", f"{random.randint(7000000000, 9999999999)}")
        t = t.replace("{amount}", f"{random.randint(10000, 500000)}")
        t = t.replace("{small_amount}", f"{random.randint(50, 2000)}")
        t = t.replace("{rand}", f"{random.randint(100, 999)}")
        # Introduce some random typos or noise in 20% of cases
        if random.random() < 0.2:
            t = t.replace("a", "@").replace("o", "0").replace("e", "3")
        data.append({"message": t, "label": label})

df = pd.DataFrame(data)
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("data/messages.csv", index=False)
print(f"Generated {len(df)} samples in data/messages.csv")
