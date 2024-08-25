#!/bin/bash

# Update package lists
apt-get update

# Install Graphviz and its dependencies
apt-get install -y graphviz

# Verify Graphviz installation
dot -V

# Add Graphviz to the system's PATH
echo 'export PATH=$PATH:/usr/bin' >> ~/.bashrc
source ~/.bashrc

# Install Python dependencies
pip install -r requirements.txt

# Print the current PATH for debugging
echo "Current PATH: $PATH"

# List contents of /usr/bin to verify Graphviz binaries
ls -l /usr/bin/dot