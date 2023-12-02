from openai import OpenAI

client = OpenAI()

initial_messages = [
    {"role": "system", "content": "You are a funny assistant."},
]

messages = initial_messages

for _ in range(5):
    user_str = input("Your response: ")
    messages += [{"role": "user", "content": user_str}]
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    assistant_str = response.choices[0].message.content
    print(assistant_str)
    messages += [{"role": "assistant", "content": assistant_str}]
