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

    Args:
        target (str): The target string (URL, domain, or IP).

    Returns:
        str: The extracted hostname or IP.

    Raises:
        ValueError: If no valid hostname or IP is found.
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

    Args:
        target (str): The target string (domain or IP).

    Returns:
        bool: True if the target is valid, False otherwise.
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
    """
    Save scan results to a CSV file if results exist.

    Args:
        results (List[Tuple[int, str, Optional[str]]]): The scan results to save.
        filename (str): The name of the file to save the results to.

    Returns:
        None
    """
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

def load_results(filename: str) -> List[Tuple[int, str, Optional[str]]]:
    """
    Load scan results from a CSV file.

    Args:
        filename (str): The name of the file to load the results from.

    Returns:
        List[Tuple[int, str, Optional[str]]]: The loaded scan results.
    """
    if not os.path.exists(filename):
        print_message(f"[!] File not found: {filename}", Fore.LIGHTRED_EX)
        return []

    try:
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            results = [(int(row[0]), row[1], row[2] if len(row) > 2 else None) for row in reader]
        print_message(f"[+] Results loaded from {filename}", Fore.LIGHTCYAN_EX)
        return results
    except IOError as e:
        print_message(f"[!] Failed to load results: {e}", Fore.LIGHTRED_EX)
        return []

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to remove invalid characters.

    Args:
        filename (str): The original filename.

    Returns:
        str: The sanitized filename.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)
