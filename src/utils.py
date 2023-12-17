import os
import datetime


def create_timestamped_results_folder():
    parent_results_folder = f"../audio_files"
    if not os.path.isdir(parent_results_folder):
        os.mikdir(parent_results_folder)

    now = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

    results_folder_path = f"{parent_results_folder}/{now}"
    if not os.path.isdir(results_folder_path):
        os.mkdir(results_folder_path)

    return results_folder_path
