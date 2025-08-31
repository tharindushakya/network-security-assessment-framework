#!/usr/bin/env python3
"""
Interactive demo of NSAF capabilities
This demo shows the main features without requiring network access
"""

import json
import os
from datetime import datetime
from nsaf import NetworkScanner, VulnerabilityScanner, ReportGenerator, get_logger
from nsaf.core.scanner import ScanResult
from nsaf.core.vulnerability_scanner import Vulnerability, SecurityIssue

def create_demo_data():
    """Create realistic demo data for demonstration"""
    
    # Simulate scan results for a fictional network
    demo_scan_results = {
        "192.168.1.1": [
            ScanResult(host="192.168.1.1", port=22, state="open", service="ssh", version="OpenSSH 7.4"),
            ScanResult(host="192.168.1.1", port=80, state="open", service="http", version="Apache 2.4.6"),
            ScanResult(host="192.168.1.1", port=443, state="open", service="https", version="Apache 2.4.6"),
            ScanResult(host="192.168.1.1", port=3306, state="open", service="mysql", version="MySQL 5.7")
        ],
        "192.168.1.10": [
            ScanResult(host="192.168.1.10", port=21, state="open", service="ftp", version="vsftpd 3.0.2"),
            ScanResult(host="192.168.1.10", port=23, state="open", service="telnet"),
            ScanResult(host="192.168.1.10", port=80, state="open", service="http", version="nginx 1.16.1"),
            ScanResult(host="192.168.1.10", port=445, state="open", service="microsoft-ds")
        ],
        "192.168.1.20": [
            ScanResult(host="192.168.1.20", port=80, state="open", service="http", version="IIS 10.0"),
            ScanResult(host="192.168.1.20", port=135, state="open", service="msrpc"),
            ScanResult(host="192.168.1.20", port=3389, state="open", service="ms-wbt-server"),
            ScanResult(host="192.168.1.20", port=5432, state="open", service="postgresql")
        ]
    }
    
    # Create realistic vulnerabilities
    demo_vulnerabilities = [
        Vulnerability(
            vuln_id="WEAK_PROTO_TELNET_192.168.1.10_23",
            title="Insecure Protocol: TELNET",
            description="The service TELNET is running on 192.168.1.10:23. This protocol transmits data in clear text.",
            severity="high",
            cvss_score=7.5,
            affected_service="telnet",
            host="192.168.1.10",
            port=23,
            evidence="Service telnet detected on port 23",
            remediation="Consider using secure alternatives to TELNET like SSH",
            references=["https://owasp.org/www-community/vulnerabilities/Insecure_Transport"]
        ),
        Vulnerability(
            vuln_id="WEAK_PROTO_FTP_192.168.1.10_21",
            title="Insecure Protocol: FTP",
            description="The service FTP is running on 192.168.1.10:21. This protocol transmits data in clear text.",
            severity="medium",
            cvss_score=5.3,
            affected_service="ftp",
            host="192.168.1.10",
            port=21,
            evidence="Service ftp detected on port 21",
            remediation="Consider using secure alternatives to FTP like SFTP or FTPS"
        ),
        Vulnerability(
            vuln_id="DB_EXPOSURE_MySQL_192.168.1.1_3306",
            title="Exposed MySQL Database",
            description="MySQL database service is accessible from the network",
            severity="high",
            cvss_score=7.5,
            affected_service="mysql",
            host="192.168.1.1",
            port=3306,
            evidence="MySQL service detected on port 3306",
            remediation="Ensure database is properly secured with authentication and access controls"
        ),
        Vulnerability(
            vuln_id="DB_EXPOSURE_PostgreSQL_192.168.1.20_5432",
            title="Exposed PostgreSQL Database",
            description="PostgreSQL database service is accessible from the network",
            severity="high",
            cvss_score=7.5,
            affected_service="postgresql",
            host="192.168.1.20",
            port=5432,
            evidence="PostgreSQL service detected on port 5432",
            remediation="Ensure database is properly secured with authentication and access controls"
        )
    ]
    
    # Create security issues
    demo_security_issues = [
        SecurityIssue(
            issue_id="SSH_DEFAULT_PORT_192.168.1.1",
            category="SSH Security",
            title="SSH Running on Default Port",
            description="SSH service is running on the default port 22, which is commonly targeted by attackers",
            risk_level="medium",
            host="192.168.1.1",
            service="ssh",
            evidence="SSH service detected on port 22",
            recommendation="Consider changing SSH to a non-standard port and implement fail2ban"
        ),
        SecurityIssue(
            issue_id="DANGEROUS_PORT_445_192.168.1.10",
            category="Network Security",
            title="Potentially Dangerous Port Open: 445",
            description="Port 445 is open and may represent a security risk",
            risk_level="medium",
            host="192.168.1.10",
            service="microsoft-ds",
            evidence="Port 445 is accessible",
            recommendation="Ensure port 445 is properly secured or close if not needed"
        ),
        SecurityIssue(
            issue_id="DANGEROUS_PORT_3389_192.168.1.20",
            category="Network Security",
            title="Potentially Dangerous Port Open: 3389",
            description="Port 3389 (RDP) is open and may represent a security risk",
            risk_level="high",
            host="192.168.1.20",
            service="ms-wbt-server",
            evidence="Port 3389 is accessible",
            recommendation="Ensure RDP is properly secured with strong authentication and consider VPN access"
        )
    ]
    
    return demo_scan_results, demo_vulnerabilities, demo_security_issues

def run_demo():
    """Run the NSAF demonstration"""
    logger = get_logger(__name__)
    
    print("🎭 NSAF Interactive Demo")
    print("=" * 60)
    print("This demo showcases NSAF capabilities using simulated data")
    print("No actual network scanning will be performed")
    print("-" * 60)
    
    # Create demo data
    print("\n📊 Creating demonstration data...")
    scan_results, vulnerabilities, security_issues = create_demo_data()
    
    # Display scan results summary
    print(f"\n🔍 Simulated Scan Results:")
    total_ports = sum(len(results) for results in scan_results.values())
    print(f"   • Hosts scanned: {len(scan_results)}")
    print(f"   • Total open ports: {total_ports}")
    
    # Show detailed scan results
    print(f"\n📋 Detailed Scan Results:")
    print("-" * 70)
    print(f"{'Host':<15} {'Port':<8} {'State':<10} {'Service':<15} {'Version'}")
    print("-" * 70)
    
    for host, results in scan_results.items():
        for result in results:
            print(f"{result.host:<15} {result.port:<8} {result.state:<10} "
                  f"{result.service or 'unknown':<15} {result.version or ''}")
    
    # Initialize vulnerability scanner and assess
    print(f"\n🚨 Running Vulnerability Assessment...")
    vuln_scanner = VulnerabilityScanner()
    
    # Create assessment results
    assessment_results = {
        'vulnerabilities': vulnerabilities,
        'security_issues': security_issues,
        'summary': {
            'total_vulnerabilities': len(vulnerabilities),
            'total_security_issues': len(security_issues),
            'severity_distribution': {
                'critical': 0,
                'high': len([v for v in vulnerabilities if v.severity == 'high']),
                'medium': len([v for v in vulnerabilities if v.severity == 'medium']),
                'low': len([v for v in vulnerabilities if v.severity == 'low']),
                'info': 0
            },
            'affected_hosts': list(set([v.host for v in vulnerabilities])),
            'assessment_date': datetime.now().isoformat()
        },
        'recommendations': [
            "Address high-severity vulnerabilities immediately",
            "Replace insecure protocols with secure alternatives",
            "Implement proper database access controls",
            "Use network segmentation to limit exposure",
            "Deploy intrusion detection systems",
            "Conduct regular security assessments",
            "Implement security monitoring and logging"
        ]
    }
    
    # Display vulnerability summary
    print(f"\n🎯 Vulnerability Assessment Results:")
    print(f"   • Total vulnerabilities: {len(vulnerabilities)}")
    print(f"   • Total security issues: {len(security_issues)}")
    
    severity_dist = assessment_results['summary']['severity_distribution']
    print(f"   • Critical: {severity_dist['critical']}")
    print(f"   • High: {severity_dist['high']}")
    print(f"   • Medium: {severity_dist['medium']}")
    print(f"   • Low: {severity_dist['low']}")
    
    # Show top vulnerabilities
    print(f"\n🔥 Top Vulnerabilities:")
    for i, vuln in enumerate(vulnerabilities[:3], 1):
        print(f"   {i}. [{vuln.severity.upper()}] {vuln.title}")
        print(f"      Host: {vuln.host}:{vuln.port} ({vuln.affected_service})")
        print(f"      CVSS: {vuln.cvss_score}")
        print()
    
    # Generate reports
    print(f"📋 Generating Demonstration Reports...")
    report_generator = ReportGenerator()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate HTML report
    html_report = report_generator.generate_html_report(
        assessment_results,
        f"demo_security_report_{timestamp}.html",
        "NSAF Demo - Network Security Assessment"
    )
    
    # Generate JSON report
    json_report = report_generator.generate_json_report(
        assessment_results,
        f"demo_assessment_data_{timestamp}.json"
    )
    
    # Generate CSV report
    csv_report = report_generator.generate_csv_report(
        assessment_results,
        f"demo_vulnerability_summary_{timestamp}.csv"
    )
    
    print(f"\n✅ Demo Reports Generated:")
    if html_report:
        print(f"   📄 HTML Report: {html_report}")
    if json_report:
        print(f"   📊 JSON Data: {json_report}")
    if csv_report:
        print(f"   📈 CSV Summary: {csv_report}")
    
    # Save scan results
    scanner = NetworkScanner()
    scanner.export_results(scan_results, f"demo_scan_results_{timestamp}.json")
    print(f"   🔍 Scan Results: demo_scan_results_{timestamp}.json")
    
    # Display recommendations
    print(f"\n💡 Security Recommendations:")
    for i, rec in enumerate(assessment_results['recommendations'], 1):
        print(f"   {i}. {rec}")
    
    print(f"\n🎉 Demo completed successfully!")
    print(f"\nOpen the HTML report in your browser to see the full assessment:")
    if html_report:
        abs_path = os.path.abspath(html_report)
        print(f"   file://{abs_path}")
    
    print(f"\n📚 Next Steps:")
    print(f"   • Try the CLI: python nsaf_cli.py --help")
    print(f"   • Run a real scan: python nsaf_cli.py scan -t 127.0.0.1")
    print(f"   • Check the examples/ directory for more usage patterns")
    print(f"   • Visit the documentation: https://github.com/yourusername/network-security-assessment-framework/wiki")

if __name__ == "__main__":
    run_demo()
