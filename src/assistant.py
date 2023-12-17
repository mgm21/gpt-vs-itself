import openai
from openai import OpenAI
from pydub import AudioSegment
import os

class Assistant:
    def __init__(self,
                 instruction_str_system,
                 gpt_model,
                 audio_model,
                 voice,
                 name,
                 results_folder_path="../audio_files"):
        self.instruction_str_system = instruction_str_system
        self.gpt_model = gpt_model
        self.audio_model = audio_model
        self.voice = voice
        self.messages = [self._convert_content_str_to_dict(instruction_str_system, role="system")]
        self.current_str = ""
        self.client = OpenAI()
        self.name = name

        self.audio_path = results_folder_path
        if not os.path.isdir(results_folder_path):
            os.mkdir(results_folder_path)

        self.curr_audio_response_location = None

    def produce_response_to_msg(self, msg, turn):
        # Append msg from other character/agent to list of messages
        self.messages += [self._convert_content_str_to_dict(content=msg, role="user")]

        # Fetch response from remote GPT model
        response = self.client.chat.completions.create(model=self.gpt_model, messages=self.messages)
        response_content_str = response.choices[0].message.content
        self.messages += [self._convert_content_str_to_dict(content=response_content_str, role="assistant")]
        print(f"{self.name}: {response_content_str}")

        # Produce and save audio response as mp3
        audio_response = openai.audio.speech.create(model=self.audio_model,
                                                    voice=self.voice,
                                                    input=response_content_str,
                                                    speed=1)
        self.curr_audio_response_location = f"{self.audio_path}/{turn}-{self.name}"
        audio_response.stream_to_file(f"{self.curr_audio_response_location}.mp3")

        # Convert and save audio response to and as wav
        mp3_sound = AudioSegment.from_mp3(f"{self.curr_audio_response_location}.mp3")
        mp3_sound.export(f"{self.curr_audio_response_location}.wav", format="wav")

    def _convert_content_str_to_dict(self, content, role):
        return {"role": role, "content": content}
