from assistant import Assistant
from conversation_moderator import ConversationModerator
import utils

parameters = {
    "instruction_str_system_1": "You are a debater who loves AI. You speak in rhymes. You answer in under 2 sentences.",
    "instruction_str_system_2": "You are a debater who dislikes AI. You speak in rhymes. You answer in under 2 "
                                "sentences.",
    "initial_user_prompt": "Do you love AI?",
    "num_dialogue_turns": 2,
    "gpt_model_1": "gpt-3.5-turbo",
    "gpt_model_2": "gpt-3.5-turbo",
    "audio_model_1": "tts-1",
    "audio_model_2": "tts-1",
    "voice_1": "nova",
    "voice_2": "echo",
    "name_1": "Assistant 1",
    "name_2": "Assistant 2"
}

results_folder_path = utils.configure_results_folder(**parameters)

assistant1 = Assistant(instruction_str_system=parameters["instruction_str_system_1"],
                       gpt_model=parameters["gpt_model_1"],
                       audio_model=parameters["audio_model_1"],
                       voice=parameters["voice_1"],
                       name=parameters["name_1"],
                       results_folder_path=results_folder_path)

assistant2 = Assistant(instruction_str_system=parameters["instruction_str_system_2"],
                       gpt_model=parameters["gpt_model_2"],
                       audio_model=parameters["audio_model_2"],
                       voice=parameters["voice_2"],
                       name=parameters["name_2"],
                       results_folder_path=results_folder_path)

conversation_moderator = ConversationModerator(assistant_1=assistant1,
                                               assistant_2=assistant2,
                                               initial_user_prompt=parameters["initial_user_prompt"],
                                               num_dialogue_turns=parameters["num_dialogue_turns"])

conversation_moderator.play_conversation()
