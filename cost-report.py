#!/usr/bin/env python
import json
import locale
import datetime 
import subprocess
from calendar import monthrange
from dateutil import relativedelta

class bcolors:
    CYAN = '\033[96m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

months = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}

yr = int; mon1 =int; date = int; mon = str;
print("Press 1 for current month Bill or Press 2 for specific mon/yr: "); 
i = str(input())
if i == '1':
    yr = datetime.now().year
    mon1 = datetime.now().month
elif i == '2':
    yr = int(input("Enter the year in YYYY format:"))
    mon1 = int(input("Enter the month in MM format:")) 	#specify month b/w 01-12
else:
    print("Invalid Selection. Please enter either 1 or 2")

dates = monthrange(yr, mon1)[1]
mon = "{:02d}".format(mon1)

end = "{}-{}-{}".format(yr, mon, str(dates))
end1 = datetime.datetime.strptime(end, '%Y-%m-%d')  #convert string to datetime
end2 = end1 + datetime.timedelta(days = 1) 		#add 1 day 
End_date = str(end2).split(" ",1)			#convert date to string then split date & time

cmd = 'aws ce get-cost-and-usage --time-period Start={}-{}-01,End={} --granularity MONTHLY --metrics "BlendedCost"'.format(yr, mon, End_date[0])
# aws ce get-cost-and-usage --time-period Start=2020-12-01,End=2020-12-31 --granularity MONTHLY --metrics "BlendedCost" "UnblendedCost" "UsageQuantity"

try:
    output = subprocess.check_output(cmd.format(yr,mon, yr, mon), shell=True)
    output = output.decode('utf-8')
    output = json.loads(output)
    amount = output['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
    amount = float(amount)
    locale.setlocale(locale.LC_ALL,'en_US')
    locale.setlocale(locale.LC_MONETARY, 'en_US')
    price = locale.currency(amount, grouping= True)
    print("AWS Cost for "+str(yr)+" "+months[mon]+" Month :", bcolors.CYAN+price+bcolors.ENDC)
except Exception as e:
    print(bcolors.WARNING+"unable to provide AWS cost and usage."+bcolors.ENDC)
    print(e)
