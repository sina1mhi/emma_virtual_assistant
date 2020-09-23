import speech_recognition as sr  # recognise speech
import time  # get time details
import webbrowser  # open browser
import os  # to remove created audio files
import random   # Generates random number
import smtplib
import classes.login_info # Email Login Information
from playsound import playsound  # to play an audio file
from gtts import gTTS  # google text to speech
from random import randint  # Generates random number
# selenium for browsing websites - Download WebDriver and put in C: directory
from selenium import webdriver
# For hiding selenium browser window
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client  # twilio for sending SMS
from classes.person import Person   # Sets the name of user
from classes.bcolors import bcolors  # Colors Code
from email.mime.multipart import MIMEMultipart  # To send emails (supports plain text and html format)
from email.mime.text import MIMEText
from win10toast import ToastNotifier    # Creates Windows 10 notification


def there_exists(terms):    # if the items exists return True
    for term in terms:
        if term in voice_data:
            return True


def weather_info():
    # these variables are needed for options part.
    CHROME_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    CHROMEDRIVER_PATH = r'C:\Windows\chromedriver.exe'
    WINDOW_SIZE = "1920,1080"

    # These options hide the selenium window
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    browser = webdriver.Chrome(chrome_options=chrome_options)
    os.system('cls||clear')  # clears the terminal
    browser.get(f"https://google.com/search?q={voice_data}")
    os.system('cls||clear')  # clears the terminal
    time.sleep(1)

    try:
        # finds the weather description and gets its text.
        wdesc = browser.find_element_by_id("wob_dc").text
        wcity = browser.find_element_by_id("wob_loc").text
        wtemp = browser.find_element_by_id("wob_tm").text
        wprec = browser.find_element_by_id("wob_pp").text
        whumid = browser.find_element_by_id("wob_hm").text
        wwind = browser.find_element_by_id("wob_ws").text
        os.system('cls||clear')
        speak(
            f"It's {wdesc} in {wcity} with the temperature of {wtemp} Celsius.")
        print(f"      Precipitation: {wprec}")
        print(f"      Humidity: {whumid}")
        print(f"      Wind: {wwind}\n")
        time.sleep(3)

    except:
        print(f"{bcolors.RED}Emma: Something went wrong!{bcolors.END}")
        exit()


def send_email(target, message, subject="EVA"):
    email_message_obj = MIMEMultipart()
    email_message_obj["from"] = "Emma Virtual Assistant"
    email_message_obj["to"] = target
    email_message_obj["subject"] = subject
    email_message_obj.attach(MIMEText(message))

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp_obj:
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.login(classes.login_info.email_address, classes.login_info.password)
        smtp_obj.send_message(email_message_obj)
        print(
            f"{bcolors.RED}Emma:{bcolors.END} Message sent.\n")
        playsound(r"sounds\message_sent.mp3")


def show_university_result():   # Connects to edu.iaurasht.ac.ir and gets the result
    # these variables are needed for options part.
    CHROME_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    CHROMEDRIVER_PATH = r'C:\Windows\chromedriver.exe'
    WINDOW_SIZE = "1920,1080"

    # These options hide the selenium window
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    # Gets the username and password to login
    username = input(f"{bcolors.RED}Emma:{bcolors.END} Username: ")
    password = input(f"{bcolors.RED}Emma:{bcolors.END} Password: ")

    browser = webdriver.Chrome(chrome_options=chrome_options)
    os.system('cls||clear')  # clears the terminal
    browser.get("http://edu.iaurasht.ac.ir/loginb.aspx")
    os.system('cls||clear')  # clears the terminal

    # Username TextBox
    username_field = browser.find_element_by_id("txtUserName")
    # enters the username value inside the username textbox
    username_field.send_keys(username)

    # Password TextBox
    password_field = browser.find_element_by_id("txtPassword")
    # enters the password value inside the password textbox
    password_field.send_keys(password)

    # submit button
    submit_button = browser.find_element_by_id("btn_ent_stu")
    # Click the submit button to finish the login process
    submit_button.click()
    time.sleep(1)   # needs to sleep to load the whole page then continues.

    # Get the information of results
    browser.get("http://edu.iaurasht.ac.ir/karnameh_total.aspx")
    os.system('cls||clear')  # clears the terminal

    try:
        # finds the average element and gets its text.
        avg_result = browser.find_element_by_id(
            "ContentPlaceHolder1_karnameh_total_lblAverage").text

        # finds the score element and gets its text.
        score = browser.find_element_by_id(
            "ContentPlaceHolder1_karnameh_total_lblGrant").text

        # finds the passed units element and gets its text.
        passed_units = browser.find_element_by_id(
            "ContentPlaceHolder1_karnameh_total_lblAcceptCourse").text

        # finds all the selected units element and gets its text.
        selected_units = browser.find_element_by_id(
            "ContentPlaceHolder1_karnameh_total_lblSelectCourse").text
        os.system('cls||clear')

        # Says nice words if the average is higher than 15.
        if float(avg_result) > 15:
            playsound(r"sounds\you_are_clever_student.mp3")

        # prints the whole info with colors.
        print(
            f"Moadel: {bcolors.GREEN}{avg_result}{bcolors.END}, Emtiyaz: {bcolors.GREEN}{score}{bcolors.END}, Ghabuli: {bcolors.GREEN}{passed_units}{bcolors.END}, Entekhabi: {bcolors.GREEN}{selected_units}{bcolors.END}")
        playsound(r"sounds\here_is_your_result.mp3")
        browser.close()  # closes the browser
    except:
        print(
            f"{bcolors.RED}Emma:{bcolors.END}Incorrect information has entered.")
        browser.close()
        playsound(r"sounds\incorrect_information.mp3")

    email_report = ""
    playsound(r"sounds\want_receive_email.mp3")
    while email_report != "y" or email_report != "n":
        email_report = input(f"{bcolors.RED}Emma:{bcolors.END} Would you like to receive an email with this information? (Y | N) - ").lower()
        if email_report == "y":
            playsound(r"sounds\enter_email_address.mp3")
            destinaton_email_address = input(
                f"{bcolors.BLUE}Email Address:{bcolors.END} ")
            message_txt = f"Moadel: {avg_result}, Emtiyaz: {score}, Ghabuli: {passed_units}, Entekhabi: {selected_units}" + "\n" + "\nSent via - Emma Virtual Assistant"
            send_email(destinaton_email_address, message_txt, "University Report")
            break
        
        elif email_report == "n":
            playsound(r"sounds\ok.mp3")
            print(f"{bcolors.RED}Emma:{bcolors.END} OK.")
            break
        else:
            print(f"{bcolors.RED}Emma:{bcolors.END} Enter a valid answer please.")
            playsound(r"sounds\incorrect_information.mp3")



r = sr.Recognizer()  # initialise a recognizer


# listen for audio and convert it to text:
def record_audio(lang="en-US"):
    # Change the sample_rate to 16000 good quality and better recognition
    # higher sample rate means slower app.
    with sr.Microphone(sample_rate=16000) as source:  # microphone as source
        print(f"{bcolors.RED}Emma:{bcolors.END} I'm listening")
        audio = r.record(source, duration=5)  # listen for the audio via source
        print(f"{bcolors.RED}Emma:{bcolors.END} Microphone turned off, processing...\n")
        voice_data = ''
        try:
            voice_data = r.recognize_google(
                audio, language=lang)  # convert audio to text
        except sr.UnknownValueError:  # error: recognizer does not understand
            print(f"{bcolors.RED}Emma:{bcolors.END} I did'nt get that")
            playsound(r"sounds\did_not_get_that.mp3")
            exit()
        except sr.RequestError:
            # error: recognizer is not connected
            speak('Sorry, the service is down')
            exit()
        # print what user said
        print(f">> {bcolors.HEADER}{voice_data.lower()}{bcolors.END}")
        return voice_data.lower()


# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')  # text to speech(voice)
    r = randint(1, 20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file)  # save as mp3
    # print what app said
    print(f"{bcolors.RED}Emma:{bcolors.END} {audio_string}")
    playsound(audio_file)  # play the audio file
    os.remove(audio_file)  # remove audio file


# starting point
person_obj = Person()
notification_obj = ToastNotifier()
os.system('color')  # makes terminal to recognize the colors

# shows notification of program's activation
notification_obj.show_toast(title="Emma Virtual Assistant", msg="Emma has activated", icon_path="favicon.ico", duration=5)

print(f"\n{bcolors.RED}Emma:{bcolors.END} How can I help you?") # The first line
playsound(r'sounds\starting_line.mp3')  # says "How can I help you"
while(1):
    voice_data = record_audio()  # get the voice input

    # University Commands:
    # shows result
    if there_exists(['result', 'report', 'university report']):
        show_university_result()
        continue

    # About the the headmaster of the computer department
    if there_exists(['headmaster', 'who\'s in charge in computer department']):
        print(f'{bcolors.RED}Emma:{bcolors.END} Professor Andalib\n')
        playsound(r"sounds\professor_andalib.mp3")
        continue

    # Location of the headmaster of the computer department office
    if there_exists(['where can i find her', 'where is her office?']):
        print(
            f"{bcolors.RED}Emma:{bcolors.END} You can find her on the fifth floor of the Faculty of Sciences building.")
        print(
            f"{bcolors.RED}Emma:{bcolors.END} for more information please check this telegram channel:")
        playsound(r"sounds\head_of_department_details.mp3")
        print(
            f"{bcolors.RED}Emma:{bcolors.END} {bcolors.BLUE}https://t.me/drazamandalib{bcolors.END}\n")
        continue

    # General Commands:
    # 1: greeting
    if there_exists(['hey', 'hi', 'hello']):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up {person_obj.name}?", f"Hi, how can I help you? {person_obj.name}", f"hello {person_obj.name}"]
        greet = greetings[randint(0, len(greetings)-1)]
        speak(greet)
        continue

    # 2: name
    if there_exists(["what is your name", "what's your name", "tell me your name"]):
        if person_obj.name:
            speak("my name is Emma")
            continue
        else:
            speak("my name is Emma. what's your name?")
            continue

    if there_exists(["my name is"]):
        person_name = voice_data.split("is")[-1].strip()
        speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name)  # remember name in person object
        continue

    # 3: greeting
    if there_exists(["how are you", "how are you doing", "how you doing?"]):
        speak(f"I'm very well, thanks for asking {person_obj.name}")
        continue

    # 4: time
    if there_exists(["time"]):
        time_list = time.ctime().split(" ")[4].split(":")[0:2]
        if time_list[0] == "00":
            hours = '12'
        else:
            hours = time_list[0]
        minutes = time_list[1]
        current_time = f'{hours}:{minutes}'
        speak(current_time)
        continue

    # 5: search google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')
        time.sleep(5)
        continue

    # 6: search youtube
    if there_exists(["youtube"]):
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')
        time.sleep(5)
        continue

    # 7: introduction to Sina Mohammadi
    if there_exists(['programmer']) and 'search' not in voice_data:
        developer_ans = ['Sina', 'Sina Mohammadi',
                         'Sina is my lovely programmer', "Why don't you see yourself?"]
        rand_number = randint(0, len(developer_ans)-1)
        if rand_number == 3:
            webbrowser.get().open("https://linkedin.com/in/sina1mhi")
            print(f"{bcolors.RED}Emma:{bcolors.END} {developer_ans[3]}")
            playsound(r"sounds\Why don't you see yourself.mp3")
            time.sleep(5)
            continue
        else:
            print(
                f"{bcolors.RED}Emma:{bcolors.END} {developer_ans[rand_number]}")
            playsound(f"sounds\\{developer_ans[rand_number]}.mp3")
            continue

    # 8: search google in persian
    if there_exists(["search in persian", "persian", "farsi"]):
        search_term = record_audio(lang="fa-IR")
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found on Google.')
        time.sleep(5)
        continue

    # 9: Emma's opinion about herself
    if there_exists(['describe']):
        print(
            f"{bcolors.RED}Emma:{bcolors.END} I'm like a cool breeze on a snowy day; when you've got nothing to worry about.\n{bcolors.RED}Emma:{bcolors.END} Did you know I was born on a snowy day in Rasht?\n")
        playsound(r"sounds\describe1.mp3")
        playsound(r"sounds\describe2.mp3")
        continue

    # 10: Who is Emma
    if there_exists(['who are you', 'tell me about yourself']):
        print(f"{bcolors.RED}Emma:{bcolors.END} I'm Emma, developed by Mohammadi to be your virtual assistant.")
        playsound(r"sounds\developed_to_be_va.mp3")
        continue

    # 11: Weather
    if there_exists(["weather"]):
        weather_info()
        continue

    # 12: What can emma do:
    if there_exists(["what can you do", "tell me what you can do"]):
        print(
            f"{bcolors.RED}Emma:{bcolors.END} I have lots of abilities thanks to my dear developer.")
        playsound(r"sounds\wicd_1.mp3")
        print(f"{bcolors.RED}Emma:{bcolors.END} If you're a student at the IAU of Rasht branch, I can show you the result.")
        playsound(r"sounds\wicd_2.mp3")
        print(f"{bcolors.RED}Emma:{bcolors.END} I can search for anything for you in English and Persian on Google and YouTube.")
        playsound(r"sounds\wicd_3.mp3")
        print(
            f"{bcolors.RED}Emma:{bcolors.END} Why don't you see my other abilities for yourself?")
        playsound(r"sounds\wicd_4.mp3")
        print(f"{bcolors.RED}Emma:{bcolors.END} For example, try asking the weather of your favorite city.")
        playsound(r"sounds\wicd_5.mp3")
        continue

    # 13: Waiting command
    if there_exists(["wait"]):  # example command: wait 30 seconds
        if voice_data == "wait a second":
            voice_data = "wait 10 seconds"
        if voice_data == "wait a minute":
            voice_data = "wait 60 seconds"
        delay_time = int(voice_data.split(" ")[1])
        print(f"{bcolors.RED}Emma:{bcolors.END} OK.")
        playsound(r"sounds\ok.mp3")
        print(f"{bcolors.RED}Emma:{bcolors.END} Waiting... {delay_time}s")
        time.sleep(delay_time)
        continue

    if there_exists(["seconds", "second", "minute"]):  # example command: wait 30 seconds
        if voice_data == "wait a second":
            voice_data = "10 seconds"
        if voice_data == "wait a minute":
            voice_data = "60 seconds"
        delay_time = int(voice_data.split(" ")[0])
        print(f"{bcolors.RED}Emma:{bcolors.END} OK.")
        playsound(r"sounds\ok.mp3")
        print(f"{bcolors.RED}Emma:{bcolors.END} Waiting... {delay_time}s")
        time.sleep(delay_time)
        continue

    # 14: Send SMS
    # Login information for Twilio website:
    # Email: leonapeters994.9.1@gmail.com
    # Password: Ytrewq!1234567
    # Recovery Code: XDr3sZ1800bL2HkhY-JivHm3uehlMleieLrRLVuG
    # Phone Number Verified: +12534488816
    if there_exists(["sms", "message"]):
        account_sid = "ACee9d52b576450bc60d66ababa6de2785"
        auth_token = "e10d957b48b317038f4be6e60483dc78"
        playsound(r"sounds\enter_message.mp3")
        message_txt = input(
            f"{bcolors.RED}Emma:{bcolors.END} Enter your message!\n\n{bcolors.BLUE}Message:{bcolors.END} ")
        playsound(r"sounds\enter_phone.mp3")
        destinaton_phone_number = input(
            f"{bcolors.BLUE}Phone Number:{bcolors.END} ")
        message_txt = message_txt + "\n" + "\nSent via - Emma Virtual Assistant"
        try:
            client = Client(account_sid, auth_token)
            message_info = client.messages.create(
                to=f"{destinaton_phone_number}",
                from_="+12018319860",
                body=f"{message_txt}"
            )
            print(
                f"{bcolors.RED}Emma:{bcolors.END} Message sent.\n")
            playsound(r"sounds\message_sent.mp3")
            time.sleep(3)
            continue
        except:
            print(
                f"{bcolors.RED}Emma:{bcolors.END} Sorry message couldn't be sent!\n")
            playsound(r"sounds\message_couldnt_be_sent.mp3")
            exit()

    # 15: Create a random password.
    if there_exists(["secure", "secure password"]):
        characters_list = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%*&')
        password = ''

        print(f"{bcolors.RED}Emma:{bcolors.END} Which account will you use this password for?")
        playsound(r"sounds\pass_usage.mp3")
        password_title = input(f"{bcolors.BLUE}Password Title:{bcolors.END} ").capitalize()

        print(f"{bcolors.RED}Emma:{bcolors.END} How many characters should your password include?")
        playsound(r"sounds\pass_length.mp3")
        try:
            password_length = int(input(f"{bcolors.BLUE}Password Length:{bcolors.END} "))
        except ValueError:
            print(f"{bcolors.RED}Emma:{bcolors.END} Please enter a number!")
            continue

        for char in range(password_length):
            password += random.choice(characters_list)
        print(f"{bcolors.RED}Password:{bcolors.END} {password} \n")
        playsound(r"sounds\pass_has_created.mp3")
        with open('userpass.txt', 'a') as file:
            file.writelines(f"\n{password_title}: {password}")
            file.writelines(f"\n{'-' * 30}")
        time.sleep(5)
        continue

    if there_exists(["fast", "password", "fast password"]):
        characters_list = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%*&')
        password = ''
        password_length = randint(8, 16)

        for char in range(password_length):
            password += random.choice(characters_list)
        print(f"{bcolors.RED}Password:{bcolors.END} {password} \n")
        playsound(r"sounds\pass_has_created.mp3")
        time.sleep(5)
        continue

    # 16: Send email messages
    if there_exists(["email"]):
        playsound(r"sounds\enter_subject.mp3")
        message_subject = input(
            f"{bcolors.BLUE}Message Subject:{bcolors.END} ")
        playsound(r"sounds\enter_message.mp3")
        message_txt = input(
            f"{bcolors.BLUE}Message:{bcolors.END} ")
        message_txt = message_txt + "\n" + "\nSent via - Emma Virtual Assistant"
        playsound(r"sounds\enter_email_address.mp3")
        destinaton_email_address = input(
            f"{bcolors.BLUE}Email Address:{bcolors.END} ")

        send_email(destinaton_email_address, message_txt, message_subject)
        time.sleep(3)
        continue

        

    # Terminates the app
    if there_exists(["exit", "quit", "goodbye", "stop"]):
        print(f"{bcolors.RED}Emma:{bcolors.END} Going offline")
        playsound(r"sounds\going_offline.mp3")
        exit()

    # Terminates the app - 2
    if there_exists(['thanks', 'thank you']):
        print(f"{bcolors.RED}Emma:{bcolors.END} You're welcome, see you later.")
        playsound(r"sounds\you_welcome_see_you.mp3")
        exit()
