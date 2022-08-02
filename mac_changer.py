#!/usr/bin/env python
import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="new_mac_addr", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        #handling err
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac_addr:
        #handling err
        parser.error("[-] Please specify a new mac address, use --help for more info")
    return options


def change_mac(interface, new_mac_addr):
    print("[+] changing mac address for " + interface + " to new mac address " + new_mac_addr)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_addr])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
    mac_addr_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_addr_search_result:
        return mac_addr_search_result.group(0)
    else:
        print("[-] Could not read MAC address")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current Mac = " + str(current_mac))
change_mac(options.interface, options.new_mac_addr)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac_addr:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed")