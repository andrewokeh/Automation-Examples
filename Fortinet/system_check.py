import os
import paramiko


def main() -> None:
    print("*** Must be on VPN! ***")
    ip = input("Interface IP: ").strip()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    commands = [
        "get system performance status",
        "get router info routing-table all",
        "show system interface wan1",
        "show system interface wan2",
        f"execute ping-options source {ip}\n"
        "execute ping-options repeat-count 100\n"
        "execute ping 8.8.8.8",
        "get hardware nic wan1",
        "get hardware nic wan2"
    ]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=username, password=password)

    for command in commands:
        if "ping" in command:
            print("Pinging, please wait...")

        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        lines = output.split('\n')
        for line in lines:
            print(f"{line}")

    ssh.close()


if __name__ == "__main__":
    main()
