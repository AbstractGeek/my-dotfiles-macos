#!/usr/bin/env python3

## Imports
import json
import os
import sys
import yaml
import logging
from time import strftime, localtime
from pprint import pprint

## Constants
config_default = "~/.config/koreader2obsidian.yml"

## Functions
def find_in_template(content, matchstr, unique=True):
    """Find matchstr in tex_content list."""
    doc_match = [i for i, line in enumerate(content.split("\n")) if matchstr in line]

    if not (len(doc_match) == 1):
        print("Multiple/No " + matchstr + " found in generated tex file.")
        sys.exit()
    else:
        doc_match = doc_match[0]
    return doc_match


def format_highlights(highlights, summary_content, note_styles):
    """Format json highlights to markdown."""
    # Add yaml metadata
    output = ["---"]
    output.append("title: " + highlights["title"])
    output.append("author: " + highlights["author"])
    output.append("exported-on: " + strftime('%Y-%m-%d %H:%M:%S', localtime(highlights["created_on"])))
    # add more metadata here, if required
    output.append("---")

    # Subtitles
    output.append("## Summary")
    output.append(summary_content)
    output.append("## Highlights")

    # Format highlights
    current_chapter = ""
    for highlight in highlights["entries"]:
        # Get style
        style = note_styles[highlight["drawer"]]
        # Get chapter
        if highlight["chapter"] != current_chapter:
            output.append("### " + highlight["chapter"])
            current_chapter = highlight["chapter"]
        # Format highlight
        output.append("##### Page " + str(highlight["page"]))
        output.append(highlight["text"])
        if "note" in highlight:
            output.append("> [!"+ style["type"] + "] " + style["title"])
            output.append("> " + highlight["note"])
        output.append("") # Add empty line

    return output


## Main
def main(json_file, output_file, config_file):

    # Load config
    with open(config_file, "r") as f:
        read_data = f.read()
    config = yaml.safe_load(read_data)

    # Get log file 
    log_file = os.path.expanduser(config["log_file"])

    # Set up logging
    logging.basicConfig(
        filename=os.path.expanduser(log_file),
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
    )

    # Load json
    with open(json_file, "r") as f:
        json_data = json.load(f)

    # Get output file
    if not output_file:
        output_folder = config["output_folder"]
        # get filename from json book title and santize it (stackoverflow: 7406102)
        outfilename = "".join(c for c in json_data["title"] if c.isalnum() or c in (' ','.','_')).rstrip()
        output_file = os.path.join(
            output_folder, outfilename + ".md"
        )
        

    # Load old file and check if there is a custom written summary file
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            output_content = f.read()
        summary_start = find_in_template(output_content, "{% summary start %}")
        summary_end = find_in_template(output_content, "{% summary end %}")
        summary_content = output_content.split("\n")[summary_start:summary_end+1]
        summary_content = "\n".join(summary_content)
    else:
        summary_content = "{% summary start %} \n{% summary end %} \n"



    # Format highlights
    highlights = format_highlights(json_data, summary_content, config["note_styles"])
    #pprint(highlights)

    # Write to file
    with open(output_file, "w") as f:
        f.write("\n".join(highlights))


# get path
if __name__ == "__main__":
    # get argument
    if len(sys.argv) == 2:
        json_file = os.path.expanduser(sys.argv[1])
        output_file = False
        config_file = os.path.expanduser(config_default)
    elif len(sys.argv) == 3:
        json_file = os.path.expanduser(sys.argv[1])
        output_file = os.path.expanduser(sys.argv[2])   
        config_file = os.path.expanduser(config_default)
    elif len(sys.argv) == 4:
        json_file = os.path.expanduser(sys.argv[1])
        output_file = os.path.expanduser(sys.argv[2]) 
        config_file = os.path.expanduser(sys.argv[3])
    else:
        print("Usage: koreader2obsidian.py json_file output_file config_file")
        sys.exit(1)

    # check if config file exists
    if not os.path.exists(config_file):
        print(config_file)
        print("Config file does not exist")
        sys.exit(1)

    # run main
    main(json_file, output_file, config_file)