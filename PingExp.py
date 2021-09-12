import pandas as pd
import os
from prettytable import PrettyTable

ip = pd.read_csv("ip.csv")
status = []

for i in ip["IP"]:
    exit_code = os.system(f"ping {i} -n 1")
    status.append(exit_code==0)

ip["Status"] = status
ip.to_csv("ip.csv", index=False)
print(ip)


# open csv file
a = open("ip.csv", 'r')

# read the csv file
a = a.readlines()

# Seperating the Headers
l1 = a[0]
l1 = l1.split(',')

# headers for table
t = PrettyTable([l1[0], l1[1]])

# Adding the data
for i in range(1, len(a)) :
    t.add_row(a[i].split(','))

code = t.get_html_string()
html_file = open('templates/Table.html', 'w')
html_file = html_file.write(code)