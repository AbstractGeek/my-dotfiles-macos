#!/usr/bin/env python3

# Imports
import sys
import glob
import subprocess

def main(input_pattern, output_pattern, ffmpeg_command):


    # Get a list of input files
    input_files = glob.glob("*" + input_pattern)
    input_output_files = [(input_file, input_file.replace(input_pattern, output_pattern)) for input_file in input_files]    

    for input_file, output_file in input_output_files:
        # Display files to be converted
        print(input_file + ' -> ' + output_file)

        # Generate command
        cmd = [ input_file if txt=='#in' else output_file if txt=='#out' else txt for txt in ffmpeg_command ]
        print("Using ffmpeg command: " + " ".join(cmd))
        
        # Run ffmpeg command
        out = subprocess.run(" ".join(cmd), capture_output=True, text=True, shell=True)

        # Check if successful
        if out.returncode != 0:
            print("Error converting " + input_file)
            print(out.stdout)
            print(out.stderr)
            print("Moving on to the next file")
            break
        else:
            print("Successfully converted.")
        
        print("====================================")

if __name__ == "__main__":
    # Get arguments
    if len(sys.argv) != 4:
        print("Usage: batch_ffmpeg.py <input_pattern> <output_pattern> <ffmpeg command as string with #in and #out for input and output pattern locations>")
        sys.exit(1)
    else:
        print("input pattern: " + sys.argv[1])
        print("output pattern: " + sys.argv[2])
        print("ffmpeg command: " + sys.argv[3])
        print("====================================")

    main(sys.argv[1], sys.argv[2], sys.argv[3].split())

