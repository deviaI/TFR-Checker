# TFR-Checker
A python code that periodically checks the FAA's TFR Website so SpaceX fans don't have to manually check the page every 20 minutes on Starship launch days. The Code also checks for changes to spacex.com/vehicles/starship so you can be notified for changes to flight profile or NET (no earlier than) Date
You need to install win10toast (type pip install win10toast into the console)for windows notifications to work, otherwise simply remove all lines related to this and you'll still receive a print to console for changes
to start type checkTFR() into the console. If you haven't used the code previously it will output to console all currently active TFRs in Texas related to Space operations. If you have used it previously it will output to console changes since the last time the code ran. 
From then on it will check every however many seconds and output changes to console and ping a windows notification.

