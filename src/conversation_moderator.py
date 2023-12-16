import simpleaudio as sa


class ConversationModerator:
    def __init__(self, assistant_1, assistant_2, initial_user_prompt="Hi there", num_dialogue_turns=3):
        self.assistant_1 = assistant_1
        self.assistant_2 = assistant_2

        self.initial_user_prompt = initial_user_prompt
        self.num_dialogue_turns = num_dialogue_turns

    def play_conversation(self):
        self.assistant_2.current_str = self.initial_user_prompt

        for turn in range(self.num_dialogue_turns):
            # Produce and speak assistant 1 response
            self.assistant_1.produce_response_to_msg(msg=self.assistant_2.current_str, turn=turn)
            wave_obj_1 = sa.WaveObject.from_wave_file(f"{self.assistant_1.curr_audio_response_location}.wav")
            if turn > 0:
                play_obj_2.wait_done()
            play_obj_1 = wave_obj_1.play()

            # Produce and speak assistant 2 response
            self.assistant_2.produce_response_to_msg(msg=self.assistant_1.current_str, turn=turn)
            wave_obj_2 = sa.WaveObject.from_wave_file(f"{self.assistant_2.curr_audio_response_location}.wav")
            play_obj_1.wait_done()
            play_obj_2 = wave_obj_2.play()

        play_obj_2.wait_done()
