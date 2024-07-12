# KAUN BANEGA CROREPATI
import win32com.client
import requests
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf

def play_mp3_with_sounddevice(file_path):
    # Load the MP3 file
    data, fs = sf.read(file_path)

    # Play the audio
    sd.play(data, fs)
    sd.wait()


def speech_to_text():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use default microphone as the audio source
    with sr.Microphone() as source:
        print("Say the answer...")

        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        # Capture the audio input
        audio = recognizer.listen(source)

        print("Processing...")

        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Sorry, You have been timed out")
            return ''
        except sr.RequestError as e:
            print(f"Sorry, there was an error accessing the Google Speech Recognition service: {e}")
            return None

def fetch_questions_from_opentdb(category, difficulty, num_questions):
    api_url = "https://opentdb.com/api.php"
    params = {
        "amount": num_questions,
        "category": category,  # Specify the category ID (e.g., 9 for General Knowledge)
        "difficulty": difficulty,  # Specify the difficulty level (easy, medium, hard)
        "type": "multiple"  # Specify the question type (multiple choice)
    }

    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            return response.json()["results"]
        else:
            print(f"Failed to fetch questions. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def application():
    speaker = win32com.client.Dispatch("SAPI.SpVoice")

    print("\n\n------------------KAUN BANEGA CROREPATI-------------------------\n\n")

    file_path = "KBC_back.mp3"
    play_mp3_with_sounddevice(file_path)

    category_id = 9  # General Knowledge category ID
    difficulty = "easy"
    num_questions = 8

    questions_data = fetch_questions_from_opentdb(category_id, difficulty, num_questions)

    if questions_data:
        # Extract questions and answers from the API response
        ques = [question["question"] for question in questions_data]
        ans = [question["correct_answer"] for question in questions_data]

        # Now integrate these questions and answers into your game logic
        # ...
    else:
        print("Failed to fetch questions from OpenTDB API. Exiting.")
        return    

    # ques = [
    #     "What is the Capital of Kerala?",
    #     "Which country won 2002 FIFA World Cup ?",
    #     "Who is called the father of Indian Renaissance?",
    #     "Who is called the father of Alternating Current ?",
    #     "How many centuries did Sachin Tendulkar score in test cricket?",
    #     "In Mahabharat who killed Shakuni Mama",
    #     "What is the capital of Denmark ? ",
    #     "Who is the CEO of OpenAI ?"
    # ]

    # ans = ['Thiruvananthapuram', 'Brazil', 'Raja Ram Mohan Roy','Nikola Tesla', '51', 'Sahdev' ,'Copenhagen','Sam Altman']


    level = ["0", '5,000', 10000, 20000, 50000, 100000, 200000, 500000, 1000000]

    i=0

    while i<8:
        q = f"{i+1} . "+ques[i]
        print(q)
        speaker.Speak(q)
        print("\n")
        # x = input("Enter your Answer : ")
        print('Enter your Answer : ')
        x = speech_to_text()
        print(x)
        if(len(x)==0):
            speaker.Speak('Sorry, You have been timed out')
            print(f'Correct answer is {ans[i]}')
            speaker.Speak(f'Correct answer is {ans[i]}')
            print("\nYou Take home",level[i],"! Thanks for playing the game\n\n")
            speaker.Speak(f"You take home rupees {level[i]}")
            speaker.Speak("Thanks for playing the game")
            break
        elif x.upper() == ans[i].upper():
            print("\n\nCongratulations! You won Rs. ", level[i+1])
            speaker.Speak(f"Congratulations! You won Rs. {level[i+1]}")
        else:
            print("\n\nSorry Wrong Answer! Correct answer is ",ans[i])
            speaker.Speak(f"Sorry Wrong Answer! Correct answer is {ans[i]}")
            print("\nYou Take home",level[i],"! Thanks for playing the game\n\n")
            speaker.Speak(f"You take home rupees {level[i]}")
            speaker.Speak("Thanks for playing the game")
            break
        print("\n")
        i=i+1


    if i==8:
        print("Congratulations! You are a crorepati. You have successfully finished the game.\n\n")
        speaker.Speak("Congratulations! You are a crorepati. You have successfully finished the game")


if __name__ == '__main__':
    application()