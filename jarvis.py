import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


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


if __name__ == "__main__":
    new_chat()