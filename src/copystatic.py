import os
import shutil

def copy_files(source_path, destination_path):
    for item in os.listdir(source_path):
        new_source_path = os.path.join(source_path, item)

        if os.path.isfile(new_source_path):
            print(f"Copying File: {os.path.basename(item)}")
            shutil.copy(new_source_path, destination_path)
        else:
            new_destination_path = os.path.join(destination_path, item)
            print(f"Creating subdirectory: {new_destination_path}")
            os.mkdir(new_destination_path)
            copy_files(new_source_path, new_destination_path)