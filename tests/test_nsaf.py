"""
Test suite for NSAF core functionality
"""

import pytest
import socket
import sys
from unittest.mock import Mock, patch, MagicMock

# Handle potential import issues gracefully
try:
    from nsaf.core.scanner import NetworkScanner, ScanResult, HostInfo
    from nsaf.core.vulnerability_scanner import VulnerabilityScanner, Vulnerability, SecurityIssue
    from nsaf.core.report_generator import ReportGenerator
    from nsaf.utils.logger import get_logger
except ImportError as e:
    pytest.skip(f"Skipping tests due to import error: {e}", allow_module_level=True)

class TestNetworkScanner:
    """Test NetworkScanner functionality"""
    
    def test_scanner_initialization(self):
        """Test scanner initialization"""
        scanner = NetworkScanner(timeout=5, max_threads=50)
        assert scanner.timeout == 5
        assert scanner.max_threads == 50
    
    def test_parse_ports(self):
        """Test port parsing functionality"""
        scanner = NetworkScanner()
        
        # Test single port
        ports = scanner._parse_ports("80")
        assert ports == [80]
        
        # Test port range
        ports = scanner._parse_ports("80-82")
        assert ports == [80, 81, 82]
        
        # Test comma-separated ports
        ports = scanner._parse_ports("80,443,8080")
        assert ports == [80, 443, 8080]
        
        # Test mixed format
        ports = scanner._parse_ports("22,80-82,443")
        assert sorted(ports) == [22, 80, 81, 82, 443]
    
    def test_identify_service(self):
        """Test service identification"""
        scanner = NetworkScanner()
        
        # Test known ports
        assert scanner._identify_service(80, "") == "http"
        assert scanner._identify_service(443, "") == "https"
        assert scanner._identify_service(22, "") == "ssh"
        
        # Test banner-based identification
        assert scanner._identify_service(8080, "HTTP/1.1 200 OK") == "http"
        assert scanner._identify_service(2222, "SSH-2.0-OpenSSH") == "ssh"
    
    @patch('socket.socket')
    def test_tcp_connect_scan(self, mock_socket):
        """Test TCP connect scan"""
        scanner = NetworkScanner()
        
        # Mock successful connection
        mock_sock = Mock()
        mock_sock.connect_ex.return_value = 0
        mock_sock.recv.return_value = b"HTTP/1.1 200 OK"
        mock_socket.return_value = mock_sock
        
        results = scanner._tcp_connect_scan("192.168.1.1", "80")
        
        assert len(results) == 1
        assert results[0].host == "192.168.1.1"
        assert results[0].port == 80
        assert results[0].state == "open"

class TestVulnerabilityScanner:
    """Test VulnerabilityScanner functionality"""
    
    def test_scanner_initialization(self):
        """Test vulnerability scanner initialization"""
        scanner = VulnerabilityScanner(timeout=10)
        assert scanner.timeout == 10
        assert isinstance(scanner.vuln_db, dict)
    
    def test_vulnerability_creation(self):
        """Test vulnerability object creation"""
        vuln = Vulnerability(
            vuln_id="TEST_001",
            title="Test Vulnerability", 
            description="A test vulnerability",
            severity="high",
            host="192.168.1.1",
            port=80,
            affected_service="http"
        )
        
        assert vuln.vuln_id == "TEST_001"
        assert vuln.severity == "high"
        assert vuln.host == "192.168.1.1"
    
    def test_security_issue_creation(self):
        """Test security issue object creation"""
        issue = SecurityIssue(
            issue_id="ISSUE_001",
            category="Configuration",
            title="Test Issue",
            description="A test security issue",
            risk_level="medium",
            host="192.168.1.1",
            service="http",
            evidence="Test evidence",
            recommendation="Test recommendation"
        )
        
        assert issue.issue_id == "ISSUE_001"
        assert issue.risk_level == "medium"
        assert issue.category == "Configuration"
    
    def test_weak_protocol_detection(self):
        """Test detection of weak protocols"""
        scanner = VulnerabilityScanner()
        
        # Create mock scan results
        scan_results = {
            "192.168.1.1": [
                ScanResult(host="192.168.1.1", port=23, state="open", service="telnet"),
                ScanResult(host="192.168.1.1", port=21, state="open", service="ftp")
            ]
        }
        
        scanner._check_weak_protocols("192.168.1.1", scan_results["192.168.1.1"])
        
        # Should detect telnet and FTP as weak protocols
        assert len(scanner.vulnerabilities) >= 2
        vuln_titles = [v.title for v in scanner.vulnerabilities]
        assert any("telnet" in title.lower() for title in vuln_titles)
        assert any("ftp" in title.lower() for title in vuln_titles)

class TestReportGenerator:
    """Test ReportGenerator functionality"""
    
    def test_generator_initialization(self):
        """Test report generator initialization"""
        generator = ReportGenerator()
        assert generator.template_dir == "templates"
        assert generator.reports_dir.name == "reports"
    
    def test_json_data_preparation(self):
        """Test JSON data preparation"""
        generator = ReportGenerator()
        
        # Test with vulnerability object
        vuln = Vulnerability(
            vuln_id="TEST_001",
            title="Test Vulnerability",
            description="Test description", 
            severity="high",
            host="192.168.1.1",
            port=80,
            affected_service="http"
        )
        
        json_data = generator._prepare_json_data(vuln)
        assert isinstance(json_data, dict)
        assert json_data['vuln_id'] == "TEST_001"
        assert json_data['severity'] == "high"
    
    def test_basic_html_report_generation(self):
        """Test basic HTML report generation"""
        generator = ReportGenerator()
        
        # Mock assessment results
        assessment_results = {
            'vulnerabilities': [],
            'security_issues': [],
            'summary': {
                'total_vulnerabilities': 0,
                'total_security_issues': 0
            },
            'recommendations': ['Update systems', 'Use strong passwords']
        }
        
        report_path = generator._generate_basic_html_report(
            assessment_results, 
            "test_report.html",
            "Test Report"
        )
        
        assert report_path.endswith("test_report.html")
        assert "reports" in report_path

class TestIntegration:
    """Integration tests for NSAF components"""
    
    def test_full_scan_workflow(self):
        """Test complete scan workflow"""
        # This would be a more comprehensive test in practice
        scanner = NetworkScanner(timeout=1, max_threads=10)
        vuln_scanner = VulnerabilityScanner(timeout=1)
        
        # Test with localhost (should be safe)
        scan_results = scanner.port_scan(["127.0.0.1"], "80,443")
        
        # Should return results (even if no ports are open)
        assert isinstance(scan_results, dict)
        assert "127.0.0.1" in scan_results
    
    @patch('nsaf.core.scanner.socket.socket')
    def test_vulnerability_assessment_workflow(self, mock_socket):
        """Test vulnerability assessment workflow"""
        # Mock scan results
        scan_results = {
            "192.168.1.1": [
                ScanResult(host="192.168.1.1", port=23, state="open", service="telnet"),
                ScanResult(host="192.168.1.1", port=80, state="open", service="http")
            ]
        }
        
        vuln_scanner = VulnerabilityScanner()
        assessment_results = vuln_scanner.assess(scan_results)
        
        assert 'vulnerabilities' in assessment_results
        assert 'security_issues' in assessment_results
        assert 'summary' in assessment_results
        assert 'recommendations' in assessment_results
        
        # Should detect telnet as a vulnerability
        vulns = assessment_results['vulnerabilities']
        assert any(v.affected_service == 'telnet' for v in vulns)

if __name__ == "__main__":
    pytest.main([__file__])
