# TFR-Checker
A python code that periodically checks the FAA's TFR Website so SpaceX don't have to manually check the page every 20 minutes on Starship launch days
You need to install win10toast (type pip install win10toast into the console)for windows notifications to work, otherwise simply remove all lines related to this and you'll still receive a print to console for changes
to start type check(['0'],['0']) into the console. This will output a list of all currently active TFR's (it will suppress windows Notifications for this first call). If you don't want the list to be output on first call you can instead use the call check(get_current_Tfrs[0], get_current_Tfrs[1]). From then on the code will check every 15 min, and if there is a change it will output this to the console and ping a windows notification.


TL;DR: Copy paste this into the console

first time start:

pip install win10toast
check(['0']['0'])

later starts:

check(['0'],['0'])
