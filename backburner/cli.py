import asyncio
import argparse
from .config import BackburnerConfig
from .scanner import scan_target_ports
from .utils import print_message, save_results
from colorama import Fore

def display_banner() -> None:
    """Display the Backburner banner."""
    banner = """
    ╔════════════════════════════╗
          BACKBURNER v2.0
    ╚════════════════════════════╝
    """
    print_message(Fore.LIGHTRED_EX + Style.BRIGHT + banner + Style.RESET_ALL)

async def run_scanner(args: argparse.Namespace) -> None:
    """Run the Backburner port scanner."""
    display_banner()
    config = BackburnerConfig()
    config.TIMEOUT = args.timeout
    config.CONCURRENCY_LIMIT = args.concurrency

    if args.target:
        # CLI mode: scan single target
        open_ports = await scan_target_ports(args.target, config)
        if open_ports and args.output:
            save_results(open_ports, args.output)
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
                if open_ports and args.output:
                    save_results(open_ports, args.output)
            except KeyboardInterrupt:
                print_message("[!] Scan interrupted", Fore.LIGHTRED_EX)
                break
            except Exception as e:
                print_message(f"[!] Unexpected error: {e}", Fore.LIGHTRED_EX)

def main() -> None:
    """Parse arguments and run the scanner."""
    parser = argparse.ArgumentParser(description="Backburner Port Scanner v2.0")
    parser.add_argument("target", nargs="?", help="Target domain or IP (optional for interactive mode)")
    parser.add_argument("--timeout", type=float, default=1.5, help="Socket timeout in seconds")
    parser.add_argument("--concurrency", type=int, default=50, help="Concurrency limit for port scans")
    parser.add_argument("--output", type=str, help="Output file for scan results (CSV format)")
    args = parser.parse_args()

    asyncio.run(run_scanner(args))

if __name__ == "__main__":
    main()
