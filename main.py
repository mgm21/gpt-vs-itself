import openai
from openai import OpenAI

client = OpenAI()

# TODO: coded a quick version of the flow. Must make functions and/or classes to avoid code repetition.

# Define the system instructions
system_instruction_1 = [{"role": "system",
                         "content": "You are a crazy assistant who believes Star Wars is better than Star Trek. Your answers are under 3 sentences."},
                        ]
system_instruction_2 = [{"role": "system",
                         "content": "You are an extremely rude assistant who believes Star Trek is better than Star Wars. Your answers are under 3 sentences."},
                        ]

initial_user_prompt = "Which is better Star Wars or Star Trek?"

# Define the messages for each assistant
messages_1 = system_instruction_1
messages_2 = system_instruction_2

# Define assistant_2_str as the initial user prompt (remember that for assistant_1, assistant_2 is the user)
assistant_2_str = initial_user_prompt

for i in range(3):
    messages_1 += [{"role": "user", "content": assistant_2_str}]
    response_1 = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages_1,)
    assistant_1_str = response_1.choices[0].message.content
    print(assistant_1_str)
    response = openai.audio.speech.create(model="tts-1", voice="alloy", input=assistant_1_str)
    response.stream_to_file(f"./{i}-ast1.mp3")
    messages_1 += [{"role": "assistant", "content": assistant_1_str}]

    messages_2 += [{"role": "user", "content": assistant_1_str}]
    response_2 = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages_2,)
    assistant_2_str = response_2.choices[0].message.content
    print(assistant_2_str)
    response = openai.audio.speech.create(model="tts-1", voice="onyx", input=assistant_2_str)
    response.stream_to_file(f"./{i}-ast2.mp3")
    messages_2 += [{"role": "assistant", "content": assistant_2_str}]

