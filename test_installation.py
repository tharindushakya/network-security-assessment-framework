#!/usr/bin/env python3
"""
Quick test script to verify NSAF installation and basic functionality
"""

import sys
from nsaf import NetworkScanner, VulnerabilityScanner, ReportGenerator, get_logger

def test_basic_functionality():
    """Test basic NSAF functionality"""
    logger = get_logger(__name__)
    
    print("🧪 Testing NSAF Basic Functionality")
    print("=" * 50)
    
    # Test 1: Scanner initialization
    print("1. Testing NetworkScanner initialization...")
    try:
        scanner = NetworkScanner(timeout=1, max_threads=10)
        print("   ✅ NetworkScanner initialized successfully")
    except Exception as e:
        print(f"   ❌ NetworkScanner failed: {e}")
        return False
    
    # Test 2: VulnerabilityScanner initialization
    print("2. Testing VulnerabilityScanner initialization...")
    try:
        vuln_scanner = VulnerabilityScanner(timeout=1)
        print("   ✅ VulnerabilityScanner initialized successfully")
    except Exception as e:
        print(f"   ❌ VulnerabilityScanner failed: {e}")
        return False
    
    # Test 3: ReportGenerator initialization
    print("3. Testing ReportGenerator initialization...")
    try:
        report_generator = ReportGenerator()
        print("   ✅ ReportGenerator initialized successfully")
    except Exception as e:
        print(f"   ❌ ReportGenerator failed: {e}")
        return False
    
    # Test 4: Port parsing
    print("4. Testing port parsing...")
    try:
        ports = scanner._parse_ports("22,80-82,443")
        expected = [22, 80, 81, 82, 443]
        if sorted(ports) == sorted(expected):
            print("   ✅ Port parsing works correctly")
        else:
            print(f"   ❌ Port parsing failed. Expected {expected}, got {ports}")
            return False
    except Exception as e:
        print(f"   ❌ Port parsing failed: {e}")
        return False
    
    # Test 5: Service identification
    print("5. Testing service identification...")
    try:
        service = scanner._identify_service(80, "HTTP/1.1 200 OK")
        if service == "http":
            print("   ✅ Service identification works correctly")
        else:
            print(f"   ❌ Service identification failed. Expected 'http', got '{service}'")
            return False
    except Exception as e:
        print(f"   ❌ Service identification failed: {e}")
        return False
    
    # Test 6: Basic scan on localhost (safe test)
    print("6. Testing basic localhost scan...")
    try:
        # Test with localhost - should be safe and work on any system
        scan_results = scanner.port_scan(["127.0.0.1"], "80,443", "tcp_connect")
        if isinstance(scan_results, dict) and "127.0.0.1" in scan_results:
            print("   ✅ Basic scan completed successfully")
        else:
            print("   ❌ Basic scan failed - unexpected result format")
            return False
    except Exception as e:
        print(f"   ❌ Basic scan failed: {e}")
        return False
    
    # Test 7: Vulnerability assessment
    print("7. Testing vulnerability assessment...")
    try:
        # Create mock scan results for testing
        from nsaf.core.scanner import ScanResult
        mock_results = {
            "127.0.0.1": [
                ScanResult(host="127.0.0.1", port=23, state="open", service="telnet"),
                ScanResult(host="127.0.0.1", port=80, state="open", service="http")
            ]
        }
        
        assessment = vuln_scanner.assess(mock_results)
        required_keys = ['vulnerabilities', 'security_issues', 'summary', 'recommendations']
        
        if all(key in assessment for key in required_keys):
            print("   ✅ Vulnerability assessment completed successfully")
        else:
            print("   ❌ Vulnerability assessment failed - missing required keys")
            return False
    except Exception as e:
        print(f"   ❌ Vulnerability assessment failed: {e}")
        return False
    
    # Test 8: Report generation
    print("8. Testing report generation...")
    try:
        test_data = {
            'vulnerabilities': [],
            'security_issues': [],
            'summary': {
                'total_vulnerabilities': 0,
                'total_security_issues': 0,
                'severity_distribution': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
            },
            'recommendations': ['Test recommendation']
        }
        
        # Test JSON report generation
        json_report = report_generator.generate_json_report(test_data, "test_report.json")
        if json_report and json_report.endswith("test_report.json"):
            print("   ✅ Report generation completed successfully")
        else:
            print("   ❌ Report generation failed")
            return False
    except Exception as e:
        print(f"   ❌ Report generation failed: {e}")
        return False
    
    print("\n🎉 All tests passed successfully!")
    print("NSAF is ready for use.")
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
