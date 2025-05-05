import json
from typing import List, Tuple, Dict, Optional


class BackburnerConfig:
    """Configuration for the Backburner port scanner."""

    # Default list of ports to scan: (port number, service name, high risk flag, category)
    PORTS: List[Tuple[int, str, bool, str]] = [
        # Web and Proxy Services (common, often secure)
        (80, "HTTP", False, "Web Services"),
        (443, "HTTPS", False, "Web Services"),
        (8080, "HTTP-Proxy", False, "Web Services"),
        (8443, "HTTPS-Proxy", False, "Web Services"),
        (8000, "HTTP-Alt", False, "Web Services"),
        # File and Transfer Services
        (21, "FTP", True, "File Transfer"),
        (69, "TFTP", True, "File Transfer"),
        # Remote Access
        (22, "SSH", False, "Remote Access"),
        (23, "Telnet", True, "Remote Access"),
        # Mail Services
        (25, "SMTP", True, "Mail Services"),
        (110, "POP3", True, "Mail Services"),
        (143, "IMAP", True, "Mail Services"),
        # Database Services
        (3306, "MySQL", True, "Database Services"),
        (5432, "PostgreSQL", True, "Database Services"),
    ]

    # Default configuration values
    TIMEOUT: float = 1.5          # Socket timeout in seconds
    CONCURRENCY_LIMIT: int = 50   # Max concurrent port scans

    @classmethod
    def get_ports(cls, high_risk_only: bool = False, category: Optional[str] = None) -> List[Tuple[int, str]]:
        """
        Retrieve a list of ports to scan.

        Args:
            high_risk_only (bool): If True, only return high-risk ports.
            category (Optional[str]): Filter by category (e.g., "Web Services").

        Returns:
            List[Tuple[int, str]]: A list of (port, service) tuples.
        """
        filtered_ports = cls.PORTS
        if high_risk_only:
            filtered_ports = [p for p in filtered_ports if p[2]]
        if category:
            filtered_ports = [p for p in filtered_ports if p[3] == category]
        return [(port, service) for port, service, _, _ in filtered_ports]

    @classmethod
    def get_port_details(cls, port: int) -> Tuple[str, bool, str]:
        """
        Retrieve details for a specific port.

        Args:
            port (int): The port number to look up.

        Returns:
            Tuple[str, bool, str]: A tuple containing the service name, high-risk flag, and category.
        """
        for p, service, high_risk, category in cls.PORTS:
            if p == port:
                return service, high_risk, category
        return "Unknown", False, "Unknown"

    @classmethod
    def add_port(cls, port: int, service: str, high_risk: bool, category: str) -> bool:
        """
        Add a new port to the configuration.

        Args:
            port (int): The port number to add.
            service (str): The service name associated with the port.
            high_risk (bool): Whether the port is considered high-risk.
            category (str): The category of the port.

        Returns:
            bool: True if the port was added successfully, False if it already exists.
        """
        if any(p[0] == port for p in cls.PORTS):
            return False  # Port already exists
        cls.PORTS.append((port, service, high_risk, category))
        return True

    @classmethod
    def remove_port(cls, port: int) -> bool:
        """
        Remove a port from the configuration.

        Args:
            port (int): The port number to remove.

        Returns:
            bool: True if the port was removed successfully, False if it was not found.
        """
        for p in cls.PORTS:
            if p[0] == port:
                cls.PORTS.remove(p)
                return True
        return False

    @classmethod
    def load_ports_from_file(cls, file_path: str) -> bool:
        """
        Load ports from a JSON file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            bool: True if the ports were loaded successfully, False otherwise.
        """
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    return False
                cls.PORTS = [
                    (int(p["port"]), p["service"], p["high_risk"], p["category"])
                    for p in data
                ]
                return True
        except (IOError, ValueError, KeyError):
            return False

    @classmethod
    def save_ports_to_file(cls, file_path: str) -> bool:
        """
        Save the current port configuration to a JSON file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            bool: True if the ports were saved successfully, False otherwise.
        """
        try:
            with open(file_path, "w") as file:
                json.dump(
                    [
                        {"port": p[0], "service": p[1], "high_risk": p[2], "category": p[3]}
                        for p in cls.PORTS
                    ],
                    file,
                    indent=4,
                )
                return True
        except IOError:
            return False

    @classmethod
    def get_categories(cls) -> List[str]:
        """
        Retrieve a list of all unique categories.

        Returns:
            List[str]: A list of unique categories.
        """
        return list({p[3] for p in cls.PORTS})


if __name__ == "__main__":
    # Example usage
    print("Default Ports:", BackburnerConfig.get_ports())
    print("High-Risk Ports:", BackburnerConfig.get_ports(high_risk_only=True))
    print("Database Ports:", BackburnerConfig.get_ports(category="Database Services"))

    # Add a new port
    BackburnerConfig.add_port(8081, "Custom Service", False, "Web Services")
    print("After Adding 8081:", BackburnerConfig.get_ports())

    # Save to file
    BackburnerConfig.save_ports_to_file("ports.json")
    print("Saved ports to 'ports.json'.")

    # Load from file
    BackburnerConfig.load_ports_from_file("ports.json")
    print("Loaded Ports:", BackburnerConfig.get_ports())
