import openai
from openai import OpenAI


class Assistant:
    def __init__(
        self,
        instruction_str_system,
        gpt_model,
        audio_model,
        voice,
        name,
    ):
        self.instruction_str_system = instruction_str_system
        self.gpt_model = gpt_model
        self.audio_model = audio_model
        self.voice = voice
        self.messages = [
            self._convert_content_str_to_dict(instruction_str_system, role="system")
        ]
        self.current_str = ""
        self.client = OpenAI()
        self.name = name

        self.curr_audio_response_location = None

    def produce_response_to_msg(self, msg):
        # Append msg from other character/agent to list of messages
        self.messages += [self._convert_content_str_to_dict(content=msg, role="user")]

        # Fetch response from remote GPT model
        response = self.client.chat.completions.create(
            model=self.gpt_model, messages=self.messages
        )

        # Extract response string and append it to messages
        response_content_str = response.choices[0].message.content
        self.messages += [
            self._convert_content_str_to_dict(
                content=response_content_str, role="assistant"
            )
        ]

        self.current_str = self.messages[-1]["content"]

        assert self.current_str == response_content_str

        print(f"{self.name}: {response_content_str}")

        # Produce and save audio
        audio_response = openai.audio.speech.create(
            model=self.audio_model,
            voice=self.voice,
            input=response_content_str,
            speed=1,
        )

        return response_content_str, audio_response

    def _convert_content_str_to_dict(self, content, role):
        return {"role": role, "content": content}
