#!/usr/bin/env python3
"""
Example usage of NSAF for basic network scanning and vulnerability assessment
"""

from nsaf import NetworkScanner, VulnerabilityScanner, ReportGenerator, get_logger

def main():
    """Example NSAF usage"""
    logger = get_logger(__name__)
    
    # Initialize components
    scanner = NetworkScanner(timeout=3, max_threads=50)
    vuln_scanner = VulnerabilityScanner()
    report_generator = ReportGenerator()
    
    # Define target network
    target_network = "192.168.1.0/24"  # Change this to your target network
    port_range = "1-1000"
    
    print("🔍 Starting Network Security Assessment...")
    print(f"Target: {target_network}")
    print(f"Ports: {port_range}")
    print("-" * 50)
    
    # 1. Host Discovery
    print("1. Discovering active hosts...")
    active_hosts = scanner.discover_hosts(target_network, method="ping")
    print(f"   Found {len(active_hosts)} active hosts")
    
    if not active_hosts:
        print("❌ No active hosts found. Exiting.")
        return
    
    # 2. Port Scanning
    print("2. Scanning ports...")
    scan_results = scanner.port_scan(active_hosts, port_range, "tcp_connect")
    
    total_open_ports = sum(len(ports) for ports in scan_results.values())
    print(f"   Found {total_open_ports} open ports across {len(scan_results)} hosts")
    
    # Display scan results
    print("\n📊 Scan Results:")
    print("-" * 70)
    print(f"{'Host':<15} {'Port':<8} {'State':<10} {'Service':<15} {'Version'}")
    print("-" * 70)
    
    for host, results in scan_results.items():
        for result in results:
            print(f"{result.host:<15} {result.port:<8} {result.state:<10} "
                  f"{result.service or 'unknown':<15} {result.version or ''}")
    
    # 3. Vulnerability Assessment
    print("\n3. Assessing vulnerabilities...")
    assessment_results = vuln_scanner.assess(scan_results)
    
    vulnerabilities = assessment_results['vulnerabilities']
    security_issues = assessment_results['security_issues']
    
    print(f"   Found {len(vulnerabilities)} vulnerabilities")
    print(f"   Found {len(security_issues)} security issues")
    
    # Display vulnerability summary
    if vulnerabilities:
        print("\n🚨 Vulnerability Summary:")
        severity_counts = {}
        for vuln in vulnerabilities:
            severity_counts[vuln.severity] = severity_counts.get(vuln.severity, 0) + 1
        
        for severity, count in severity_counts.items():
            print(f"   {severity.capitalize()}: {count}")
        
        print("\n🔍 Top Vulnerabilities:")
        for i, vuln in enumerate(vulnerabilities[:3], 1):
            print(f"   {i}. [{vuln.severity.upper()}] {vuln.title}")
            print(f"      Host: {vuln.host}:{vuln.port}")
            print(f"      Service: {vuln.affected_service}")
            print()
    
    # 4. Generate Reports
    print("4. Generating reports...")
    
    # Generate HTML report
    html_report = report_generator.generate_html_report(
        assessment_results, 
        "example_security_report.html",
        "Example Network Security Assessment"
    )
    
    if html_report:
        print(f"   ✅ HTML report: {html_report}")
    
    # Generate JSON report for further analysis
    json_report = report_generator.generate_json_report(
        assessment_results,
        "example_security_data.json"
    )
    
    if json_report:
        print(f"   ✅ JSON report: {json_report}")
    
    # Save scan results
    scanner.export_results(scan_results, "example_scan_results.json")
    print(f"   ✅ Scan results: example_scan_results.json")
    
    print("\n✅ Assessment complete!")
    print(f"📋 Summary:")
    print(f"   • Hosts scanned: {len(active_hosts)}")
    print(f"   • Open ports: {total_open_ports}")
    print(f"   • Vulnerabilities: {len(vulnerabilities)}")
    print(f"   • Security issues: {len(security_issues)}")

if __name__ == "__main__":
    main()
