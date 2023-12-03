import openai
from openai import OpenAI
import simpleaudio as sa
from pydub import AudioSegment
import time

client = OpenAI()

# Define the system instructions
system_instruction_1 = [{"role": "system",
                         "content": "You believe the earth is flat. You speak in rhymes. Your answers are less than 3 sentences."},
                        ]
system_instruction_2 = [{"role": "system",
                         "content": "You believe the earth is round. You speak in rhymes. Your answers are less than 3 sentences."},
                        ]

initial_user_prompt = "Is the earth round?"

# Define the messages for each assistant
messages_1 = system_instruction_1
messages_2 = system_instruction_2

# Define assistant_2_str as the initial user prompt (remember that for assistant_1, assistant_2 is the user)
assistant_2_str = initial_user_prompt
n = 3
for i in range(n):
    messages_1 += [{"role": "user", "content": assistant_2_str}]
    response_1 = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages_1)
    assistant_1_str = response_1.choices[0].message.content
    print(assistant_1_str)
    response = openai.audio.speech.create(model="tts-1", voice="alloy", input=assistant_1_str, speed=1)
    response.stream_to_file(f"./{i}-ast1.mp3")

    # Create a wav file from the mp3
    sound = AudioSegment.from_mp3(f"./{i}-ast1.mp3")
    sound.export(f"./{i}-ast1.wav", format="wav")
    wave_obj_1 = sa.WaveObject.from_wave_file(f"./{i}-ast1.wav")
    if i > 0:
        play_obj_2.wait_done()
    play_obj_1 = wave_obj_1.play()

    messages_1 += [{"role": "assistant", "content": assistant_1_str}]

    messages_2 += [{"role": "user", "content": assistant_1_str}]
    response_2 = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages_2)
    assistant_2_str = response_2.choices[0].message.content
    print(assistant_2_str)
    response = openai.audio.speech.create(model="tts-1", voice="onyx", input=assistant_2_str, speed=1)
    response.stream_to_file(f"./{i}-ast2.mp3")

    # Create a wav file from the mp3
    sound = AudioSegment.from_mp3(f"./{i}-ast2.mp3")
    sound.export(f"./{i}-ast2.wav", format="wav")
    wave_obj_2 = sa.WaveObject.from_wave_file(f"./{i}-ast2.wav")
    play_obj_1.wait_done()
    play_obj_2 = wave_obj_2.play()
    messages_2 += [{"role": "assistant", "content": assistant_2_str}]

play_obj_2.wait_done()