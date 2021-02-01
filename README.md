# TFR-Checker
A python code that periodically checks the FAA's TFR Website so SpaceX don't have to manually check the page every 20 minutes on Starship launch days
You need to install win10toast for windows notifications to work, otherwise simply remove all lines related to this and you'll still receive a print to console for changes
to start type check([],[]) into the console. This will output a list of all currently active TFR's (it will suppress windows Notifications for this first call). From then on the code will check every 15 min, and if there is a change it will output this to the console and ping a windows notification.
