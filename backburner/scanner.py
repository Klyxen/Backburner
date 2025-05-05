import asyncio
import socket
import random
import time
import json
from typing import List, Optional, Tuple
from asyncio import Semaphore
from contextlib import closing
from .config import BackburnerConfig
from .utils import print_message, parse_target, is_valid_target
from colorama import Fore

# Randomized user-agents for stealth scans
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "curl/7.68.0",
]

async def resolve_ip(target: str) -> Optional[str]:
    """Resolve a domain or IP to an IP address."""
    try:
        ip = socket.gethostbyname(target)
        print_message(f"[+] Resolved {target} to {ip}", Fore.LIGHTCYAN_EX)
        return ip
    except socket.gaierror:
        print_message(f"[!] Cannot resolve {target}: invalid or unreachable hostname", Fore.LIGHTRED_EX)
        return None

async def grab_banner(ip: str, port: int, timeout: float = 1.5) -> Optional[str]:
    """Attempt to grab a service banner from an open port."""
    try:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(timeout)
            await asyncio.get_event_loop().run_in_executor(
                None, lambda: sock.connect((ip, port))
            )
            # Service-specific probes
            if port in [80, 443, 8080, 8443]:
                user_agent = random.choice(USER_AGENTS)  # Randomized user-agent
                request = f"GET / HTTP/1.1\r\nHost: localhost\r\nUser-Agent: {user_agent}\r\n\r\n"
                sock.send(request.encode())
            elif port == 22:  # SSH
                pass  # SSH sends banner automatically
            elif port == 53:  # DNS
                sock.send(b"\x00\xfc\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01")
            banner = await asyncio.get_event_loop().run_in_executor(
                None, lambda: sock.recv(1024).decode('utf-8', errors='ignore').strip()
            )
            return banner[:100] if banner else None
    except (socket.error, UnicodeDecodeError):
        return None

async def scan_port(
    ip: str,
    port: int,
    service: str,
    is_high_risk: bool,
    open_ports: List[Tuple[int, str, Optional[str]]],
    semaphore: Semaphore,
    config: BackburnerConfig
) -> None:
    """Scan a single port and attempt banner grabbing if open."""
    async with semaphore:
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.settimeout(config.TIMEOUT)
                result = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: sock.connect_ex((ip, port))
                )
                if result == 0:  # Port is open
                    banner = await grab_banner(ip, port, config.TIMEOUT)
                    banner_info = f" - {banner}" if banner else ""
                    severity = Fore.LIGHTRED_EX if is_high_risk else Fore.LIGHTGREEN_EX
                    label = "HIGHLY vulnerable" if is_high_risk else "potentially vulnerable"
                    print_message(f"[+] Port {port} ({service}) is open - {label}{banner_info}", severity)
                    open_ports.append({"port": port, "service": service, "banner": banner})
                else:
                    # Random delay for stealth
                    time.sleep(random.uniform(0.1, 0.5))
        except socket.error:
            pass  # Silently skip failed scans

async def scan_target_ports(target: str, config: BackburnerConfig) -> List[dict]:
    """Scan all configured ports for the target."""
    open_ports: List[dict] = []
    semaphore = Semaphore(config.CONCURRENCY_LIMIT)
    ports = config.PORTS
    total_ports = len(ports)

    # Validate and resolve the target
    try:
        hostname = parse_target(target)
        if not is_valid_target(hostname):
            print_message(f"[!] Invalid target: {hostname} is not a valid domain or IP", Fore.LIGHTRED_EX)
            return open_ports
    except ValueError as e:
        print_message(f"[!] Invalid target: {e}", Fore.LIGHTRED_EX)
        return open_ports

    ip = await resolve_ip(hostname)
    if not ip:
        return open_ports

    print_message(f"[*] Scanning {total_ports} ports for {ip} in {'stealth' if config.STEALTH_MODE else 'normal'} mode", Fore.LIGHTBLUE_EX)

    # Create tasks for scanning ports
    tasks = [
        scan_port(ip, port, service, is_high_risk, open_ports, semaphore, config)
        for port, service, is_high_risk in ports
    ]

    # Progress feedback
    for i in range(0, len(tasks), config.CONCURRENCY_LIMIT):
        await asyncio.gather(*tasks[i:i + config.CONCURRENCY_LIMIT])
        print_message(f"[*] Scanned {min(i + config.CONCURRENCY_LIMIT, total_ports)}/{total_ports} ports", Fore.LIGHTBLUE_EX)

    if not open_ports:
        print_message("[!] No open ports found", Fore.LIGHTYELLOW_EX)

    # Organized JSON output
    if config.VERBOSE_OUTPUT:
        print_message(json.dumps(open_ports, indent=4), Fore.LIGHTCYAN_EX)

    return open_ports

if __name__ == "__main__":
    # Example usage for standalone testing
    import sys
    from .config import BackburnerConfig

    async def main():
        if len(sys.argv) < 2:
            print_message("[!] Usage: python scanner.py <target>", Fore.LIGHTRED_EX)
            return

        target = sys.argv[1]
        config = BackburnerConfig(
            TIMEOUT=2.0,
            CONCURRENCY_LIMIT=50,
            PORTS=[(80, "HTTP", False), (443, "HTTPS", False), (22, "SSH", True)],
            STEALTH_MODE=True,
            VERBOSE_OUTPUT=True,
        )
        results = await scan_target_ports(target, config)
        print_message(f"[*] Scan complete. Found {len(results)} open ports.", Fore.LIGHTGREEN_EX)

    asyncio.run(main())
