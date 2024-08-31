#!/usr/bin/env python3

## Imports
import hashlib
import os
import sys
import pickle
import subprocess
import logging
import yaml

## Constants
config_default = "~/.config/convert_supernotes/config.yml"

## Functions
def find_hashes(root_dir, ext):
    # Set output list
    file_hashes = {}
    # Iterate over all items in the directory
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        # Check if the item is a file or a directory
        if os.path.isfile(item_path) and item_path.endswith(ext):
            # Find hash of the file
            file_hashes[item_path] = find_file_hash(item_path)
        elif os.path.isdir(item_path):
            # Recurse into the directory
            print("Entering directory: ", item_path)
            dir_file_hashes = find_hashes(item_path, ext)
            file_hashes = {**file_hashes, **dir_file_hashes}
    # return hashes
    return file_hashes


def find_file_hash(filename):
    # Find hash of the file
    with open(filename, "rb") as f:
        digest = hashlib.file_digest(f, "blake2b")
    return digest.hexdigest()


def convert_supernotes(note, supernote_tool_path, dest_file=None):
    # Generate pdf/txt name based on dest_dir
    if dest_file is None:
        # Get filename
        pdf_name = os.path.join(
            os.path.dirname(note), os.path.splitext(os.path.basename(note))[0] + ".pdf"
        )
        txt_name = os.path.join(
            os.path.dirname(note), os.path.splitext(os.path.basename(note))[0] + ".txt"
        )
    else:
        # Get filename
        pdf_name = dest_file + ".pdf"
        txt_name = dest_file + ".txt"

    # Convert to pdf
    subprocess.run(
        [
            os.path.expanduser(supernote_tool_path),
            "convert",
            "-t",
            "pdf",
            "-a",
            note,
            pdf_name,
        ]
    )
    # Extract text
    subprocess.run(
        [
            os.path.expanduser(supernote_tool_path),
            "convert",
            "-t",
            "txt",
            "-a",
            note,
            txt_name,
        ]
    )

    # Log completed pdf
    logging.info("Converted to pdf (and txt if applicable): %s", pdf_name)


## Main
def main(config_file):
    # Load config
    with open(config_file, "r") as f:
        read_data = f.read()
    config = yaml.safe_load(read_data)

    # Get log file and supernote tool path
    log_file = os.path.expanduser(config["log_file"])
    supernote_tool_path = os.path.expanduser(config["supernote_tool_path"])

    # Set up logging
    logging.basicConfig(
        filename=os.path.expanduser(log_file),
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
    )

    if config["root_mode"]:
        # Start conversion
        logging.info("[root_mode] Starting conversion")

        # Get root directory
        root_dir = os.path.expanduser(config["root_dir"])

        # Get hashes
        new_hashes = find_hashes(root_dir, ".note")

        # Load old hashes and update new or changed files
        if os.path.exists(os.path.join(root_dir, "hashes.pickle")):
            with open(os.path.join(root_dir, "hashes.pickle"), "rb") as handle:
                old_hashes = pickle.load(handle)
            for key, value in new_hashes.items():
                if key in old_hashes:
                    if value != old_hashes[key]:
                        logging.info("[root_mode] File changed: %s", key)
                        convert_supernotes(key,supernote_tool_path)
                    # else:
                    #     print("File unchanged")
                    #     logging.info("File unchanged: %s", key)
                else:
                    logging.info("[root_mode] New file: %s", key)
                    convert_supernotes(key, supernote_tool_path)

        else:
            for key in new_hashes:
                logging.info("[root_mode] New file: %s", key)
                convert_supernotes(key, supernote_tool_path)

        # Save new hashes
        with open(os.path.join(root_dir, "hashes.pickle"), "wb") as handle:
            pickle.dump(new_hashes, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logging.info("[root_mode] Completed conversion, exiting")

    if config["single_mode"]:
        # Start conversion
        logging.info("[root_mode] Starting conversion")

        # Check src and dest lengths
        if len(config["src_files"]) != len(config["dest_files"]):
            logging.error("Length of src_files and dest_files not equal, exiting")
            sys.exit(1)
        
        # get config dir
        config_dir = os.path.dirname(config_file)

        # get hashes
        new_hashes = {}
        for src in config["src_files"]:
            item_path = os.path.expanduser(src)
            new_hashes[item_path] = find_file_hash(item_path)

        # Load old hashes and update new or changed files
        if os.path.exists(os.path.join(config_dir, "hashes.pickle")):
            with open(os.path.join(config_dir, "hashes.pickle"), "rb") as handle:
                old_hashes = pickle.load(handle)
            for key, value, dest in zip(new_hashes.keys(), new_hashes.values(), config["dest_files"]):
                if key in old_hashes:
                    if value != old_hashes[key]:
                        logging.info("[single_mode] File changed: %s", key)
                        convert_supernotes(key, supernote_tool_path, dest)
                    # else:
                    #     print("File unchanged")
                    #     logging.info("File unchanged: %s", key)
                else:
                    logging.info("[single_mode] New file: %s", key)
                    convert_supernotes(key, supernote_tool_path, dest)
 
        else:
            # first time running the code
            for key, dest in zip(new_hashes.keys(), config["dest_files"]):
                logging.info("[single_mode] New file: %s", key)
                convert_supernotes(key, supernote_tool_path, dest)

        # Save new hashes
        with open(os.path.join(config_dir, "hashes.pickle"), "wb") as handle:
            pickle.dump(new_hashes, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logging.info("[single_mode] Completed conversion, exiting")


 
        


# get path
if __name__ == "__main__":
    # get argument
    if len(sys.argv) == 1:
        config_file = os.path.expanduser(config_default)
    elif len(sys.argv) == 2:
        config_file = os.path.expanduser(sys.argv[2])         
    else:
        print("Usage: convert_supernotes.py <path>")
        sys.exit(1)

    # check if config file exists
    if not os.path.exists(config_file):
        print(config_file)
        print("Config file does not exist")
        sys.exit(1)

    # run main
    main(config_file)
