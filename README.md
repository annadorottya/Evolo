# Evolo

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus urna nulla, molestie ut orci a, tempor venenatis lacus. In tortor sem, vehicula quis facilisis a, consectetur non risus. Vivamus massa magna, rutrum at ultricies hendrerit, tincidunt ac enim.

# Features to implement
1. Write the summary of the project above
2. Implement the php part of the web interface - save config to a text file
3. List the nearby drones for adding them to whitelist on the webinterface (call the python script `listDrones.py` from php and read the response (check the sampleResponse_listDrones.txt file))
4. Implement readConfig() in evolo.py - read the config file and return the whitelist of drones (string array of MAC addresses) and other config data (not used yet)
5. Implement the usage of the config variables
6. Solve the issue of global variables in main.py. `underattack[]` and `attackInProgress` should be shared among processes, but the simple `global` declaration does not work.

# Good to know
Start ftp daemon on Raspberry: `python -m pyftpdlib -w`
Always run evolo as root! (Otherwise it can not connect to wifi networks)
