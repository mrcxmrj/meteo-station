#!/bin/bash

source .venv/bin/activate
alias repl="sudo mpremote connect port:/dev/ttyACM0"

if [[ -e src/config.py ]]; then
    echo "Existing Wi-Fi config detected"
else
    echo "No Wi-Fi config detected, enter credentials"
    echo -n "SSID: "
    read wifi_ssid
    echo -n "password: "
    read -s wifi_password
    echo; echo
    touch src/config.py
    echo "WIFI_SSID='$wifi_ssid'\nWIFI_PASSWORD='$wifi_password'" > src/config.py
fi

echo "Loading source files..."
cd ./src && repl fs cp -r ./* : && cd ../
echo "Done"

echo "-------------------"
echo "Available commands:"
echo "repl - to open micropython interactive prompt (read-eval-print loop)"
echo "repl \$1 - to run mpremote commands on pico"
echo "run \$1 - to run your scripts"
echo "reload - to reload source files"
echo "nukefs - to clear filesystem"

alias run="repl run"
alias reload="echo \"Reloading files...\" && cd ./src && repl fs cp -r ./* : && cd ../"
alias nukefs="repl exec --no-follow \"import os, machine, rp2; os.umount('/'); bdev = rp2.Flash(); os.VfsLfs2.mkfs(bdev, progsize=256); vfs = os.VfsLfs2(bdev, progsize=256); os.mount(vfs, '/'); machine.reset()\""
