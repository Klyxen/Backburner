from typing import List, Tuple

class BackburnerConfig:
    """Configuration for the Backburner port scanner."""
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
    TIMEOUT: float = 1.5          # Socket timeout in seconds
    CONCURRENCY_LIMIT: int = 50   # Max concurrent port scans
