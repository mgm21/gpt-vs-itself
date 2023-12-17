import os
import datetime
from assistant import Assistant
from conversation_moderator import ConversationModerator

# Parameters
instruction_str_system_1 = "You are a debater who loves AI. You speak in rhymes. You answer in under 2 sentences."
instruction_str_system_2 = "You are a debater who dislikes AI. You speak in rhymes. You answer in under 2 sentences."
initial_user_prompt = "Do you love AI?"
num_dialogue_turns = 2
gpt_model_1 = "gpt-3.5-turbo"
gpt_model_2 = "gpt-3.5-turbo"
audio_model_1 = "tts-1"
audio_model_2 = "tts-1"
voice_1 = "nova"
voice_2 = "echo"

# Prepare timestamped results folder
parent_results_folder = f"../audio_files"
if not os.path.isdir(parent_results_folder):
    os.mikdir(parent_results_folder)

now = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

results_folder_path = f"{parent_results_folder}/{now}"
if not os.path.isdir(results_folder_path):
    os.mkdir(results_folder_path)

assistant1 = Assistant(instruction_str_system=instruction_str_system_1,
                       gpt_model=gpt_model_1,
                       audio_model=audio_model_1,
                       voice=voice_1,
                       name="assistant_1",
                       results_folder_path=results_folder_path)

assistant2 = Assistant(instruction_str_system=instruction_str_system_2,
                       gpt_model=gpt_model_2,
                       audio_model=audio_model_2,
                       voice=voice_2,
                       name="assistant_2",
                       results_folder_path=results_folder_path)

conversation_moderator = ConversationModerator(assistant_1=assistant1,
                                               assistant_2=assistant2,
                                               initial_user_prompt=initial_user_prompt,
                                               num_dialogue_turns=num_dialogue_turns)

conversation_moderator.play_conversation()
