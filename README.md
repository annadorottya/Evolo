# Evolo

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus urna nulla, molestie ut orci a, tempor venenatis lacus. In tortor sem, vehicula quis facilisis a, consectetur non risus. Vivamus massa magna, rutrum at ultricies hendrerit, tincidunt ac enim.

# Features to implement
1. Write the summary of the project above
2. Implement the php part of the web interface - save config to a text file
3. List the nearby drones for adding them to whitelist on the webinterface (write a python script which lists the drones, and then call it from php)
4. Implement readConfig() in evolo.py - read the config file and return the whitelist of drones (string array of MAC addresses) and other config data (not used yet)
5. Solve the issue of global variables in main.py. `underattack[]` and `attackInProgress` should be shared among processes, but the simple `global` declaration does not work.
6. Implement `warn` to sendSpoofedParrotPacket() in evolo.py - not just stop the drone but slowly rotate it.
