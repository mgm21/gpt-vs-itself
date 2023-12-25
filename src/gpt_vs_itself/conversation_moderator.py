import simpleaudio as sa
from pydub import AudioSegment
import os
import numpy as np


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

        # Create 'dummy' 50 millisecond silence audio to be able to initially check whether play_obj_2 is done
        silence = np.zeros((1, 2))
        play_obj_2 = sa.play_buffer(silence, 1, 2, 44100)

        for turn in range(self.num_dialogue_turns):
            play_obj_1 = self._perform_turn(speaker=self.assistant_1,
                                            opponent=self.assistant_2,
                                            turn=turn,
                                            opponent_play_obj=play_obj_2)

            play_obj_2 = self._perform_turn(speaker=self.assistant_2,
                                            opponent=self.assistant_1,
                                            turn=turn,
                                            opponent_play_obj=play_obj_1)

        play_obj_2.wait_done()

    def _perform_turn(self, speaker, opponent, turn, opponent_play_obj):
        # Produce speaker text and audio response
        resp_str, resp_audio = speaker.produce_response_to_msg(msg=opponent.current_str)
        # Save speaker text response
        self._add_line_to_transcript(message=resp_str, messenger_name=speaker.name)
        # Save speaker audio response
        resp_audio_loc = self._save_audio_response(audio_response=resp_audio,
                                                   turn=turn,
                                                   speaker_name=speaker.name)
        # Play speaker audio response
        speaker_wav_obj = sa.WaveObject.from_wave_file(f"{resp_audio_loc}.wav")
        opponent_play_obj.wait_done()
        speaker_play_obj = speaker_wav_obj.play()
        # Print speaker text response
        print(f"{speaker.name}: {resp_str}")

        # NB putting the print statement here instead of before wait done allows text and voice to be output at the same
        # time. If you would like to see the text as soon as it is generated (before the voice has even started), then
        # place the print statement above the comment # Play speaker audio response.

        return speaker_play_obj

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
