import asyncio
import argparse
import os
from .config import BackburnerConfig
from .scanner import scan_target_ports
from .utils import print_message
from colorama import Fore, Style
import random
import time


def clear_terminal() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_banner() -> None:
    """Display the Backburner banner."""
    banner = """
    _--____-__---____---______----____-___-_____-____-----___`.
    ╔════════════════════════════╗
          BACKBURNER
    ╚════════════════════════════╝          `               `
    created by : Klyxen           ' '         '            '
    )(  )  ()   )    (     )(     (   )    (    )   (  (    ))
      )(   )(  (      )   (  )     ) (      )  (     )  )  ((
     (  ) (  )  )    )     ))     (  )     (    )   )  )   ))
    --__----_--___----___------____---_---_-----_----_____---`.
    """

    print_message(Fore.LIGHTRED_EX + Style.BRIGHT + banner + Style.RESET_ALL)


def format_port_output(port: int, status: str, service: str, banner: str = None) -> str:
    """Format the port output for terminal display."""
    service_color = Fore.LIGHTCYAN_EX if "HTTP" in service else Fore.LIGHTYELLOW_EX
    return (
        f"{Fore.LIGHTGREEN_EX}[ {status.upper()} ]{Style.RESET_ALL} : "
        f"{Fore.LIGHTWHITE_EX}{port}{Style.RESET_ALL} | {service_color}{service}{Style.RESET_ALL}"
        + (f" | {Fore.LIGHTMAGENTA_EX}Banner: {banner}{Style.RESET_ALL}" if banner else "")
    )


async def run_scanner(args: argparse.Namespace) -> None:
    """Run the Backburner port scanner."""
    clear_terminal()
    display_banner()
    config = BackburnerConfig()
    config.TIMEOUT = args.timeout
    config.CONCURRENCY_LIMIT = args.concurrency
    config.STEALTH_MODE = args.stealth

    def display_results(open_ports, target):
        """Display scan results in a categorized and color-coded format."""
        print_message(f"\n{Fore.LIGHTCYAN_EX}Scan results for {target}:{Style.RESET_ALL}", Fore.LIGHTCYAN_EX)
        if open_ports:
            for port, service, banner in open_ports:
                status = "open"
                print(format_port_output(port, status, service, banner))
            print_message(f"\n{Fore.LIGHTGREEN_EX}[+] Scan completed for {target}\n", Fore.LIGHTGREEN_EX)
        else:
            print_message(f"{Fore.LIGHTYELLOW_EX}[!] No open ports found for {target}\n", Fore.LIGHTYELLOW_EX)

    if args.target:
        # CLI mode: scan a single target
        try:
            open_ports = await scan_target_ports(args.target, config)
            display_results(open_ports, args.target)
        except Exception as e:
            print_message(f"{Fore.LIGHTRED_EX}[!] Error scanning target {args.target}: {e}\n", Fore.LIGHTRED_EX)
    else:
        # Interactive mode: loop for multiple targets
        while True:
            try:
                print(f"{Fore.RED}Enter Target [ domain : IP | q to quit ] : ", end="")
                target = input().strip()
                if target.lower() == 'q':
                    print_message("[+] Exiting Backburner. Goodbye!\n", Fore.LIGHTCYAN_EX)
                    break
                if not target:
                    print_message(f"{Fore.LIGHTRED_EX}[!] Target cannot be empty.\n", Fore.LIGHTRED_EX)
                    continue

                open_ports = await scan_target_ports(target, config)
                display_results(open_ports, target)
            except KeyboardInterrupt:
                print_message(f"\n{Fore.LIGHTRED_EX}[!] Scan interrupted by user.\n", Fore.LIGHTRED_EX)
                break
            except Exception as e:
                print_message(f"{Fore.LIGHTRED_EX}[!] Unexpected error: {e}\n", Fore.LIGHTRED_EX)


def main() -> None:
    """Parse arguments and run the scanner."""
    parser = argparse.ArgumentParser(description="Backburner - The Beast Port Scanner")
    parser.add_argument("target", nargs="?", help="Target domain or IP (optional for interactive mode)")
    parser.add_argument("--timeout", type=float, default=1.5, help="Socket timeout in seconds")
    parser.add_argument("--concurrency", type=int, default=50, help="Concurrency limit for port scans")
    parser.add_argument("--stealth", action="store_true", help="Enable stealth mode for scans")
    args = parser.parse_args()

    try:
        asyncio.run(run_scanner(args))
    except KeyboardInterrupt:
        print_message(f"\n{Fore.LIGHTRED_EX}[!] Program interrupted by user.\n", Fore.LIGHTRED_EX)
    except Exception as e:
        print_message(f"{Fore.LIGHTRED_EX}[!] Fatal error: {e}\n", Fore.LIGHTRED_EX)


if __name__ == "__main__":
    main()
