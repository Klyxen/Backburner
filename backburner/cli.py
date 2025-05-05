import asyncio
import argparse
import os
from .config import BackburnerConfig
from .scanner import scan_target_ports
from .utils import print_message, save_results
from colorama import Fore, Style

def clear_terminal() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner() -> None:
    """Display the Backburner banner."""
    banner = """
    ╔════════════════════════════╗
          BACKBURNER v3.0
    ╚════════════════════════════╝
    """
    print_message(Fore.LIGHTRED_EX + Style.BRIGHT + banner + Style.RESET_ALL)

def format_port_output(port: int, status: str, service: str, banner: str = None) -> str:
    """Format the port output."""
    return f"[ {status} ] : {port} | {service}" + (f" | Banner: {banner}" if banner else "")

async def run_scanner(args: argparse.Namespace) -> None:
    """Run the Backburner port scanner."""
    clear_terminal()
    display_banner()
    config = BackburnerConfig()
    config.TIMEOUT = args.timeout
    config.CONCURRENCY_LIMIT = args.concurrency
    config.STEALTH_MODE = args.stealth

    def display_results(open_ports, target):
        """Display scan results in the desired format."""
        print_message(f"Scan results for {target}:", Fore.LIGHTCYAN_EX)
        for port, service, banner in open_ports:
            status = "open"
            print(format_port_output(port, status, service, banner))
        print_message(f"[+] Scan completed for {target}", Fore.LIGHTGREEN_EX)

    if args.target:
        # CLI mode: scan a single target
        try:
            open_ports = await scan_target_ports(args.target, config)
            display_results(open_ports, args.target)
            if args.output:
                save_results(open_ports, args.output)
                print_message(f"[+] Results saved to {args.output}", Fore.LIGHTCYAN_EX)
        except Exception as e:
            print_message(f"[!] Error scanning target {args.target}: {e}", Fore.LIGHTRED_EX)
    else:
        # Interactive mode: loop for multiple targets
        while True:
            try:
                print(f"{Fore.LIGHTCYAN_EX}Enter target (domain or IP, or 'q' to quit): ", end="")
                target = input().strip()
                if target.lower() == 'q':
                    print_message("[+] Exiting Backburner", Fore.LIGHTCYAN_EX)
                    break
                if not target:
                    print_message("[!] Target cannot be empty", Fore.LIGHTRED_EX)
                    continue

                open_ports = await scan_target_ports(target, config)
                display_results(open_ports, target)
                print(f"{Fore.LIGHTCYAN_EX}Enter output file to save results (or press Enter to skip): ", end="")
                output_file = input().strip()
                if output_file:
                    save_results(open_ports, output_file)
                    print_message(f"[+] Results saved to {output_file}", Fore.LIGHTCYAN_EX)
            except KeyboardInterrupt:
                print_message("\n[!] Scan interrupted by user", Fore.LIGHTRED_EX)
                break
            except Exception as e:
                print_message(f"[!] Unexpected error: {e}", Fore.LIGHTRED_EX)

def main() -> None:
    """Parse arguments and run the scanner."""
    parser = argparse.ArgumentParser(description="Backburner Port Scanner v3.0")
    parser.add_argument("target", nargs="?", help="Target domain or IP (optional for interactive mode)")
    parser.add_argument("--timeout", type=float, default=1.5, help="Socket timeout in seconds")
    parser.add_argument("--concurrency", type=int, default=50, help="Concurrency limit for port scans")
    parser.add_argument("--output", type=str, help="Output file for scan results (CSV format)")
    parser.add_argument("--stealth", action="store_true", help="Enable stealth mode for scans")
    args = parser.parse_args()

    try:
        asyncio.run(run_scanner(args))
    except KeyboardInterrupt:
        print_message("\n[!] Program interrupted by user", Fore.LIGHTRED_EX)
    except Exception as e:
        print_message(f"[!] Fatal error: {e}", Fore.LIGHTRED_EX)

if __name__ == "__main__":
    main()
