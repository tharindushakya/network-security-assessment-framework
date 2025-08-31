#!/usr/bin/env python3
"""
Advanced NSAF usage example with custom vulnerability checks and detailed reporting
"""

import json
from datetime import datetime
from nsaf import NetworkScanner, VulnerabilityScanner, ReportGenerator, get_logger
from nsaf.core.vulnerability_scanner import Vulnerability, SecurityIssue

class CustomVulnerabilityScanner(VulnerabilityScanner):
    """Extended vulnerability scanner with custom checks"""
    
    def custom_assessment(self, scan_results):
        """Perform custom vulnerability assessments"""
        logger = get_logger(__name__)
        logger.info("Running custom vulnerability assessments")
        
        # Custom check for weak SSH configurations
        self._check_ssh_weaknesses(scan_results)
        
        # Custom check for database services
        self._check_database_exposure(scan_results)
        
        # Custom check for web server configurations
        self._check_web_server_security(scan_results)
        
        return {
            'custom_vulnerabilities': self.vulnerabilities,
            'custom_issues': self.security_issues
        }
    
    def _check_ssh_weaknesses(self, scan_results):
        """Check for SSH-related security issues"""
        for host, results in scan_results.items():
            for result in results:
                if result.port == 22 and 'ssh' in result.service.lower():
                    # Check if SSH is on default port
                    issue = SecurityIssue(
                        issue_id=f"SSH_DEFAULT_PORT_{host}",
                        category="SSH Security",
                        title="SSH Running on Default Port",
                        description="SSH service is running on the default port 22, which is commonly targeted by attackers",
                        risk_level="medium",
                        host=host,
                        service="ssh",
                        evidence=f"SSH service detected on port 22",
                        recommendation="Consider changing SSH to a non-standard port and implement fail2ban"
                    )
                    self.security_issues.append(issue)
    
    def _check_database_exposure(self, scan_results):
        """Check for exposed database services"""
        db_ports = {
            3306: "MySQL",
            5432: "PostgreSQL", 
            1433: "SQL Server",
            27017: "MongoDB",
            6379: "Redis"
        }
        
        for host, results in scan_results.items():
            for result in results:
                if result.port in db_ports:
                    vuln = Vulnerability(
                        vuln_id=f"DB_EXPOSURE_{db_ports[result.port]}_{host}_{result.port}",
                        title=f"Exposed {db_ports[result.port]} Database",
                        description=f"{db_ports[result.port]} database service is accessible from the network",
                        severity="high",
                        cvss_score=7.5,
                        affected_service=db_ports[result.port].lower(),
                        host=host,
                        port=result.port,
                        evidence=f"{db_ports[result.port]} service detected on port {result.port}",
                        remediation="Ensure database is properly secured with authentication and access controls"
                    )
                    self.vulnerabilities.append(vuln)
    
    def _check_web_server_security(self, scan_results):
        """Check for web server security issues"""
        web_ports = [80, 443, 8080, 8443, 8000]
        
        for host, results in scan_results.items():
            for result in results:
                if result.port in web_ports:
                    # Check for HTTP on non-standard ports
                    if result.port not in [80, 443]:
                        issue = SecurityIssue(
                            issue_id=f"WEB_NONSTANDARD_PORT_{host}_{result.port}",
                            category="Web Security",
                            title="Web Service on Non-Standard Port",
                            description=f"Web service running on non-standard port {result.port}",
                            risk_level="low",
                            host=host,
                            service="web",
                            evidence=f"HTTP service on port {result.port}",
                            recommendation="Ensure non-standard web services are properly secured"
                        )
                        self.security_issues.append(issue)

def advanced_assessment_example():
    """Demonstrate advanced NSAF usage"""
    logger = get_logger(__name__)
    
    print("🔬 Advanced Network Security Assessment")
    print("=" * 50)
    
    # Configuration
    targets = ["192.168.1.100", "192.168.1.1"]  # Specific targets
    port_ranges = {
        "common": "20-25,53,80,110,143,443,993,995",
        "extended": "1-1000",
        "databases": "1433,3306,5432,27017,6379"
    }
    
    # Initialize enhanced scanner
    scanner = NetworkScanner(timeout=5, max_threads=50)
    custom_vuln_scanner = CustomVulnerabilityScanner(timeout=10)
    report_generator = ReportGenerator()
    
    all_results = {}
    
    # Perform multiple scan types
    for scan_name, ports in port_ranges.items():
        print(f"\n🎯 Performing {scan_name} port scan...")
        print(f"   Targets: {targets}")
        print(f"   Ports: {ports}")
        
        scan_results = scanner.port_scan(targets, ports, "tcp_connect")
        all_results[scan_name] = scan_results
        
        # Display results for this scan
        total_ports = sum(len(results) for results in scan_results.values())
        print(f"   Found {total_ports} open ports")
        
        for host, results in scan_results.items():
            if results:
                print(f"   {host}: {[r.port for r in results]}")
    
    # Combine all scan results
    combined_results = {}
    for scan_results in all_results.values():
        for host, results in scan_results.items():
            if host not in combined_results:
                combined_results[host] = []
            combined_results[host].extend(results)
    
    # Remove duplicates
    for host in combined_results:
        seen_ports = set()
        unique_results = []
        for result in combined_results[host]:
            if result.port not in seen_ports:
                unique_results.append(result)
                seen_ports.add(result.port)
        combined_results[host] = unique_results
    
    print(f"\n🔍 Combined Scan Results:")
    total_unique_ports = sum(len(results) for results in combined_results.values())
    print(f"   Total unique open ports: {total_unique_ports}")
    
    # Perform standard vulnerability assessment
    print(f"\n🚨 Standard Vulnerability Assessment...")
    standard_assessment = custom_vuln_scanner.assess(combined_results)
    
    # Perform custom vulnerability assessment
    print(f"🔬 Custom Vulnerability Assessment...")
    custom_assessment = custom_vuln_scanner.custom_assessment(combined_results)
    
    # Combine assessments
    all_vulnerabilities = (standard_assessment['vulnerabilities'] + 
                          custom_assessment['custom_vulnerabilities'])
    all_issues = (standard_assessment['security_issues'] + 
                 custom_assessment['custom_issues'])
    
    # Create comprehensive assessment results
    comprehensive_results = {
        'vulnerabilities': all_vulnerabilities,
        'security_issues': all_issues,
        'summary': {
            'total_vulnerabilities': len(all_vulnerabilities),
            'total_security_issues': len(all_issues),
            'assessment_date': datetime.now().isoformat(),
            'scan_types_performed': list(port_ranges.keys()),
            'targets_scanned': targets,
            'severity_distribution': {}
        },
        'recommendations': []
    }
    
    # Calculate severity distribution
    for vuln in all_vulnerabilities:
        severity = vuln.severity
        comprehensive_results['summary']['severity_distribution'][severity] = \
            comprehensive_results['summary']['severity_distribution'].get(severity, 0) + 1
    
    # Generate enhanced recommendations
    recommendations = set(standard_assessment['recommendations'])
    recommendations.add("Implement network segmentation for database services")
    recommendations.add("Use non-standard ports for administrative services")
    recommendations.add("Deploy web application firewall (WAF) for web services")
    recommendations.add("Implement intrusion detection/prevention system (IDS/IPS)")
    comprehensive_results['recommendations'] = list(recommendations)
    
    # Display comprehensive results
    print(f"\n📊 Comprehensive Assessment Results:")
    print(f"   • Total vulnerabilities: {len(all_vulnerabilities)}")
    print(f"   • Total security issues: {len(all_issues)}")
    
    if all_vulnerabilities:
        print(f"\n   🚨 Severity Distribution:")
        for severity, count in comprehensive_results['summary']['severity_distribution'].items():
            print(f"      {severity.capitalize()}: {count}")
    
    # Generate multiple report formats
    print(f"\n📋 Generating comprehensive reports...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"advanced_security_assessment_{timestamp}"
    
    report_files = report_generator.generate_all_reports(
        comprehensive_results, 
        base_filename
    )
    
    print(f"   Generated reports:")
    for format_type, file_path in report_files.items():
        print(f"      📄 {format_type.upper()}: {file_path}")
    
    # Save detailed scan data
    detailed_data = {
        'scan_configuration': {
            'targets': targets,
            'port_ranges': port_ranges,
            'scan_date': datetime.now().isoformat()
        },
        'scan_results': {
            scan_name: {
                host: [
                    {
                        'port': r.port,
                        'state': r.state,
                        'service': r.service,
                        'version': r.version,
                        'banner': r.banner
                    } for r in results
                ] for host, results in scan_results.items()
            } for scan_name, scan_results in all_results.items()
        },
        'assessment_results': comprehensive_results
    }
    
    detailed_filename = f"detailed_assessment_data_{timestamp}.json"
    with open(detailed_filename, 'w') as f:
        json.dump(detailed_data, f, indent=2, default=str)
    
    print(f"      📊 Detailed data: {detailed_filename}")
    
    print(f"\n✅ Advanced assessment complete!")
    return comprehensive_results

if __name__ == "__main__":
    advanced_assessment_example()
