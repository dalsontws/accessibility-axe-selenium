#!/bin/bash

echo -e "\n=========================="
echo -e "hats for Mac installer."
echo -e "==========================\n"

echo -e "\n===================================="
echo -e "Password is your login password"
echo -e "====================================\n"

sudo echo ""

echo -e "Install Ansible if currently not installed"
if [ ! -f /usr/local/bin/ansible-playbook ]; then
	echo -e "	Installing Ansible..."
	pip install ansible 
else
	pip upgrade ansible
fi

. ~/.bash_profile


echo -e "Making Directories"
mkdir ~/accessibility-testing
cd ~/accessibility-testing

svn checkout https://github.com/dalsontws/accessibility-axe-selenium/trunk/python-axe-selenium
cd python-axe-selenium

echo -e "Running Playbooks"

ansible-playbook ansible/ansible-task-install-packages.yml -i ansible/inventory.yml -c local

echo -e "\n===================================="
echo -e "Install complete. Please re-open your terminal.\n"
echo -e "====================================\n"

/venv/bin/python axeSelenium.py
