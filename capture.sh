#!/bin/bash

# Get the primary network interface
interface=$(ip route | grep default | awk '{print $5}' | head -n 1)

output_dir="/tmp/pcaps"
mkdir -p $output_dir

# Change ownership of the output directory to tcpdump user
sudo chown tcpdump:tcpdump $output_dir

echo "Press Ctrl+C to stop the packet capture."

sudo tcpdump -i "$interface" -C 100 -G 3600 -w "$output_dir/output.pcap"

