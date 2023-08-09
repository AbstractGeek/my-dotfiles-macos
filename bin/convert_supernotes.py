#!/usr/bin/env python3

## Imports
import hashlib
import os
import sys
import pickle
import subprocess
import logging

## Constants
log_file = "~/.local/logs/convert_supernotes.log"
supernote_tool_path = "~/.local/bin/supernote-tool"

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
            with open(item_path, "rb") as f:
                digest = hashlib.file_digest(f, "blake2b")
            file_hashes[item_path] = digest.hexdigest()
        elif os.path.isdir(item_path):
            # Recurse into the directory
            print("Entering directory: ", item_path)
            dir_file_hashes = find_hashes(item_path, ext)
            file_hashes = {**file_hashes, **dir_file_hashes}
    # return hashes
    return file_hashes

def convert_supernotes(note):
    # Get filename
    pdf_name = os.path.join(os.path.dirname(note), 
                            os.path.splitext(os.path.basename(note))[0] + ".pdf")
    txt_name = os.path.join(os.path.dirname(note), 
                            os.path.splitext(os.path.basename(note))[0] + ".txt")

    # Convert to pdf
    subprocess.run([os.path.expanduser(supernote_tool_path), "convert", "-t", "pdf", "-a", note, pdf_name ])
    # Extract text
    subprocess.run([os.path.expanduser(supernote_tool_path), "convert", "-t", "txt", "-a", note, txt_name ])
    
    # Log completed pdf
    logging.info("Converted to pdf (and txt if applicable): %s", pdf_name)


    


## Main
def main(root_dir):

    # Set up logging
    logging.basicConfig(filename=os.path.expanduser(log_file), level=logging.INFO, format='%(asctime)s - %(message)s')
    logging.info("Starting conversion")

    # Get hashes
    new_hashes = find_hashes(root_dir, ".note")

    # Load old hashes and update new or changed files
    if os.path.exists(os.path.join(root_dir, "hashes.pickle")):
        with open(os.path.join(root_dir, "hashes.pickle"), 'rb') as handle:
            old_hashes = pickle.load(handle)
        for key, value in new_hashes.items():
            if key in old_hashes:
                if value != old_hashes[key]:
                    logging.info("File changed: %s", key)
                    convert_supernotes(key)
                # else:
                #     logging.info("File unchanged: %s", key)
            else:
                logging.info("New file: %s", key)
                convert_supernotes(key)

    else:
        for key in new_hashes:
            logging.info("New file: %s", key)
            convert_supernotes(key)

    # Save new hashes
    with open(os.path.join(root_dir,'hashes.pickle'), 'wb') as handle:
        pickle.dump(new_hashes, handle, protocol=pickle.HIGHEST_PROTOCOL)
    logging.info("Completed conversion, exiting")


        


# get path
if __name__ == "__main__":
    # get argument
    if len(sys.argv) != 2:
        print("Usage: convert_supernotes.py <path>")
        sys.exit(1)
    
    # get path
    root_dir = os.path.expanduser(sys.argv[1])
    # check if path exists
    if not os.path.exists(root_dir):
        print("Path does not exist")
        sys.exit(1)
    # check if path is a directory
    if not os.path.isdir(root_dir):
        print("Path is not a directory")
        sys.exit(1)

    # run main
    main(root_dir)





