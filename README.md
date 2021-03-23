 TFR-Checker
A python code that periodically checks the FAA's TFR Website so SpaceX don't have to manually check the page every 20 minutes on Starship launch days
The Code also checks for changes to spacex.com/vehicles/starship so you can be notified for changes to flight profile or NET (no earlier than) Date, as well as www.everydayastronaut.com7when_will_sn_#x_launch. The code also includes a function to print the currently active TFR's to console
You need to install win10toast (type pip install win10toast into the console)for windows notifications to work, otherwise simply remove all lines related to this and you'll still receive a print to console for changes
to start type check() into the console. This will output a list of all TFR's that have been added or removed since the programm last ran.

From then on it will check every however many seconds and output changes to console and ping a windows notification.


TL;DR: Copy paste this into the console

first time start:

pip install win10toast
check()

later starts:

check()
