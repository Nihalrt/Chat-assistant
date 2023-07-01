import speech_recognition as sr
import pyttsx3
import openai

openai.api_key = "Your API Key"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

conversation = []
user_name = "Sam"
bot_name = "Siri"

def listen_for_audio():
    with mic as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("No longer listening")

    try:
        user_input = r.recognize_google(audio)
        return user_input
    except sr.UnknownValueError:
        return ""

def generate_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_str = response.choices[0].text.strip().replace("\n", "")
    return response_str

while True:
    user_input = listen_for_audio()
    if user_input:
        prompt = user_name + ": " + user_input + "\n" + bot_name + ":"
        conversation.append(prompt)

        response_str = generate_response("\n".join(conversation))
        conversation.append(response_str + "\n")
        print(response_str)

        engine.say(response_str)
        engine.runAndWait()
