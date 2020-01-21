# install and run.sh

if ! [ -d "a11y/bin" ]; then
  deactivate 2>/dev/null;
    virtualenv a11y
  . a11y/bin/activate
  pip3 install ansible

else
  echo Skipping Ansible install
  . a11y/bin/activate

fi

ansible-playbook -i localhost, -c local ansible/ansible-task-install-packages.yml