#!/bin/bash
# assumption that this is being installed from lubuntu with virtual box
# I recommend not running this script for other machines :)
# update apt get
echo "lubuntu" | sudo -S apt-get update
# uninstall previous versions of node and npm
sudo apt-get remove nodejs npm 
sudo apt-get purge nodejs
rm -rf "$HOME/.config/nvm"
# gets install file for nvm
wget https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash 
sudo chmod +x install.sh # makes install file executable
./install.sh
# restarts the script for nvm, node and npm to work
sudo chmod +x npm_install.sh

export NVM_DIR="$HOME/.config/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm 
nvm install 18.1.0 

echo "Now exit and reopen your terminal, cd into this folder once again and run sh npm_install.sh"




#sudo apt-get install -y nodejs
