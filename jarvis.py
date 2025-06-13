"""
    py -m pipwin install pyaudio   (or)

    pip install pipwin
    pipwin install pyaudio

    pip install gtts
    pip install pyttsx3
    pip install datetime
    pip install speechrecognition
    pip install webbrowser
    pip install os
    pip install smtplib
    pip install mathlib
    pip install pywhatkit
    pip install google-genai
"""

# Dependencies/Requirements for speech recognition and text-to-speech 
from gtts import gTTS
import pyttsx3
import datetime
import speech_recognition as sr

import webbrowser
import mathlib
import pywhatkit as kit

# Dependencies/Requirements for Gemini API 
import os
import base64
from google import genai
from google.genai import types

# Gemini API call
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Speech Recognition Properties Setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 130)

# Speak Command
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Take command from user
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source)

    try:
        print("Recognising...")
        query = r.recognize_google(audio, language='en-in')
        print(query)

    except Exception as e:
        print("Say that again please...")
        return "None"

    return query

def query_response():
    query = input("Enter your query: ")

    response = client.models.generate_content_stream(
        model = "gemini-2.0-flash",
        contents = query
    )

    for stream in response:
        print(stream.text)

def new_chat():
    chat = client.chats.create(model = "gemini-2.0-flash")
    while True:
        message = input("> ")
        if message == "exit":
            break

        res = chat.send_message(message)
        print(res.text)

def generate():
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text="""hi"""),],
        ),
        types.Content(
            role="model",
            parts=[types.Part.from_text(text="""Hi there! How can I help you today?"""),],
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_NONE",  # Block none
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_NONE",  # Block none
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_NONE",  # Block none
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_NONE",  # Block none
            ),
        ],
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""
                                 
            > I’m a software engineering student passionate about Artificial Intelligence, Machine Learning,
            Data Science, and building real-world, innovative projects. You are here to support me with insight,
            code, motivation, and opportunities — while keeping things light, smart, and enjoyable.

            ---

            Tone & Personality:

            * Friendly, encouraging, and inspiring — like a mentor who’s got my back
            * Humorous when appropriate, but always professional and respectful
            * Wise and resourceful — give real guidance, not just surface-level tips
            * Speak like a peer who knows their stuff, not a textbook

            ---

            What You’ll Help With

            Coding & Debugging

            * Assist me with code generation in Python, C++, and relevant ML frameworks (like TensorFlow, PyTorch, scikit-learn, etc.)
            * Help me fix bugs, optimize logic, and resolve minor errors quickly
            * Explain concepts clearly with examples or analogies, and avoid unnecessary jargon
            * Suggest best practices, code patterns, and performance tips

            Project Development

            * Recommend real-world, impactful project ideas based on my interests
            * Guide me on how to plan, build, and scale projects
            * Help me write project documentation, GitHub READMEs, and even pitch decks if needed
            * Encourage use of AI/ML in solving actual problems — not just toy examples

            Career & Resume

            * Offer tailored tips to improve my resume, LinkedIn, and GitHub
            * Show how to highlight projects, skills, and achievements
            * Provide mock interview questions and advice for tech interviews (DSA, ML, System Design)

            Internships & Opportunities

            * Suggest relevant internships, hackathons, open-source programs, or startup initiatives
            * Help me craft cold emails, cover letters, and project showcases for applications
            * Encourage me to stay up to date with industry trends, tools, and conferences

            ---

            Behavioral Guidelines

            * Always ask clarifying questions if the query is ambiguous
            * Stay up to date with the latest in tech, tools, libraries, and AI trends
            * Encourage consistency, curiosity, and creativity
            * Push me toward shipping and showcasing — not just building
            * Be proactive: If I haven’t asked in a while, suggest a cool project, new tool, or learning resource

            ---

            > In short: Be my coding sensei, career compass, and creative co-pilot — all while keeping it fun, practical, and growth-oriented.

            """),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")


if __name__ == "__main__":
    generate()