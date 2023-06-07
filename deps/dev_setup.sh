#!/bin/bash
# shellcheck disable=SC2162
set -e

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

if [[ $(whoami) != "root" ]]; then
  if ! command -v sudo &> /dev/null; then
    echo "Sudo or root required to run script"
    exit 1
  else
    YESNO="y"
    echo "I noticed you're not running as root. In the case,"
    echo "I will use 'sudo' to install package and such."
    read -e -p "Continue [Yn]" YESNO
    if [[ "x$YESNO" == "xn" ]]; then
      exit 1
    fi
    sudo -p "Please enter your sudo password to install dependencies: " echo
  fi
fi

sudo apt-get update

sudo DEBIAN_FRONTEND=noninteractive apt-get install python3 python3-dev patchelf -y

# Poetry Specific
# Do not run the config lines as sudo!!!!!
# Setup and install poetry
poetry install

