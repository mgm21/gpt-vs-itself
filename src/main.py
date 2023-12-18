from assistant import Assistant
from conversation_moderator import ConversationModerator
import utils
import definitions
import yaml

with open(definitions.CONFIG_PATH) as f:
    PARAMS = yaml.load(f, Loader=yaml.BaseLoader)

results_folder_path = utils.configure_results_folder(**PARAMS)

assistant1 = Assistant(instruction_str_system=PARAMS["instruction_str_system_1"],
                       gpt_model=PARAMS["gpt_model_1"],
                       audio_model=PARAMS["audio_model_1"],
                       voice=PARAMS["voice_1"],
                       name=PARAMS["name_1"],
                       results_folder_path=results_folder_path)

assistant2 = Assistant(instruction_str_system=PARAMS["instruction_str_system_2"],
                       gpt_model=PARAMS["gpt_model_2"],
                       audio_model=PARAMS["audio_model_2"],
                       voice=PARAMS["voice_2"],
                       name=PARAMS["name_2"],
                       results_folder_path=results_folder_path)

conversation_moderator = ConversationModerator(assistant_1=assistant1,
                                               assistant_2=assistant2,
                                               initial_user_prompt=PARAMS["initial_user_prompt"],
                                               num_dialogue_turns=PARAMS["num_dialogue_turns"])

conversation_moderator.play_conversation()