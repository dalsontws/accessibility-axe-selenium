#!/bin/bash

echo -e "\n=========================="
echo -e "hats for Mac installer."
echo -e "==========================\n"

echo -e "\n===================================="
echo -e "Password is your login password"
echo -e "====================================\n"

sudo echo ""

echo -e "Install brew if currently not installed"
if [ ! -f /usr/local/bin/brew ]; then
	echo -e "	Installing Brew..."
	
	ruby \
  	-e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" \
  	</dev/null
  	
  	brew update
fi

echo -e "Install Ansible if currently not installed"
if [ ! -f /usr/local/bin/ansible-playbook ]; then
	echo -e "	Installing Ansible..."
	brew install ansible 
else
	brew upgrade ansible
fi


#. ~/.bash_profile


echo -e "Making Directories"
mkdir ~/accessibility-testing
cd ~/accessibility-testing
# mkdir python-axe-selenium
# cd python-axe-selenium
svn checkout https://github.com/dalsontws/accessibility-axe-selenium/trunk/python-axe-selenium
cd python-axe-selenium

echo -e "Running Playbooks"

ansible-playbook ansible/ansible-task-install-packages.yml -i ansible/inventory.yml -c local

echo -e "\n===================================="
echo -e "Install complete. Please re-open your terminal.\n"
echo -e "====================================\n"