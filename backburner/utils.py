import re
import csv
import logging
from typing import List, Optional, Tuple
from urllib.parse import urlparse
from colorama import Fore, Style, init
import ipaddress
import os
from concurrent.futures import ThreadPoolExecutor

# Initialize colorama for colored console output
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BackburnerUtilsException(Exception):
    """Custom exception class for Backburner utilities."""
    pass

def print_message(message: str, color: str = Fore.LIGHTWHITE_EX) -> None:
    """Print a formatted message to the console."""
    logging.info(message)
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
        logging.error("Invalid hostname extracted.")
        raise ValueError("No valid hostname found")
    logging.debug(f"Parsed hostname: {hostname}")
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
        logging.debug("Target matches domain pattern.")
        return True
    if re.match(ip_pattern, target):
        try:
            ip = ipaddress.ip_address(target)
            is_valid = not ip.is_private and not ip.is_loopback and not ip.is_reserved
            logging.debug(f"IP validation result for {target}: {is_valid}")
            return is_valid
        except ValueError:
            logging.error(f"Invalid IP address: {target}")
            return False
    logging.warning(f"Target does not match any known patterns: {target}")
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

    def write_to_file():
        try:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Port", "Service", "Banner"])
                writer.writerows(results)
            print_message(f"[+] Results saved to {filename}", Fore.LIGHTCYAN_EX)
        except IOError as e:
            logging.exception("Failed to save results.")
            print_message(f"[!] Failed to save results: {e}", Fore.LIGHTRED_EX)

    # Save using threading for scalability
    with ThreadPoolExecutor() as executor:
        executor.submit(write_to_file)

def load_results(filename: str) -> List[Tuple[int, str, Optional[str]]]:
    """
    Load scan results from a CSV file.

    Args:
        filename (str): The name of the file to load the results from.

    Returns:
        List[Tuple[int, str, Optional[str]]]: The loaded scan results.
    """
    if not os.path.exists(filename):
        logging.error(f"File not found: {filename}")
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
        logging.exception("Failed to load results.")
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
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    logging.debug(f"Sanitized filename: {sanitized}")
    return sanitized

if __name__ == "__main__":
    # Example for testing
    try:
        print_message("Starting Backburner utilities...", Fore.LIGHTGREEN_EX)
        result = parse_target("https://example.com")
        print_message(f"Parsed target: {result}", Fore.LIGHTBLUE_EX)
    except BackburnerUtilsException as e:
        logging.error(e)
