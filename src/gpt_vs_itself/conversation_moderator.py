import simpleaudio as sa
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
        if not os.path.isdir(results_folder_path):
            os.mkdir(results_folder_path)

        self.transcription_file_path = f"{self.results_folder_path}/transcription.txt"
        self._set_up_transcript_file()

    def play_conversation(self):
        self.assistant_2.current_str = self.initial_user_prompt

        for turn in range(self.num_dialogue_turns):
            # TODO: can make the following more scalable to more agents using a for loop over assistants
            # Produce and speak assistant 1 response
            self.assistant_1.produce_response_to_msg(msg=self.assistant_2.current_str, turn=turn)
            wave_obj_1 = sa.WaveObject.from_wave_file(f"{self.assistant_1.curr_audio_response_location}.wav")
            if turn > 0:
                play_obj_2.wait_done()
            play_obj_1 = wave_obj_1.play()

            # Save text of message to transcript
            assistant_1_message = self.assistant_1.current_str
            self._add_line_to_transcript(message=assistant_1_message, messenger_name=self.assistant_1.name)

            # Produce and speak assistant 2 response
            self.assistant_2.produce_response_to_msg(msg=self.assistant_1.current_str, turn=turn)
            wave_obj_2 = sa.WaveObject.from_wave_file(f"{self.assistant_2.curr_audio_response_location}.wav")
            play_obj_1.wait_done()
            play_obj_2 = wave_obj_2.play()

            # Save text of message to transcript
            assistant_2_message = self.assistant_2.current_str
            self._add_line_to_transcript(message=assistant_2_message, messenger_name=self.assistant_2.name)

        play_obj_2.wait_done()

    def _set_up_transcript_file(self):
        with open(self.transcription_file_path, mode="w"):
            pass

    def _add_line_to_transcript(self, message, messenger_name):
        with open(self.transcription_file_path, mode="a") as f:
            f.write(f"{messenger_name}: {message} \n")
