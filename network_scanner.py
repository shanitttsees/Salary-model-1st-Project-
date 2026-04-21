"""
Network Vulnerability Scanner Module
Scans the local network for vulnerabilities and security issues.
"""

import socket
import subprocess
import platform
import ipaddress
import threading
from typing import List, Dict, Optional
from datetime import datetime
import json


class NetworkScanner:
    """Scans network for devices and vulnerabilities."""
    
    COMMON_PORTS = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'SMB',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        5984: 'CouchDB',
        6379: 'Redis',
        8080: 'HTTP-Alt',
        8443: 'HTTPS-Alt',
        27017: 'MongoDB',
    }
    
    VULNERABILITY_RULES = {
        'telnet': {'port': 23, 'severity': 'HIGH', 'description': 'Telnet is unencrypted and vulnerable to MITM attacks'},
        'ftp': {'port': 21, 'severity': 'HIGH', 'description': 'FTP sends credentials in plain text'},
        'http': {'port': 80, 'severity': 'MEDIUM', 'description': 'HTTP traffic is not encrypted'},
        'smb': {'port': 445, 'severity': 'HIGH', 'description': 'SMB exposed to network - risk of ransomware'},
        'ssh_weak': {'port': 22, 'severity': 'MEDIUM', 'description': 'SSH exposed - ensure strong authentication'},
        'mysql_exposed': {'port': 3306, 'severity': 'CRITICAL', 'description': 'MySQL exposed to network'},
        'mongodb_exposed': {'port': 27017, 'severity': 'CRITICAL', 'description': 'MongoDB exposed to network'},
        'redis_exposed': {'port': 6379, 'severity': 'CRITICAL', 'description': 'Redis exposed - no authentication'},
    }
    
    def __init__(self, network_range: Optional[str] = None):
        """
        Initialize the scanner.
        
        Args:
            network_range: Network range to scan (e.g., '192.168.1.0/24')
        """
        self.network_range = network_range or self._get_local_network()
        self.devices_found = []
        self.vulnerabilities = []
        self.scan_results = {}
        self.lock = threading.Lock()
        
    def _get_local_network(self) -> str:
        """Detect the local network range."""
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            # Convert to /24 network
            parts = ip.split('.')
            return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        except Exception as e:
            print(f"Error detecting network: {e}")
            return "192.168.1.0/24"
    
    def get_network_info(self) -> Dict:
        """Get current network information."""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            return {
                'hostname': hostname,
                'local_ip': local_ip,
                'network_range': self.network_range,
                'scan_time': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def scan_host(self, host: str, ports: Optional[List[int]] = None) -> Dict:
        """
        Scan a single host for open ports.
        
        Args:
            host: IP address to scan
            ports: List of ports to scan (default: common ports)
            
        Returns:
            Dictionary with scan results
        """
        if ports is None:
            ports = list(self.COMMON_PORTS.keys())
        
        results = {
            'host': host,
            'open_ports': [],
            'services': []
        }
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                
                result = sock.connect_ex((host, port))
                
                if result == 0:
                    service = self.COMMON_PORTS.get(port, 'Unknown')
                    results['open_ports'].append(port)
                    results['services'].append(service)
                    
                sock.close()
            except socket.gaierror:
                pass
            except socket.error:
                pass
        
        return results
    
    def check_host_alive(self, host: str) -> bool:
        """
        Check if a host is alive using ping.
        
        Args:
            host: IP address to ping
            
        Returns:
            True if host responds, False otherwise
        """
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '1', host]
            result = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, Exception):
            return False
    
    def scan_network(self) -> List[Dict]:
        """
        Scan the entire network for active hosts.
        
        Returns:
            List of active hosts with their open ports
        """
        try:
            network = ipaddress.ip_network(self.network_range, strict=False)
            print(f"Scanning network: {self.network_range}")
            
            threads = []
            for host in network.hosts():
                host_str = str(host)
                thread = threading.Thread(
                    target=self._scan_host_thread,
                    args=(host_str,)
                )
                thread.daemon = True
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join(timeout=10)
            
            print(f"Found {len(self.devices_found)} active device(s)")
            return self.devices_found
            
        except Exception as e:
            print(f"Error scanning network: {e}")
            return []
    
    def _scan_host_thread(self, host: str):
        """Helper method for threaded host scanning."""
        if self.check_host_alive(host):
            results = self.scan_host(host)
            
            if results['open_ports']:
                with self.lock:
                    self.devices_found.append(results)
                    self.scan_results[host] = results
    
    def identify_vulnerabilities(self) -> List[Dict]:
        """
        Identify vulnerabilities based on open ports.
        
        Returns:
            List of identified vulnerabilities
        """
        vulnerabilities = []
        
        for host, results in self.scan_results.items():
            for port in results['open_ports']:
                for vuln_name, vuln_info in self.VULNERABILITY_RULES.items():
                    if vuln_info['port'] == port:
                        vulnerability = {
                            'host': host,
                            'port': port,
                            'service': self.COMMON_PORTS.get(port, 'Unknown'),
                            'vulnerability': vuln_name,
                            'severity': vuln_info['severity'],
                            'description': vuln_info['description'],
                            'timestamp': datetime.now().isoformat()
                        }
                        vulnerabilities.append(vulnerability)
        
        self.vulnerabilities = vulnerabilities
        return vulnerabilities
    
    def get_severity_summary(self) -> Dict:
        """Get summary of vulnerabilities by severity."""
        summary = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
        
        for vuln in self.vulnerabilities:
            severity = vuln.get('severity', 'LOW')
            if severity in summary:
                summary[severity] += 1
        
        return summary
    
    def get_remediation_advice(self) -> List[Dict]:
        """Get remediation advice for found vulnerabilities."""
        advice = []
        
        remediation_map = {
            'telnet': 'Disable Telnet and use SSH instead',
            'ftp': 'Use SFTP or SCP for secure file transfer',
            'http': 'Enable HTTPS/TLS encryption',
            'smb': 'Restrict SMB access with firewall rules',
            'ssh_weak': 'Use key-based authentication and strong algorithms',
            'mysql_exposed': 'Bind MySQL to localhost only or use VPN',
            'mongodb_exposed': 'Enable authentication and network restrictions',
            'redis_exposed': 'Use Redis with authentication and firewall rules',
        }
        
        for vuln in self.vulnerabilities:
            remediation = {
                'vulnerability': vuln['vulnerability'],
                'host': vuln['host'],
                'port': vuln['port'],
                'recommendation': remediation_map.get(
                    vuln['vulnerability'],
                    'Restrict access to this port'
                )
            }
            advice.append(remediation)
        
        return advice
    
    def export_results(self, format_type: str = 'json') -> str:
        """
        Export scan results.
        
        Args:
            format_type: 'json' or 'dict'
            
        Returns:
            Results in requested format
        """
        results = {
            'network_info': self.get_network_info(),
            'devices_found': self.devices_found,
            'vulnerabilities': self.vulnerabilities,
            'severity_summary': self.get_severity_summary(),
            'remediation_advice': self.get_remediation_advice()
        }
        
        if format_type == 'json':
            return json.dumps(results, indent=2)
        else:
            return results
