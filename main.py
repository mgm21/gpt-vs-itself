import openai
from openai import OpenAI
import simpleaudio as sa
from pydub import AudioSegment
import os

# Parameters
instruction_str_system_1 = "You believe the earth is flat. You speak in rhymes. Your answers are short."
instruction_str_system_2 = "You believe the earth is round. You speak in rhymes. Your answers are short."
initial_user_prompt = "Is the earth round?"
num_dialogue_turns = 3
gpt_model_1 = "gpt-3.5-turbo"
gpt_model_2 = "gpt-3.5-turbo"
audio_model_1 = "tts-1"
audio_model_2 = "tts-1"
voice_1 = "alloy"
voice_2 = "onyx"


########################################################################################################################
def content_str_to_dict(content, role):
    return {"role": role, "content": content}


client = OpenAI()
messages_1 = [content_str_to_dict(instruction_str_system_1, role="system")]
messages_2 = [content_str_to_dict(instruction_str_system_2, role="system")]
assistant_2_str = initial_user_prompt
audio_path = "./audio_files"
if not os.path.isdir("./audio_files"):
    os.mkdir("./audio_files")

for turn in range(num_dialogue_turns):
    messages_1 += [content_str_to_dict(assistant_2_str, role="user")]
    response_1 = client.chat.completions.create(model=gpt_model_1, messages=messages_1)
    assistant_1_str = response_1.choices[0].message.content
    messages_1 += [content_str_to_dict(assistant_1_str, role="assistant")]
    print(assistant_1_str)
    response = openai.audio.speech.create(model=audio_model_1, voice=voice_1, input=assistant_1_str, speed=1)
    response.stream_to_file(f"{audio_path}/{turn}-ast1.mp3")

    # Create a wav file from the mp3
    sound = AudioSegment.from_mp3(f"{audio_path}/{turn}-ast1.mp3")
    sound.export(f"{audio_path}/{turn}-ast1.wav", format="wav")
    wave_obj_1 = sa.WaveObject.from_wave_file(f"{audio_path}/{turn}-ast1.wav")
    if turn > 0:
        play_obj_2.wait_done()
    play_obj_1 = wave_obj_1.play()

    messages_2 += [content_str_to_dict(assistant_1_str, role="user")]
    response_2 = client.chat.completions.create(model=gpt_model_2, messages=messages_2)
    assistant_2_str = response_2.choices[0].message.content
    messages_2 += [content_str_to_dict(assistant_2_str, role="assistant")]
    print(assistant_2_str)
    response = openai.audio.speech.create(model=audio_model_2, voice=voice_2, input=assistant_2_str, speed=1)
    response.stream_to_file(f"{audio_path}/{turn}-ast2.mp3")

    # Create a wav file from the mp3
    sound = AudioSegment.from_mp3(f"{audio_path}/{turn}-ast2.mp3")
    sound.export(f"{audio_path}/{turn}-ast2.wav", format="wav")
    wave_obj_2 = sa.WaveObject.from_wave_file(f"{audio_path}/{turn}-ast2.wav")
    play_obj_1.wait_done()
    play_obj_2 = wave_obj_2.play()

play_obj_2.wait_done()
