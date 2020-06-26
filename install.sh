#!/bin/bash

####################################
# Fashions Palettes Install Script #
####################################

if ! [[ $EUID -eq 0 ]]; then
   echo -e "${err} Install script must be run as sudo (sudo ./install.sh)"
   exit 1
fi

if ! [ -z ${1+x} ]; then
    echo "Usage: ./install.sh"
    exit 1
fi

cat <<EOF
#################
Fashions Palettes
#################
EOF

# Color codes
plus="\033[1;32m[+]\e[m"
warn="\033[1;33m[!]\e[m"
err="\033[1;31m[!]\e[m"

# Update package list and set list to check if package needs updating
echo -e "$plus Updating package list..."
apt update

# Check if a package is installed before trying to install it
install_package() {
    if ! (dpkg -l $1 > /dev/null 2>&1); then
        apt install -y $1 && echo -e "\t$plus Successfully installed $1." || echo -e "\t$err Installing $1 failed!"
    else
        echo -e "\t$plus Package $1 is already installed."
    fi
}

echo -e "\n$plus Installing dependencies..."
install_package python3
install_package python3-pip
install_package python3-dev
pip3 install -U requests timeout-decorator 
pip3 install -U Flask flask_login flask-wtf uwsgi

