import os
import datetime
import json


def configure_results_folder(**kwargs):
    results_folder_path = create_timestamped_results_folder()
    create_experiment_summary_file(results_folder_path, **kwargs)
    return results_folder_path


def create_timestamped_results_folder():
    parent_results_folder = f"../audio_files"
    if not os.path.isdir(parent_results_folder):
        os.mikdir(parent_results_folder)

    now = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

    results_folder_path = f"{parent_results_folder}/{now}"
    if not os.path.isdir(results_folder_path):
        os.mkdir(results_folder_path)

    return results_folder_path


def create_experiment_summary_file(results_folder_path, **kwargs):
    # Create the file at the results_folder_path
    with open(f'{results_folder_path}/experiment_summary.txt', 'w') as file:
        file.write(json.dumps(kwargs, indent=2))