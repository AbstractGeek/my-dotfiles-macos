#!/usr/bin/env python3

## Imports
import hashlib
import os
from itertools import chain
import pickle
import subprocess
import logging
import yaml
import sys

## Constants
config_default = "~/.config/cronpy/supernote_zotfile.yml"

## Functions
def find_file_hash(filename):
    # Find hash of the file
    with open(filename, "rb") as f:
        digest = hashlib.file_digest(f, "blake2b")
    return digest.hexdigest()

## Main
def main(config_file):
    # Load config
    with open(config_file, "r") as f:
        read_data = f.read()
    config = yaml.safe_load(read_data)
   
    # Get yaml config
    log_file = os.path.expanduser(config["log_file"])
    zotfile_folder = os.path.expanduser(config["zotfile_folder"])
    markfile_folder = os.path.expanduser(config["markfile_folder"])
    supernote_folder = os.path.expanduser(config["supernote_folder"])
    export_folder = os.path.expanduser(config["export_folder"])
    config_folder = os.path.dirname(config_file)

    # Set up logging
    logging.basicConfig(
        filename=os.path.expanduser(log_file),
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
    )

    zotfile_hashes = [(f, find_file_hash(os.path.join(zotfile_folder, f))) 
                      for f in os.listdir(zotfile_folder) if f.endswith('.pdf')]
    export_pdfs = [f for f in os.listdir(export_folder) if f.endswith('.pdf')]   
    supernote_pdfs = [f for f in os.listdir(supernote_folder) if f.endswith('.pdf')]   

    # # debug
    # print("Zotfile hashes: " + str(zotfile_hashes))
    # print("Supernote pdfs: " + str(supernote_pdfs))
    # print("Export pdfs: " + str(export_pdfs))

    # move new files to supernote folder
    for f, _ in zotfile_hashes:
        if f not in supernote_pdfs:
            logging.info("New pdf in zotfile folder. Moving file: " + f)
            # copy file to supernote folder
            subprocess.run(["cp", os.path.join(zotfile_folder, f), supernote_folder])
            continue

    # compare hashes of zotfile and export files
    for f, h in zotfile_hashes:
        if f in export_pdfs:
            # get hash of export file
            export_hash = find_file_hash(os.path.join(export_folder, f))
            if h == export_hash:
                # do nothing
                continue
            else:   
                logging.info("Copying updated export file: " + f)
                # copy file to zotfile folder
                subprocess.run(["cp", os.path.join(export_folder, f), zotfile_folder])
                continue
        
    # clean up mode - compare zotfile hashes with old hashes
    # Get pickle file
    if os.path.exists(os.path.join(config_folder, "hashes.pickle")):
        with open(os.path.join(config_folder, "hashes.pickle"), "rb") as handle:
            old_hashes = pickle.load(handle)

        # compare hashes
        for f, h in old_hashes:
            if f not in chain.from_iterable(zotfile_hashes):
                logging.info("Main zotfile not found: " + f)
                
                # delete supernote file
                if os.path.isfile(os.path.join(supernote_folder, f)):
                    subprocess.run(["rm", os.path.join(supernote_folder, f)])
                    logging.info("Supernote file deleted: " + os.path.join(supernote_folder, f))

                # move mark file
                if os.path.isfile(os.path.join(supernote_folder, f+'.mark')):
                    subprocess.run(["mv", os.path.join(supernote_folder, f+'.mark'), markfile_folder])
                    logging.info("Moved mark file: " + os.path.join(supernote_folder, f+'.mark'))
                
                # delete export file
                if os.path.isfile(os.path.join(export_folder, f)):
                    subprocess.run(["rm", os.path.join(export_folder, f)])
                    logging.info("Export file deleted: " + os.path.join(export_folder, f))
                continue

    # save new hashes
    with open(os.path.join(config_folder, "hashes.pickle"), "wb") as handle:
        pickle.dump(zotfile_hashes, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    logging.info("supernote_zotfile: run completed.")
    
## Main
if __name__ == "__main__":
    # get argument
    if len(sys.argv) == 1:
        config_file = os.path.expanduser(config_default)
    elif len(sys.argv) == 2:
        config_file = os.path.expanduser(sys.argv[2])         
    else:
        print("Usage: supernote_zotfile.py <path>")
        sys.exit(1)

    # check if config file exists
    if not os.path.exists(config_file):
        print(config_file)
        print("Config file does not exist")
        sys.exit(1)

    # run main
    main(config_file)