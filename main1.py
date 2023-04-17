import speech_recognition as sr
import pyttsx3
import requests
import datetime
# import openai
import os
import random
import smtplib
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# openai.api_key = "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"
NEWS_API_KEY = "89451bd793f245b187e5b542ec3ee299"


# Initialize the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Define a function to speak the response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define a function to listen for voice commands
def listen():
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    try:
        # Use the Google Speech Recognition API to convert audio to text
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError:
        print("Sorry, I could not process your request.")



def get_city():
    # Get the city name from the user via speech recognition
    speak("What city would you like the weather for?")
    city = listen()

    # If speech recognition failed, ask the user to enter the city name via keyboard input
    if not city:
        city = input("Enter city name: ")

    return city

def play_music(song_name):
    speak("What song do you want to hear?")
    city = listen()
    query = '+'.join(song_name.split())
    url = "https://music.youtube.com/search?q=" + query
    webbrowser.open(url)

def search_music():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("What song do you want to hear?")
        audio = r.listen(source)

    try:
        song_name = r.recognize_google(audio)
        print("You said:", song_name)
        play_music(song_name)  # pass song_name to play_music()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Can you please try again?")
    except sr.RequestError:
        print("Sorry, my speech service is down. Please try again later.")



def send_email(to, subject, body):
    # Enter your email credentials here
    email = "your_email@gmail.com"
    password = "your_password"

    # Connect to the email server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)

    # Create the email message
    message = f"Subject: {subject}\n\n{body}"

    # Send the email
    server.sendmail(email, to, message)
    server.quit()

def process_email_command(command):
    if "send email" in command:
        speak("To whom should I send the email?")
        to = listen()
        speak("What should the subject be?")
        subject = listen()
        speak("What should the body of the email say?")
        body = listen()
        send_email(to, subject, body)
        speak("Email sent successfully!")

def search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def process_search_command(command):
    if "search" in command:
        speak("What would you like me to search for?")
        query = listen()
        search(query)

def get_news(topic):
    url = f"https://newsapi.org/v2/top-headlines?q={topic}&apiKey=89451bd793f245b187e5b542ec3ee299"
    response = requests.get(url)
    data = response.json()
    articles = data["articles"]
    for article in articles:
        speak(article["title"])

def process_news_command(command):
    if "news" in command:
        speak("What topic would you like the news for?")
        topic = listen()
        get_news(topic)

# Run the voice assistant
while True:
    command = listen()

    if "hello" in command:
        speak("Hello there! How can I help you?")
        continue
    elif "what is your name" in command:
        speak("My name is none of your business. now what can I help you with?")
    elif "that was rude" in command:
        speak("You would think you were paying me to sit here and be polite. Now how can I help you? My commands are news, weather, what is the time, music, email, and search.  Which can I help you with?")
        
    elif "weather" in command:
        # Get the city name from the user
        city = get_city()

        # Make an HTTP request to the OpenWeatherMap API
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=37eb18ecfb049bd0b03c88083f876596&units=imperial"
        response = requests.get(url)

        # Check for errors in the API response
        if response.status_code == 404:
            speak(f"Sorry, I could not find the weather for {city}. Please pick one that exist or pronounce it correctly")
            continue
        elif response.status_code != 200:
            speak("Sorry, there was an error processing your request.")
            continue

        # Parse the JSON response from the API
        data = response.json()

        # Check for errors in the API response
        if "main" not in data:
            speak(f"Sorry, there was an error processing the weather information for {city}.")
            continue

        # Extract the weather information from the API response
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]

        # Speak the weather information
        response_text = f"The temperature in {city} is {temperature} , and the weather is {description}. You are welcome"
        speak(response_text)

    elif "what is the time" in command:
        now = datetime.datetime.now()
        response_text = (f"The time is currently {now.strftime('%I:%M %p')}.")

    elif "music" in command:
        play_music()
        

    elif "email" in command:
        process_email_command(command)

    elif "search" in command:
        process_search_command(command)

    elif "news" in command:
        process_news_command(command)

    elif " " in command:
         speak("Sorry, please speak up.")
         continue
    
    elif "stop" in command or "bye" in command:
        speak("Goodbye!")
        break

    else:
        speak("I'm sorry, I don't understand. Can you please repeat? With confidence this time")
            
