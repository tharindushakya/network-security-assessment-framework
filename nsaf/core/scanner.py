"""
Core networking scanner module for NSAF.
Handles port scanning, host discovery, and service detection.
"""

import socket
import threading
import ipaddress
import time
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
import platform
import json
from dataclasses import dataclass
from datetime import datetime

try:
    import nmap
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False

from ..utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class ScanResult:
    """Data class for scan results"""
    host: str
    port: int
    state: str
    service: str = ""
    version: str = ""
    banner: str = ""
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class HostInfo:
    """Data class for host information"""
    ip: str
    hostname: str = ""
    mac_address: str = ""
    os_info: str = ""
    open_ports: List[ScanResult] = None
    status: str = "unknown"

    def __post_init__(self):
        if self.open_ports is None:
            self.open_ports = []

class NetworkScanner:
    """Comprehensive network scanner with multiple scanning techniques"""
    
    def __init__(self, timeout: int = 3, max_threads: int = 100):
        """
        Initialize NetworkScanner
        
        Args:
            timeout: Socket timeout in seconds
            max_threads: Maximum number of concurrent threads
        """
        self.timeout = timeout
        self.max_threads = max_threads
        self.nm = None
        
        if NMAP_AVAILABLE:
            try:
                self.nm = nmap.PortScanner()
                logger.info("Nmap scanner initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize nmap: {e}")
        else:
            logger.warning("Nmap not available, using basic scanning only")

    def discover_hosts(self, network: str, method: str = "ping") -> List[str]:
        """
        Discover active hosts in a network
        
        Args:
            network: Network range (e.g., "192.168.1.0/24")
            method: Discovery method ("ping", "arp", "tcp_syn")
            
        Returns:
            List of active IP addresses
        """
        logger.info(f"Starting host discovery for {network} using {method}")
        
        active_hosts = []
        
        try:
            network_obj = ipaddress.ip_network(network, strict=False)
            hosts = list(network_obj.hosts())
            
            if method == "ping":
                active_hosts = self._ping_sweep(hosts)
            elif method == "arp" and platform.system().lower() == "linux":
                active_hosts = self._arp_sweep(hosts)
            elif method == "tcp_syn":
                active_hosts = self._tcp_syn_sweep(hosts)
            else:
                # Fallback to ping sweep
                active_hosts = self._ping_sweep(hosts)
                
        except Exception as e:
            logger.error(f"Host discovery failed: {e}")
            
        logger.info(f"Discovered {len(active_hosts)} active hosts")
        return active_hosts

    def _ping_sweep(self, hosts: List[ipaddress.IPv4Address]) -> List[str]:
        """Perform ping sweep to discover hosts"""
        active_hosts = []
        
        def ping_host(host):
            try:
                param = "-n" if platform.system().lower() == "windows" else "-c"
                cmd = ["ping", param, "1", "-w", "1000", str(host)]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return str(host)
            except Exception:
                pass
            return None

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(ping_host, host) for host in hosts]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    active_hosts.append(result)
                    
        return active_hosts

    def _tcp_syn_sweep(self, hosts: List[ipaddress.IPv4Address]) -> List[str]:
        """TCP SYN sweep for host discovery"""
        active_hosts = []
        common_ports = [22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
        
        def check_host(host):
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((str(host), port))
                    sock.close()
                    if result == 0:
                        return str(host)
                except Exception:
                    continue
            return None

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(check_host, host) for host in hosts]
            for future in as_completed(futures):
                result = future.result()
                if result and result not in active_hosts:
                    active_hosts.append(result)
                    
        return active_hosts

    def port_scan(self, targets: List[str], ports: str = "1-1000", 
                  scan_type: str = "tcp_connect") -> Dict[str, List[ScanResult]]:
        """
        Perform port scanning on targets
        
        Args:
            targets: List of IP addresses to scan
            ports: Port range (e.g., "1-1000", "22,80,443")
            scan_type: Type of scan ("tcp_connect", "tcp_syn", "udp")
            
        Returns:
            Dictionary mapping hosts to list of scan results
        """
        logger.info(f"Starting port scan on {len(targets)} targets")
        results = {}
        
        for target in targets:
            logger.info(f"Scanning {target}")
            if self.nm and scan_type in ["tcp_syn", "udp"]:
                results[target] = self._nmap_scan(target, ports, scan_type)
            else:
                results[target] = self._tcp_connect_scan(target, ports)
                
        return results

    def _nmap_scan(self, target: str, ports: str, scan_type: str) -> List[ScanResult]:
        """Perform nmap scan"""
        results = []
        try:
            scan_args = ""
            if scan_type == "tcp_syn":
                scan_args = "-sS"
            elif scan_type == "udp":
                scan_args = "-sU"
            
            self.nm.scan(target, ports, arguments=scan_args)
            
            if target in self.nm.all_hosts():
                for port in self.nm[target]['tcp']:
                    state = self.nm[target]['tcp'][port]['state']
                    service = self.nm[target]['tcp'][port].get('name', '')
                    version = self.nm[target]['tcp'][port].get('version', '')
                    
                    if state == 'open':
                        result = ScanResult(
                            host=target,
                            port=port,
                            state=state,
                            service=service,
                            version=version
                        )
                        results.append(result)
                        
        except Exception as e:
            logger.error(f"Nmap scan failed for {target}: {e}")
            
        return results

    def _tcp_connect_scan(self, target: str, ports: str) -> List[ScanResult]:
        """Perform TCP connect scan"""
        results = []
        port_list = self._parse_ports(ports)
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    # Try to grab banner
                    banner = ""
                    try:
                        sock.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
                        banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    except:
                        pass
                    
                    service = self._identify_service(port, banner)
                    scan_result = ScanResult(
                        host=target,
                        port=port,
                        state="open",
                        service=service,
                        banner=banner[:200]  # Limit banner length
                    )
                    sock.close()
                    return scan_result
                    
                sock.close()
            except Exception as e:
                logger.debug(f"Error scanning port {port} on {target}: {e}")
                
            return None

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(scan_port, port) for port in port_list]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                    
        return sorted(results, key=lambda x: x.port)

    def _parse_ports(self, ports: str) -> List[int]:
        """Parse port string into list of integers"""
        port_list = []
        
        for part in ports.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                port_list.extend(range(start, end + 1))
            else:
                port_list.append(int(part))
                
        return port_list

    def _identify_service(self, port: int, banner: str) -> str:
        """Identify service based on port and banner"""
        common_services = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
            53: "dns", 80: "http", 110: "pop3", 143: "imap",
            443: "https", 993: "imaps", 995: "pop3s",
            3389: "rdp", 5432: "postgresql", 3306: "mysql"
        }
        
        service = common_services.get(port, "unknown")
        
        # Enhance service detection with banner analysis
        if banner:
            banner_lower = banner.lower()
            if "http" in banner_lower:
                service = "http"
            elif "ssh" in banner_lower:
                service = "ssh"
            elif "ftp" in banner_lower:
                service = "ftp"
            elif "smtp" in banner_lower:
                service = "smtp"
                
        return service

    def get_host_info(self, target: str) -> HostInfo:
        """Get comprehensive host information"""
        logger.info(f"Gathering host information for {target}")
        
        host_info = HostInfo(ip=target)
        
        # Get hostname
        try:
            host_info.hostname = socket.gethostbyaddr(target)[0]
        except:
            pass
            
        # Perform basic port scan
        scan_results = self._tcp_connect_scan(target, "1-1000")
        host_info.open_ports = scan_results
        host_info.status = "up" if scan_results else "filtered"
        
        return host_info

    def service_detection(self, scan_results: List[ScanResult]) -> List[ScanResult]:
        """Enhanced service detection and version enumeration"""
        logger.info("Performing enhanced service detection")
        
        enhanced_results = []
        
        for result in scan_results:
            enhanced_result = result
            
            # Perform more detailed service detection
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                sock.connect((result.host, result.port))
                
                # Send service-specific probes
                if result.service in ["http", "https"]:
                    enhanced_result = self._detect_web_service(sock, result)
                elif result.service == "ssh":
                    enhanced_result = self._detect_ssh_service(sock, result)
                elif result.service == "ftp":
                    enhanced_result = self._detect_ftp_service(sock, result)
                    
                sock.close()
                
            except Exception as e:
                logger.debug(f"Service detection failed for {result.host}:{result.port}: {e}")
                
            enhanced_results.append(enhanced_result)
            
        return enhanced_results

    def _detect_web_service(self, sock: socket.socket, result: ScanResult) -> ScanResult:
        """Detect web service details"""
        try:
            request = f"GET / HTTP/1.1\r\nHost: {result.host}\r\n\r\n"
            sock.send(request.encode())
            response = sock.recv(4096).decode('utf-8', errors='ignore')
            
            # Extract server information
            lines = response.split('\n')
            for line in lines:
                if line.lower().startswith('server:'):
                    result.version = line.split(':', 1)[1].strip()
                    break
                    
        except Exception:
            pass
            
        return result

    def _detect_ssh_service(self, sock: socket.socket, result: ScanResult) -> ScanResult:
        """Detect SSH service details"""
        try:
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            if banner.startswith('SSH-'):
                result.version = banner.strip()
        except Exception:
            pass
            
        return result

    def _detect_ftp_service(self, sock: socket.socket, result: ScanResult) -> ScanResult:
        """Detect FTP service details"""
        try:
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            if '220' in banner:
                result.banner = banner.strip()
        except Exception:
            pass
            
        return result

    def export_results(self, results: Dict[str, List[ScanResult]], 
                      filename: str = "scan_results.json") -> None:
        """Export scan results to JSON file"""
        logger.info(f"Exporting results to {filename}")
        
        export_data = {}
        for host, scan_results in results.items():
            export_data[host] = []
            for result in scan_results:
                export_data[host].append({
                    'port': result.port,
                    'state': result.state,
                    'service': result.service,
                    'version': result.version,
                    'banner': result.banner,
                    'timestamp': result.timestamp.isoformat()
                })
                
        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            logger.info(f"Results exported successfully to {filename}")
        except Exception as e:
            logger.error(f"Failed to export results: {e}")
