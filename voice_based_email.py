from email.message import EmailMessage
import ssl
import smtplib
import speech_recognition as sr
import pyttsx3
from imapclient import IMAPClient
import re
import time
import email

email_sender = 'demomail686@gmail.com'
email_password = 'qjlikcpoaymvbreu'

def menu():
    while True:
        show_menu()
        option = get_speech_input("Please choose an option from the menu:")
        process_menu_option(option)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def read_emails(email, password, num_emails=5):
    # Connect to the IMAP server
    server = IMAPClient("imap.gmail.com", ssl=True)

    # Login to the email account
    server.login(email, password)

    # Select the mailbox (e.g., 'INBOX')
    server.select_folder("INBOX")

    uids = server.search("ALL")
    total_emails = len(uids)
    start_index = max(total_emails - num_emails, 0)
    end_index = total_emails

    index_mapping = {}  # Mapping of index to email UID

    while start_index >= 0:
        # Fetch and print the subjects and sender email addresses of the selected emails
        messages = server.fetch(uids[start_index:end_index], ["ENVELOPE", "BODY[HEADER.FIELDS (FROM)]"])

        for idx, uid in enumerate(reversed(messages), start=1):
            data = messages[uid]
            envelope = data[b"ENVELOPE"]
            subject = envelope.subject.decode()
            sender = re.findall(r'<(.*?)>', data[b"BODY[HEADER.FIELDS (FROM)]"].decode())[0]
            
            # Store the index mapping
            index_mapping[idx] = uid
            
            print(f"Index: {idx}")
            print("Sender email:", sender)
            speak(f"Index {idx} :")
            speak(f"Sender email: {sender}")
            print("Subject:", subject)
            speak("Subject: " + subject)
            print("-" * 50)

        end_index = start_index
        start_index = max(start_index - num_emails, 0)

        # Ask the user if they want to read more emails or expand a specific email
        while True:
            user_choice = get_speech_input("Do you want to read more emails or expand a specific email? (more/expand/no)")

            if user_choice == "no":
                break
            elif user_choice == "more":
                break
            elif user_choice == "expand":
                while True:
                    expand_choice = get_number_input("Please speak the number of the email you want to expand:")
                    if expand_choice.isdigit() and int(expand_choice) in index_mapping:
                        selected_uid = index_mapping[int(expand_choice)]
                        expand_email(selected_uid, server)
                        break
                    else:
                        print("Invalid email number. Please try again.")
                        speak("Invalid email number. Please try again.")
            else:
                print("Invalid choice. Please enter 'more', 'expand', or 'no'.")
                speak("Invalid choice. Please enter 'more', 'expand', or 'no'.")

        if user_choice == "no":
            break

    server.logout()

def expand_email(uid, server):
    # Fetch the email content
    email_data = server.fetch([uid], ["RFC822"])

    # Get the sender email, subject, and body
    email_message = email.message_from_bytes(email_data[uid][b"RFC822"])
    sender = email.utils.parseaddr(email_message["From"])[1]
    subject = email_message["Subject"]
    body = ""

    # Extract the email body
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = email_message.get_payload(decode=True).decode()

    # Display the sender email, subject, and body
    print("Sender email:", sender)
    speak("Sender email: " + sender)
    print("Subject:", subject)
    speak("Subject: " + subject)
    print("Body:", body)
    speak("Body: " + body)

    # Additional actions or processing for the expanded email
    # ...

    print("-" * 50)

def get_number_input(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        speak(prompt)
        recognizer.dynamic_energy_adjustment_ratio = 1.5  # Adjust the ratio as per your needs
        recognizer.dynamic_energy_threshold = True
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

    try:
        input_text = recognizer.recognize_google(audio)
        # Convert spoken numbers to numerical representation
        input_text = input_text.lower().replace(" ", "")
        input_text = convert_spoken_numbers(input_text)
        print("User input:", input_text)
        speak("User input: " + input_text)

        return input_text
    except sr.UnknownValueError:
        print("Invalid audio or no speech detected. Please try again.")
        speak("Invalid audio or no speech detected. Please try again.")
        return get_speech_input(prompt)


def convert_spoken_numbers(text):
    """
    Converts spoken numbers to numerical representation.
    Example: "one" -> "1", "two" -> "2", etc.
    Add more conversions as per your needs.
    """
    conversions = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "tree": "3",
        "sri": "3",
        "shri": "3",
        "for" : "4",
        "free" : "3",
        "firstemail" : "1",
        "secondemail" : "2",
        "thirdemail" : "3",
        "fourthemail" : "4",
        "fifthemail" : "5",
        
        # Add more conversions here
    }

    for word, number in conversions.items():
        text = text.replace(word, number)

    return text


def get_speech_input(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        speak(prompt)
        recognizer.dynamic_energy_adjustment_ratio = 1.5  # Adjust the ratio as per your needs
        recognizer.dynamic_energy_threshold = True
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

    try:
        input_text = recognizer.recognize_google(audio)
        print("User input:", input_text)
        speak("User input: " + input_text)
        return input_text
    except sr.UnknownValueError:
        print("Invalid audio or no speech detected. Please try again.")
        speak("Invalid audio or no speech detected. Please try again.")
        return get_speech_input(prompt)


def get_login_input(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        speak(prompt)
        recognizer.dynamic_energy_adjustment_ratio = 2  # Adjust the ratio as per your needs
        recognizer.dynamic_energy_threshold = True
        audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)

    try:
        input_text = recognizer.recognize_google(audio)
        input_text = input_text.lower().replace(" ", "")
        if "atgmail.com" in input_text:
            input_text = input_text.replace("atgmail.com", "@gmail.com")
        print("User input:", input_text)
        speak("User input: " + input_text)
        return input_text
    except sr.UnknownValueError:
        print("Invalid audio or no speech detected. Please try again.")
        speak("Invalid audio or no speech detected. Please try again.")
        return get_login_input(prompt)



def show_menu():
    menu = ["Send Mail", "Read Mail", "Logout"]
    menu_text = "\n".join(menu)
    print("Menu:\n" + menu_text)
    speak("Menu:\n" + menu_text)

def process_menu_option(option):
    if option == "send mail":
        speak("Directing you to the send mail page.")
        while True:
            while True:
                email_recipient = get_login_input("Please speak the recipient's email address:")
                confirm_message = "You said " + email_recipient + ". Is that correct? (yes/no)"
                user_choice = get_speech_input(confirm_message)
                if user_choice == "yes":
                    break
                elif user_choice != "no":
                    print("Invalid option. Please choose 'yes' or 'no'.")
                    speak("Invalid option. Please choose 'yes' or 'no'.")
            break

        subject = get_speech_input("Please speak the email subject:")
        body = get_speech_input("Please speak the email message:")

        attachment = None
        while True:
            attachment_choice = get_speech_input("Do you want to add an attachment? (yes/no)")
            if attachment_choice == "yes":
                attachment = record_audio()
                break
            elif attachment_choice == "no":
                break
            else:
                print("Invalid option. Please choose 'yes' or 'no'.")
                speak("Invalid option. Please choose 'yes' or 'no'.")

        send_email(email_recipient, subject, body, attachment)
    elif option == "read mail":
        print("Showing you the last 5 emails...")
        speak("Showing you the last 5 emails")
        read_emails(email_sender, email_password, num_emails=5)
    elif option == "logout" or option == "log out":
        exit()
    else:
        print("Invalid option. Please try again.")
        speak("Invalid option. Please try again.")
        option = get_speech_input("Please choose an option from the menu:")
        process_menu_option(option)

def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Start speaking now.")
        speak("Start speaking now.")
        recognizer.dynamic_energy_adjustment_ratio = 2  # Adjust the ratio as per your needs
        recognizer.dynamic_energy_threshold = True
        audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)

    # Wait for 3 seconds after the user stops speaking
    time.sleep(3)
    try:
        print("Recording successful!")
        speak("Recording successful!")
        return audio
    except sr.UnknownValueError:
        print("Recording failed. Please try again.")
        speak("Recording failed. Please try again.")
        return record_audio()

def send_email(recipient, subject, body, attachment=None):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = recipient
    em['Subject'] = subject
    em.set_content(body)

    if attachment is not None:
        em.add_attachment(attachment.get_wav_data(), maintype='audio', subtype='wav', filename='attachment.wav')

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, recipient, em.as_string())
        print("Email sent successfully!")
        speak("Email sent successfully!")
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPException):
        print("Email not sent. Invalid email or an error occurred.")
        speak("Email not sent. Invalid email or an error occurred.")


def main():
    print("Welcome to the EchoMail")
    speak("Welcome to the Echo Mail")
    
    menu()

if __name__ == "__main__":
    main()
