import smtplib

sender = "Private Person <from@example.com>"
receiver = "andrszollai@gmail.com"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

This is a test e-mail message."""

with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
    server.login("a8dab34e0f140d", "e24f82680e0e23")
    server.sendmail(sender, receiver, message)