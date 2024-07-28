import paramiko
import csv
import os

# Branch IPs
branches = [
    "0.0.0.0" # List redacted for privacy
]

# HQ IP
hq = ["0.0.0.0"]  # Redacted for privacy

# Prompt user for firewall username and password
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")


# Log into each firewall in a list, get ARP table IPs, write to CSV file
def arp_to_csv(ip_list, filename):
    # All ARP table IPs go in this list
    arp_list = []

    # Command to run on each firewall
    command = "get system arp"

    # Iterate through each IP in IP list
    for ip in ip_list:
        print(f"Getting ARP table entries for {ip}...")

        # Connect to firewall and login
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)

        # Execute a command and convert to easier to read text
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        lines = output.split('\n')
        # print(lines)  # See what the output of the command is

        # Iterate through each line of the output
        for line in lines:
            # Check to see if the line contains a dot (for IP), ignore warning lines and all other lines
            if "." in line and "drive" not in line and "proceeding" not in line and "hour" not in line:
                arp_entry = line.split()[0]  # Only extract the IP address from the line
                arp_list.append(arp_entry)  # Append IP address to the list above

        ssh.close()  # Close the connection
        print("Success!")

    #  Write the list to CSV file
    with open(filename, "w") as file:
        write = csv.writer(file, delimiter="\n")
        write.writerow(arp_list)


arp_to_csv(branches, "Branches.csv")
arp_to_csv(hq, "HQ.csv")
