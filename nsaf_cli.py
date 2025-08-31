#!/usr/bin/env python3
"""
Network Security Assessment Framework (NSAF)
Command Line Interface

A comprehensive network security assessment tool that automates vulnerability 
scanning and generates detailed reports.
"""

import sys
import argparse
import json
from pathlib import Path
from typing import List, Optional

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.panel import Panel
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from nsaf import NetworkScanner, VulnerabilityScanner, ReportGenerator, get_logger
from nsaf.utils.logger import setup_logging

# Initialize console and logger
if RICH_AVAILABLE:
    console = Console()
else:
    console = None

logger = get_logger(__name__)

def print_banner():
    """Print application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║    Network Security Assessment Framework (NSAF) v1.0.0       ║
    ║                                                               ║
    ║    A comprehensive network security assessment tool           ║
    ║    * Automated vulnerability scanning                         ║
    ║    * Network reconnaissance                                   ║
    ║    * Detailed security reporting                              ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    
    if RICH_AVAILABLE:
        console.print(banner, style="bold blue")
    else:
        print(banner)

def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Network Security Assessment Framework (NSAF)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic network scan
  python nsaf_cli.py scan -t 192.168.1.0/24

  # Comprehensive assessment with vulnerability scanning
  python nsaf_cli.py assess -t 192.168.1.100 -p 1-1000 --vuln-scan

  # Generate only HTML report from previous scan results
  python nsaf_cli.py report -i scan_results.json -f html

  # Full assessment with all report formats
  python nsaf_cli.py assess -t 192.168.1.0/24 --all-reports
        """
    )
    
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--version', action='version', version='NSAF 1.0.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Perform network scanning')
    scan_parser.add_argument('-t', '--targets', required=True,
                            help='Target hosts or network (e.g., 192.168.1.0/24, 10.0.0.1)')
    scan_parser.add_argument('-p', '--ports', default='1-1000',
                            help='Port range to scan (default: 1-1000)')
    scan_parser.add_argument('--scan-type', choices=['tcp_connect', 'tcp_syn', 'udp'],
                            default='tcp_connect', help='Type of port scan')
    scan_parser.add_argument('--discovery', choices=['ping', 'arp', 'tcp_syn'],
                            default='ping', help='Host discovery method')
    scan_parser.add_argument('-o', '--output', help='Output file for scan results')
    scan_parser.add_argument('--timeout', type=int, default=3,
                            help='Connection timeout in seconds (default: 3)')
    scan_parser.add_argument('--threads', type=int, default=100,
                            help='Maximum number of threads (default: 100)')
    
    # Assess command (scan + vulnerability assessment)
    assess_parser = subparsers.add_parser('assess', help='Perform comprehensive security assessment')
    assess_parser.add_argument('-t', '--targets', required=True,
                              help='Target hosts or network')
    assess_parser.add_argument('-p', '--ports', default='1-1000',
                              help='Port range to scan (default: 1-1000)')
    assess_parser.add_argument('--scan-type', choices=['tcp_connect', 'tcp_syn', 'udp'],
                              default='tcp_connect', help='Type of port scan')
    assess_parser.add_argument('--discovery', choices=['ping', 'arp', 'tcp_syn'],
                              default='ping', help='Host discovery method')
    assess_parser.add_argument('--vuln-scan', action='store_true',
                              help='Enable vulnerability scanning')
    assess_parser.add_argument('--timeout', type=int, default=3,
                              help='Connection timeout in seconds')
    assess_parser.add_argument('--threads', type=int, default=100,
                              help='Maximum number of threads')
    assess_parser.add_argument('--report-format', choices=['html', 'pdf', 'json', 'csv'],
                              default='html', help='Report format')
    assess_parser.add_argument('--all-reports', action='store_true',
                              help='Generate all report formats')
    assess_parser.add_argument('-o', '--output', help='Output directory for reports')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate reports from scan results')
    report_parser.add_argument('-i', '--input', required=True,
                              help='Input file with scan results (JSON)')
    report_parser.add_argument('-f', '--format', choices=['html', 'pdf', 'json', 'csv'],
                              default='html', help='Report format')
    report_parser.add_argument('--all-formats', action='store_true',
                              help='Generate all report formats')
    report_parser.add_argument('-o', '--output', help='Output directory for reports')
    report_parser.add_argument('--title', default='Network Security Assessment Report',
                              help='Report title')
    
    return parser

def display_scan_results(scan_results, show_summary=True):
    """Display scan results in a formatted table"""
    if not scan_results:
        if RICH_AVAILABLE:
            console.print("[yellow]No scan results to display[/yellow]")
        else:
            print("No scan results to display")
        return
    
    total_open_ports = sum(len(ports) for ports in scan_results.values())
    
    if show_summary:
        if RICH_AVAILABLE:
            console.print(f"\n[bold green]Scan Summary:[/bold green]")
            console.print(f"  • Hosts scanned: {len(scan_results)}")
            console.print(f"  • Total open ports: {total_open_ports}")
        else:
            print(f"\nScan Summary:")
            print(f"  • Hosts scanned: {len(scan_results)}")
            print(f"  • Total open ports: {total_open_ports}")
    
    if RICH_AVAILABLE:
        table = Table(title="Scan Results")
        table.add_column("Host", style="cyan")
        table.add_column("Port", style="magenta")
        table.add_column("State", style="green")
        table.add_column("Service", style="yellow")
        table.add_column("Version", style="blue")
        
        for host, results in scan_results.items():
            for result in results:
                table.add_row(
                    result.host,
                    str(result.port),
                    result.state,
                    result.service or "unknown",
                    result.version or ""
                )
        
        console.print(table)
    else:
        print("\nScan Results:")
        print("-" * 80)
        print(f"{'Host':<15} {'Port':<8} {'State':<10} {'Service':<15} {'Version'}")
        print("-" * 80)
        
        for host, results in scan_results.items():
            for result in results:
                print(f"{result.host:<15} {result.port:<8} {result.state:<10} "
                      f"{result.service or 'unknown':<15} {result.version or ''}")

def display_vulnerabilities(vulnerabilities):
    """Display vulnerabilities in a formatted way"""
    if not vulnerabilities:
        if RICH_AVAILABLE:
            console.print("[green]No vulnerabilities found[/green]")
        else:
            print("No vulnerabilities found")
        return
    
    severity_counts = {}
    for vuln in vulnerabilities:
        severity_counts[vuln.severity] = severity_counts.get(vuln.severity, 0) + 1
    
    if RICH_AVAILABLE:
        console.print(f"\n[bold red]Vulnerability Summary:[/bold red]")
        for severity, count in severity_counts.items():
            color = {
                'critical': 'red',
                'high': 'orange',
                'medium': 'yellow', 
                'low': 'green',
                'info': 'blue'
            }.get(severity, 'white')
            console.print(f"  • {severity.capitalize()}: {count}", style=color)
        
        console.print("\n[bold]Vulnerability Details:[/bold]")
        for vuln in vulnerabilities:
            severity_color = {
                'critical': 'red',
                'high': 'orange',
                'medium': 'yellow',
                'low': 'green', 
                'info': 'blue'
            }.get(vuln.severity, 'white')
            
            panel_content = f"""
[bold]Host:[/bold] {vuln.host}:{vuln.port}
[bold]Service:[/bold] {vuln.affected_service}
[bold]Description:[/bold] {vuln.description}
[bold]Remediation:[/bold] {vuln.remediation}
            """
            
            console.print(Panel(
                panel_content.strip(),
                title=f"[{severity_color}]{vuln.severity.upper()}[/{severity_color}] - {vuln.title}",
                border_style=severity_color
            ))
    else:
        print(f"\nVulnerability Summary:")
        for severity, count in severity_counts.items():
            print(f"  • {severity.capitalize()}: {count}")
        
        print("\nVulnerability Details:")
        print("=" * 80)
        for vuln in vulnerabilities:
            print(f"\n[{vuln.severity.upper()}] {vuln.title}")
            print(f"Host: {vuln.host}:{vuln.port}")
            print(f"Service: {vuln.affected_service}")
            print(f"Description: {vuln.description}")
            print(f"Remediation: {vuln.remediation}")
            print("-" * 80)

def cmd_scan(args):
    """Execute scan command"""
    if RICH_AVAILABLE:
        console.print(f"[bold green]Starting network scan...[/bold green]")
    else:
        print("Starting network scan...")
    
    # Initialize scanner
    scanner = NetworkScanner(timeout=args.timeout, max_threads=args.threads)
    
    # Discover hosts
    if RICH_AVAILABLE:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Discovering hosts...", total=None)
            hosts = scanner.discover_hosts(args.targets, method=args.discovery)
            progress.update(task, completed=True)
    else:
        print("Discovering hosts...")
        hosts = scanner.discover_hosts(args.targets, method=args.discovery)
    
    if not hosts:
        if RICH_AVAILABLE:
            console.print("[red]No active hosts found[/red]")
        else:
            print("No active hosts found")
        return
    
    if RICH_AVAILABLE:
        console.print(f"[green]Found {len(hosts)} active hosts[/green]")
    else:
        print(f"Found {len(hosts)} active hosts")
    
    # Perform port scan
    if RICH_AVAILABLE:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Scanning ports...", total=None)
            scan_results = scanner.port_scan(hosts, args.ports, args.scan_type)
            progress.update(task, completed=True)
    else:
        print("Scanning ports...")
        scan_results = scanner.port_scan(hosts, args.ports, args.scan_type)
    
    # Display results
    display_scan_results(scan_results)
    
    # Save results if requested
    if args.output:
        scanner.export_results(scan_results, args.output)
        if RICH_AVAILABLE:
            console.print(f"[green]Results saved to {args.output}[/green]")
        else:
            print(f"Results saved to {args.output}")

def cmd_assess(args):
    """Execute assess command"""
    if RICH_AVAILABLE:
        console.print(f"[bold green]Starting comprehensive security assessment...[/bold green]")
    else:
        print("Starting comprehensive security assessment...")
    
    # Initialize components
    scanner = NetworkScanner(timeout=args.timeout, max_threads=args.threads)
    vuln_scanner = VulnerabilityScanner(timeout=args.timeout)
    report_generator = ReportGenerator()
    
    # Discover hosts
    if RICH_AVAILABLE:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Discovering hosts...", total=None)
            hosts = scanner.discover_hosts(args.targets, method=args.discovery)
            progress.update(task, completed=True)
    else:
        print("Discovering hosts...")
        hosts = scanner.discover_hosts(args.targets, method=args.discovery)
    
    if not hosts:
        if RICH_AVAILABLE:
            console.print("[red]No active hosts found[/red]")
        else:
            print("No active hosts found")
        return
    
    # Perform port scan
    if RICH_AVAILABLE:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Scanning ports...", total=None)
            scan_results = scanner.port_scan(hosts, args.ports, args.scan_type)
            progress.update(task, completed=True)
    else:
        print("Scanning ports...")
        scan_results = scanner.port_scan(hosts, args.ports, args.scan_type)
    
    # Display scan results
    display_scan_results(scan_results)
    
    # Perform vulnerability assessment if requested
    assessment_results = None
    if args.vuln_scan:
        if RICH_AVAILABLE:
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
                task = progress.add_task("Assessing vulnerabilities...", total=None)
                assessment_results = vuln_scanner.assess(scan_results)
                progress.update(task, completed=True)
        else:
            print("Assessing vulnerabilities...")
            assessment_results = vuln_scanner.assess(scan_results)
        
        # Display vulnerability results
        display_vulnerabilities(assessment_results['vulnerabilities'])
        
        # Generate reports
        if RICH_AVAILABLE:
            console.print(f"\n[bold blue]Generating reports...[/bold blue]")
        else:
            print("\nGenerating reports...")
        
        if args.all_reports:
            report_files = report_generator.generate_all_reports(assessment_results)
            if RICH_AVAILABLE:
                console.print("[green]Generated reports:[/green]")
                for format_type, file_path in report_files.items():
                    console.print(f"  • {format_type.upper()}: {file_path}")
            else:
                print("Generated reports:")
                for format_type, file_path in report_files.items():
                    print(f"  • {format_type.upper()}: {file_path}")
        else:
            if args.report_format == 'html':
                report_file = report_generator.generate_html_report(assessment_results)
            elif args.report_format == 'pdf':
                report_file = report_generator.generate_pdf_report(assessment_results)
            elif args.report_format == 'json':
                report_file = report_generator.generate_json_report(assessment_results)
            elif args.report_format == 'csv':
                report_file = report_generator.generate_csv_report(assessment_results)
            
            if report_file:
                if RICH_AVAILABLE:
                    console.print(f"[green]Report generated: {report_file}[/green]")
                else:
                    print(f"Report generated: {report_file}")

def cmd_report(args):
    """Execute report command"""
    if RICH_AVAILABLE:
        console.print(f"[bold green]Generating report from {args.input}...[/bold green]")
    else:
        print(f"Generating report from {args.input}...")
    
    # Load scan results
    try:
        with open(args.input, 'r') as f:
            data = json.load(f)
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error loading input file: {e}[/red]")
        else:
            print(f"Error loading input file: {e}")
        return
    
    # Initialize report generator
    report_generator = ReportGenerator()
    
    # Generate reports
    if args.all_formats:
        report_files = report_generator.generate_all_reports(data)
        if RICH_AVAILABLE:
            console.print("[green]Generated reports:[/green]")
            for format_type, file_path in report_files.items():
                console.print(f"  • {format_type.upper()}: {file_path}")
        else:
            print("Generated reports:")
            for format_type, file_path in report_files.items():
                print(f"  • {format_type.upper()}: {file_path}")
    else:
        if args.format == 'html':
            report_file = report_generator.generate_html_report(data, title=args.title)
        elif args.format == 'pdf':
            report_file = report_generator.generate_pdf_report(data, title=args.title)
        elif args.format == 'json':
            report_file = report_generator.generate_json_report(data)
        elif args.format == 'csv':
            report_file = report_generator.generate_csv_report(data)
        
        if report_file:
            if RICH_AVAILABLE:
                console.print(f"[green]Report generated: {report_file}[/green]")
            else:
                print(f"Report generated: {report_file}")

def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    
    # Print banner
    print_banner()
    
    # Execute command
    if args.command == 'scan':
        cmd_scan(args)
    elif args.command == 'assess':
        cmd_assess(args)
    elif args.command == 'report':
        cmd_report(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if RICH_AVAILABLE:
            console.print("\n[yellow]Scan interrupted by user[/yellow]")
        else:
            print("\nScan interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if RICH_AVAILABLE:
            console.print(f"[red]Error: {e}[/red]")
        else:
            print(f"Error: {e}")
        sys.exit(1)
