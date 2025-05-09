from typing import List, Tuple

class BackburnerConfig:
    """Configuration for the Backburner port scanner."""

    # List of scanning modes
    MODES = ["Ghost scan", "Stealth scan", "Normal scan"]

    # List of ports to scan: (port number, service name, high risk flag)
    PORTS: List[Tuple[int, str, bool]] = [
        # Web and Proxy Services (common, often secure)
        (80, "HTTP", False), (443, "HTTPS", False), (8080, "HTTP-Proxy", False),
        (8443, "HTTPS-Proxy", False), (8000, "HTTP-Alt", False), (8008, "HTTP-Alt", False),
        (8081, "HTTP-Alt", False), (8088, "HTTP-Alt", False), (8090, "HTTP-Alt", False),
        (8888, "HTTP-Alt", False), (9000, "Admin-Panel", False), (9999, "Admin-Custom", False),

        # File and Transfer Services
        (20, "FTP-Data", True), (21, "FTP", True), (69, "TFTP", True), (2049, "NFS", True),
        (873, "rsync", True),

        # Remote Access
        (22, "SSH", False), (23, "Telnet", True), (3389, "RDP", True), (5900, "VNC", True),
        (2222, "DirectAdmin", True), (5632, "PCAnywhere", True), (1723, "PPTP", True),

        # Mail Services
        (25, "SMTP", True), (110, "POP3", True), (143, "IMAP", True), (465, "SMTPS", True),
        (587, "SMTP-Submission", True), (993, "IMAPS", True), (995, "POP3S", True),

        # Windows and Networking
        (135, "RPC", True), (137, "NetBIOS-NS", True), (138, "NetBIOS-DGM", True),
        (139, "NetBIOS-SSN", True), (445, "SMB", True),

        # Database Services
        (1433, "MSSQL", True), (1521, "Oracle-DB", True), (3306, "MySQL", True),
        (5432, "PostgreSQL", True), (5984, "CouchDB", True), (5986, "CouchDB-HTTPS", True),
        (6379, "Redis", True), (9042, "Cassandra", True), (9160, "Cassandra-Thrift", True),
        (11211, "Memcached", True), (27017, "MongoDB", True),

        # Monitoring and IoT
        (161, "SNMP", True), (162, "SNMP-Trap", True), (1883, "MQTT", True),
        (502, "Modbus", True), (47808, "BACnet", True), (7547, "TR-069", True),
        (5060, "SIP", True),

        # Directory and Authentication
        (389, "LDAP", True), (2181, "Zookeeper", True),

        # Container and DevOps
        (2375, "Docker", True), (9200, "Elasticsearch", True), (9300, "Elasticsearch-Transport", True),
        (4848, "GlassFish", True), (5672, "RabbitMQ", True),

        # Legacy and Potentially Malicious
        (512, "rexec", True), (513, "rlogin", True), (514, "rsh", True),
        (12345, "NetBus", True), (27015, "Steam", True), (10000, "Webmin", True),
        (54321, "Custom", True)
    ]

    # Default configuration values
    TIMEOUT: float = 1.5          # Socket timeout in seconds
    CONCURRENCY_LIMIT: int = 50   # Max concurrent port scans
    CURRENT_MODE: int = 2         # Default mode is "Normal scan"

    def set_mode(self, mode: int) -> None:
        """Set the scanning mode."""
        if 0 <= mode < len(self.MODES):
            self.CURRENT_MODE = mode
            self.adjust_settings_based_on_mode()

    def get_current_mode(self) -> str:
        """Get the current scanning mode as a string."""
        return self.MODES[self.CURRENT_MODE]

    def adjust_settings_based_on_mode(self) -> None:
        """Adjust configuration settings based on the selected mode."""
        if self.CURRENT_MODE == 0:  # Ghost scan
            self.TIMEOUT = 3.0
            self.CONCURRENCY_LIMIT = 20
        elif self.CURRENT_MODE == 1:  # Stealth scan
            self.TIMEOUT = 2.0
            self.CONCURRENCY_LIMIT = 35
        elif self.CURRENT_MODE == 2:  # Normal scan
            self.TIMEOUT = 1.5
            self.CONCURRENCY_LIMIT = 50

    @classmethod
    def get_ports(cls, high_risk_only: bool = False) -> List[Tuple[int, str]]:
        """
        Retrieve a list of ports to scan.

        Args:
            high_risk_only (bool): If True, only return high-risk ports.

        Returns:
            List[Tuple[int, str]]: A list of (port, service) tuples.
        """
        if high_risk_only:
            return [(port, service) for port, service, high_risk in cls.PORTS if high_risk]
        return [(port, service) for port, service, _ in cls.PORTS]

    @classmethod
    def get_port_details(cls, port: int) -> Tuple[str, bool]:
        """
        Retrieve details for a specific port.

        Args:
            port (int): The port number to look up.

        Returns:
            Tuple[str, bool]: A tuple containing the service name and high-risk flag.
        """
        for p, service, high_risk in cls.PORTS:
            if p == port:
                return service, high_risk
        return "Unknown", False
