import simpleaudio as sa
from pydub import AudioSegment
import os


class ConversationModerator:
    def __init__(self,
                 assistant_1,
                 assistant_2,
                 initial_user_prompt="Hi there",
                 num_dialogue_turns=3,
                 results_folder_path="/results"):
        self.assistant_1 = assistant_1
        self.assistant_2 = assistant_2

        self.initial_user_prompt = initial_user_prompt
        self.num_dialogue_turns = num_dialogue_turns

        self.results_folder_path = results_folder_path
        self._set_up_results_folder()

        self.transcription_file_path = f"{self.results_folder_path}/transcription.txt"
        self._set_up_transcript_file()

    def play_conversation(self):
        self.assistant_2.current_str = self.initial_user_prompt

        for turn in range(self.num_dialogue_turns):
            # Produce assistant 1 text and audio response
            resp_str, resp_audio = self.assistant_1.produce_response_to_msg(msg=self.assistant_2.current_str)

            # Save assistant 1 text response
            self._add_line_to_transcript(message=resp_str, messenger_name=self.assistant_1.name)

            # Save assistant 1 audio response
            resp_audio_loc = self._save_audio_response(audio_response=resp_audio,
                                                       turn=turn,
                                                       speaker_name=self.assistant_1.name)

            # Play assistant 1 audio response
            wave_obj_1 = sa.WaveObject.from_wave_file(f"{resp_audio_loc}.wav")
            if turn > 0:
                play_obj_2.wait_done()
            play_obj_1 = wave_obj_1.play()

            # Produce assistant 2 text and audio response
            resp_str, resp_audio = self.assistant_2.produce_response_to_msg(msg=self.assistant_1.current_str)

            # Save assistant 2 text response
            self._add_line_to_transcript(message=resp_str, messenger_name=self.assistant_2.name)

            # Save assistant 2 audio response
            resp_audio_loc = self._save_audio_response(audio_response=resp_audio,
                                                       turn=turn,
                                                       speaker_name=self.assistant_2.name)
            
            # Play assistant 2 audio response
            wave_obj_2 = sa.WaveObject.from_wave_file(f"{resp_audio_loc}.wav")
            play_obj_1.wait_done()
            play_obj_2 = wave_obj_2.play()

        play_obj_2.wait_done()

    def _set_up_transcript_file(self):
        with open(self.transcription_file_path, mode="w"):
            pass

    def _add_line_to_transcript(self, message, messenger_name):
        with open(self.transcription_file_path, mode="a") as f:
            f.write(f"{messenger_name}: {message} \n")

    def _set_up_results_folder(self):
        if not os.path.isdir(self.results_folder_path):
            os.mkdir(self.results_folder_path)

    def _save_audio_response(self, audio_response, turn, speaker_name):
        audio_response_location = f"{self.results_folder_path}/{turn}-{speaker_name}"
        audio_response.stream_to_file(f"{audio_response_location}.mp3")

        # Convert to and save audio response as wav
        mp3_sound = AudioSegment.from_mp3(f"{audio_response_location}.mp3")
        mp3_sound.export(f"{audio_response_location}.wav", format="wav")

        return audio_response_location
