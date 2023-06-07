import argparse
import glob
import json
import os
import pprint
import subprocess
import tempfile


def run_nfdump(nfcapd_file):
    """Run nfdump command and capture the JSON output"""
    command = ["nfdump", "-r", nfcapd_file, "-n", "-N", "-o", "json", "-O", "bytes"]
    output = subprocess.check_output(command)

    # Decode the JSON output
    json_output = output.decode("utf-8")

    # Convert the JSON string to a dictionary
    data = json.loads(json_output)

    return data


def convert_pcap(input_pcap, output_dir):
    """Convert pcap file using nfpcapd and return a list of file paths"""
    # Create a temporary directory for the output files
    temp_dir = tempfile.mkdtemp()

    # Run nfpcapd command
    command = ["nfpcapd", "-r", input_pcap, "-l", temp_dir]
    subprocess.run(command, check=True)

    # Get the paths of the output files
    file_paths = glob.glob(os.path.join(temp_dir, "nfcapd.*"))

    # Return the list of file paths
    return file_paths


def process_nfcapd_files(nfcapd_files):
    """Process nfcapd files and return an output dictionary"""
    output_dict = {}

    for nfcapd_file in nfcapd_files:
        # Extract the file name without the path
        file_name = os.path.basename(nfcapd_file)

        # Run nfdump and capture the JSON output
        json_output = run_nfdump(nfcapd_file)

        # Add the JSON output to the dictionary
        output_dict[file_name] = json_output

    return output_dict


def main():
    """Main function"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Convert pcap file and run nfdump")
    parser.add_argument("input_pcap", help="Path to the input pcap file")
    args = parser.parse_args()

    # Create the output directory using tempfile
    output_dir = tempfile.mkdtemp()

    # Create an empty output dictionary
    output_dict = {}

    # Convert the pcap file
    nfcapd_files = convert_pcap(args.input_pcap, output_dir)

    # Process the nfcapd files
    output_dict = process_nfcapd_files(nfcapd_files)

    # Access the JSON output for a specific file
    if nfcapd_files:
        file_name = os.path.basename(nfcapd_files[0])
        json_output = output_dict[file_name]

        output_dict[file_name] = json_output
        # Perform further processing as needed

    else:
        print("No nfcapd files generated.")

    # Pretty-print the output dictionary
    pprint.pprint(output_dict)


if __name__ == "__main__":
    main()
