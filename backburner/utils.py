import re
import csv
from typing import List, Optional, Tuple
from urllib.parse import urlparse
from colorama import Fore, Style, init
import ipaddress
import os

# Initialize colorama for colored console output
init(autoreset=True)

def print_message(message: str, color: str = Fore.LIGHTWHITE_EX) -> None:
    """Print a formatted message to the console."""
    print(f"{color}{message}{Style.RESET_ALL}")

def parse_target(target: str) -> str:
    """
    Extract hostname or IP from a URL, domain, or IP.
    """
    target = target.strip()
    parsed = urlparse(target if target.startswith(('http://', 'https://')) else f'http://{target}')
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("No valid hostname found")
    return hostname

def is_valid_target(target: str) -> bool:
    """
    Check if the target is a valid domain or IP, excluding reserved/private IPs.
    """
    domain_pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    
    if re.match(domain_pattern, target):
        return True
    if re.match(ip_pattern, target):
        try:
            ip = ipaddress.ip_address(target)
            return not ip.is_private and not ip.is_loopback and not ip.is_reserved
        except ValueError:
            return False
    return False

def save_results(results: List[Tuple[int, str, Optional[str]]], filename: str) -> None:
    """Save scan results to a CSV file."""
    if not results:
        print_message("[!] No open ports to save", Fore.LIGHTYELLOW_EX)
        return

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    try:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Port", "Service", "Banner"])
            writer.writerows(results)
        print_message(f"[+] Results saved to {filename}", Fore.LIGHTCYAN_EX)
    except IOError as e:
        print_message(f"[!] Failed to save results: {e}", Fore.LIGHTRED_EX)
