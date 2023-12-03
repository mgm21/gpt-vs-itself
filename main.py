import simpleaudio as sa
from assistant import Assistant

# Parameters
instruction_str_system_1 = "You are a debater who loves AI. You speak in rhymes. You answer in under 2 sentences."
instruction_str_system_2 = "You are a debater who dislikes AI. You speak in rhymes. You answer in under 2 sentences."
initial_user_prompt = "Do you love AI?"
num_dialogue_turns = 5
gpt_model_1 = "gpt-3.5-turbo"
gpt_model_2 = "gpt-3.5-turbo"
audio_model_1 = "tts-1"
audio_model_2 = "tts-1"
voice_1 = "nova"
voice_2 = "echo"

########################################################################################################################
assistant1 = Assistant(instruction_str_system=instruction_str_system_1,
                       gpt_model=gpt_model_1,
                       audio_model=audio_model_1,
                       voice=voice_1,
                       name="assistant_1")

assistant2 = Assistant(instruction_str_system=instruction_str_system_2,
                       gpt_model=gpt_model_2,
                       audio_model=audio_model_2,
                       voice=voice_2,
                       name="assistant_2")

assistant2.current_str = initial_user_prompt

for turn in range(num_dialogue_turns):
    # Produce and speak assistant 1 response
    assistant1.produce_response_to_msg(msg=assistant2.current_str, turn=turn)
    wave_obj_1 = sa.WaveObject.from_wave_file(f"{assistant1.curr_audio_response_location}.wav")
    if turn > 0:
        play_obj_2.wait_done()
    play_obj_1 = wave_obj_1.play()

    # Produce and speak assistant 2 response
    assistant2.produce_response_to_msg(msg=assistant1.current_str, turn=turn)
    wave_obj_2 = sa.WaveObject.from_wave_file(f"{assistant2.curr_audio_response_location}.wav")
    play_obj_1.wait_done()
    play_obj_2 = wave_obj_2.play()

play_obj_2.wait_done()
