#!/bin/bash

source .venv/bin/activate
alias repl="sudo mpremote connect port:/dev/ttyACM0"

if [[ -e config.py ]]; then
    echo "Existing Wi-Fi config detected"
else
    echo "No Wi-Fi config detected, enter credentials"
    echo -n "SSID: "
    read wifi_ssid
    echo -n "password: "
    read -s wifi_password
    echo; echo
    touch config.py
    echo "WIFI_SSID='$wifi_ssid'\nWIFI_PASSWORD='$wifi_password'" > config.py
fi

echo "Loading Wi-Fi config..."
repl cp config.py :
echo "Done"

echo "Loading system controllers..."
repl fs cp -r controllers/* :
echo "Done"

echo "Loading views..."
repl fs cp -r views/* :
echo "Done"

echo "-------------------"
echo "Available commands:"
echo "repl - to open micropython interactive prompt (read-eval-print loop)"
echo "repl \$1 - to run mpremote commands on pico"
echo "run \$1 - to run your scripts"
alias run="repl run"
