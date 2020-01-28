# install and run.sh
if ! [ -d "a11y/bin" ]; then
  deactivate 2>/dev/null;
    virtualenv a11y
  . a11y/bin/activate
  pip3 install ansible


else
  
  . a11y/bin/activate
  export NVM_DIR="ansible/.nvm";
        source $NVM_DIR/nvm.sh;
        nvm use --delete-prefix default;
pip3 install pandas
pip3 install bokeh
pip3 install panel

WEBSITE="https://www.isomer.sg" node trial => jug.csv
#node trial => jug.csv
python CSVMerge.py

fi