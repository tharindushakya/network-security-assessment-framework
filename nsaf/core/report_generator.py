"""
Report generation module for NSAF.
Generates comprehensive security assessment reports in multiple formats.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import base64

try:
    from jinja2 import Template, Environment, FileSystemLoader
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from ..utils.logger import get_logger
from .vulnerability_scanner import Vulnerability, SecurityIssue

logger = get_logger(__name__)

class ReportGenerator:
    """Comprehensive report generator for security assessments"""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize ReportGenerator
        
        Args:
            template_dir: Directory containing report templates
        """
        self.template_dir = template_dir or "templates"
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
        
        # Ensure templates directory exists
        Path(self.template_dir).mkdir(exist_ok=True)
        
        # Create default templates if they don't exist
        self._create_default_templates()

    def _create_default_templates(self) -> None:
        """Create default HTML report templates"""
        template_path = Path(self.template_dir)
        
        # Main report template
        main_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ report_title }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #2c3e50;
            margin: 0;
            font-size: 2.5em;
        }
        .header .subtitle {
            color: #7f8c8d;
            margin-top: 10px;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .summary-card h3 {
            margin: 0 0 10px 0;
            font-size: 2em;
        }
        .severity-critical { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); }
        .severity-high { background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%); }
        .severity-medium { background: linear-gradient(135deg, #ffca28 0%, #ffc107 100%); }
        .severity-low { background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%); }
        
        .section {
            margin-bottom: 40px;
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .vulnerability, .security-issue {
            background: #f8f9fa;
            border-left: 5px solid #3498db;
            margin: 15px 0;
            padding: 20px;
            border-radius: 5px;
        }
        .vulnerability.critical {
            border-left-color: #e74c3c;
            background: #fdf2f2;
        }
        .vulnerability.high {
            border-left-color: #f39c12;
            background: #fef9e7;
        }
        .vulnerability.medium {
            border-left-color: #f1c40f;
            background: #fffbf0;
        }
        .vulnerability.low {
            border-left-color: #27ae60;
            background: #f0f9f0;
        }
        .vuln-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .vuln-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin: 10px 0;
            font-size: 0.9em;
        }
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }
        .badge.critical { background: #e74c3c; color: white; }
        .badge.high { background: #f39c12; color: white; }
        .badge.medium { background: #f1c40f; color: #2c3e50; }
        .badge.low { background: #27ae60; color: white; }
        
        .evidence {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
            overflow-x: auto;
        }
        .recommendations {
            background: #e8f5e8;
            border: 1px solid #27ae60;
            padding: 20px;
            border-radius: 5px;
        }
        .recommendations ul {
            margin: 0;
            padding-left: 20px;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            color: #7f8c8d;
        }
        @media print {
            body { background: white; }
            .container { box-shadow: none; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ report_title }}</h1>
            <div class="subtitle">
                <strong>Assessment Date:</strong> {{ assessment_date }}<br>
                <strong>Generated:</strong> {{ generation_date }}
            </div>
        </div>

        <div class="section">
            <h2>Executive Summary</h2>
            <div class="summary">
                <div class="summary-card">
                    <h3>{{ summary.total_vulnerabilities }}</h3>
                    <p>Total Vulnerabilities</p>
                </div>
                <div class="summary-card severity-critical">
                    <h3>{{ summary.severity_distribution.critical }}</h3>
                    <p>Critical</p>
                </div>
                <div class="summary-card severity-high">
                    <h3>{{ summary.severity_distribution.high }}</h3>
                    <p>High</p>
                </div>
                <div class="summary-card severity-medium">
                    <h3>{{ summary.severity_distribution.medium }}</h3>
                    <p>Medium</p>
                </div>
                <div class="summary-card severity-low">
                    <h3>{{ summary.severity_distribution.low }}</h3>
                    <p>Low</p>
                </div>
            </div>
        </div>

        {% if vulnerabilities %}
        <div class="section">
            <h2>Vulnerabilities</h2>
            {% for vuln in vulnerabilities %}
            <div class="vulnerability {{ vuln.severity }}">
                <div class="vuln-title">{{ vuln.title }}</div>
                <div class="vuln-meta">
                    <div><strong>Host:</strong> {{ vuln.host }}</div>
                    <div><strong>Port:</strong> {{ vuln.port }}</div>
                    <div><strong>Service:</strong> {{ vuln.affected_service }}</div>
                    <div><strong>Severity:</strong> <span class="badge {{ vuln.severity }}">{{ vuln.severity }}</span></div>
                    {% if vuln.cvss_score > 0 %}
                    <div><strong>CVSS Score:</strong> {{ vuln.cvss_score }}</div>
                    {% endif %}
                </div>
                <p><strong>Description:</strong> {{ vuln.description }}</p>
                {% if vuln.evidence %}
                <div class="evidence">{{ vuln.evidence }}</div>
                {% endif %}
                <p><strong>Remediation:</strong> {{ vuln.remediation }}</p>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% if security_issues %}
        <div class="section">
            <h2>Security Issues</h2>
            {% for issue in security_issues %}
            <div class="security-issue">
                <div class="vuln-title">{{ issue.title }}</div>
                <div class="vuln-meta">
                    <div><strong>Host:</strong> {{ issue.host }}</div>
                    <div><strong>Service:</strong> {{ issue.service }}</div>
                    <div><strong>Category:</strong> {{ issue.category }}</div>
                    <div><strong>Risk Level:</strong> <span class="badge {{ issue.risk_level }}">{{ issue.risk_level }}</span></div>
                </div>
                <p><strong>Description:</strong> {{ issue.description }}</p>
                {% if issue.evidence %}
                <div class="evidence">{{ issue.evidence }}</div>
                {% endif %}
                <p><strong>Recommendation:</strong> {{ issue.recommendation }}</p>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% if recommendations %}
        <div class="section">
            <h2>Recommendations</h2>
            <div class="recommendations">
                <ul>
                {% for rec in recommendations %}
                    <li>{{ rec }}</li>
                {% endfor %}
                </ul>
            </div>
        </div>
        {% endif %}

        <div class="footer">
            <p>Generated by Network Security Assessment Framework (NSAF) v1.0.0</p>
            <p>This report contains confidential security information</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(template_path / "report_template.html", "w", encoding="utf-8") as f:
            f.write(main_template)

    def generate_html_report(self, assessment_results: Dict[str, Any], 
                            filename: str = None, 
                            title: str = "Network Security Assessment Report") -> str:
        """
        Generate HTML report from assessment results
        
        Args:
            assessment_results: Results from vulnerability assessment
            filename: Output filename
            title: Report title
            
        Returns:
            Path to generated report file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_assessment_report_{timestamp}.html"
            
        logger.info(f"Generating HTML report: {filename}")
        
        if not JINJA2_AVAILABLE:
            logger.warning("Jinja2 not available, generating basic HTML report")
            return self._generate_basic_html_report(assessment_results, filename, title)
        
        try:
            # Load template
            env = Environment(loader=FileSystemLoader(self.template_dir))
            template = env.get_template("report_template.html")
            
            # Prepare template data
            template_data = {
                'report_title': title,
                'assessment_date': assessment_results.get('summary', {}).get('assessment_date', datetime.now().isoformat()),
                'generation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'summary': assessment_results.get('summary', {}),
                'vulnerabilities': assessment_results.get('vulnerabilities', []),
                'security_issues': assessment_results.get('security_issues', []),
                'recommendations': assessment_results.get('recommendations', [])
            }
            
            # Render template
            html_content = template.render(**template_data)
            
            # Write to file
            report_path = self.reports_dir / filename
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            logger.info(f"HTML report generated successfully: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"Failed to generate HTML report: {e}")
            return self._generate_basic_html_report(assessment_results, filename, title)

    def _generate_basic_html_report(self, assessment_results: Dict[str, Any], 
                                   filename: str, title: str) -> str:
        """Generate basic HTML report without Jinja2"""
        logger.info("Generating basic HTML report")
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }}
                .summary {{ background: #f0f0f0; padding: 20px; margin: 20px 0; }}
                .vulnerability {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; }}
                .critical {{ border-left: 5px solid #red; }}
                .high {{ border-left: 5px solid #orange; }}
                .medium {{ border-left: 5px solid #yellow; }}
                .low {{ border-left: 5px solid #green; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{title}</h1>
                <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            
            <div class="summary">
                <h2>Summary</h2>
                <p>Total Vulnerabilities: {len(assessment_results.get('vulnerabilities', []))}</p>
                <p>Security Issues: {len(assessment_results.get('security_issues', []))}</p>
            </div>
        """
        
        # Add vulnerabilities
        vulnerabilities = assessment_results.get('vulnerabilities', [])
        if vulnerabilities:
            html_content += "<h2>Vulnerabilities</h2>"
            for vuln in vulnerabilities:
                html_content += f"""
                <div class="vulnerability {vuln.severity}">
                    <h3>{vuln.title}</h3>
                    <p><strong>Host:</strong> {vuln.host}:{vuln.port}</p>
                    <p><strong>Severity:</strong> {vuln.severity}</p>
                    <p><strong>Description:</strong> {vuln.description}</p>
                    <p><strong>Remediation:</strong> {vuln.remediation}</p>
                </div>
                """
        
        html_content += "</body></html>"
        
        report_path = self.reports_dir / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return str(report_path)

    def generate_pdf_report(self, assessment_results: Dict[str, Any], 
                           filename: str = None,
                           title: str = "Network Security Assessment Report") -> str:
        """
        Generate PDF report from assessment results
        
        Args:
            assessment_results: Results from vulnerability assessment
            filename: Output filename
            title: Report title
            
        Returns:
            Path to generated report file
        """
        if not REPORTLAB_AVAILABLE:
            logger.error("ReportLab not available, cannot generate PDF report")
            return ""
            
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_assessment_report_{timestamp}.pdf"
            
        logger.info(f"Generating PDF report: {filename}")
        
        try:
            report_path = self.reports_dir / filename
            doc = SimpleDocTemplate(str(report_path), pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Center
            )
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 20))
            
            # Summary
            summary = assessment_results.get('summary', {})
            story.append(Paragraph("Executive Summary", styles['Heading2']))
            
            summary_data = [
                ['Metric', 'Count'],
                ['Total Vulnerabilities', str(summary.get('total_vulnerabilities', 0))],
                ['Critical', str(summary.get('severity_distribution', {}).get('critical', 0))],
                ['High', str(summary.get('severity_distribution', {}).get('high', 0))],
                ['Medium', str(summary.get('severity_distribution', {}).get('medium', 0))],
                ['Low', str(summary.get('severity_distribution', {}).get('low', 0))]
            ]
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 20))
            
            # Vulnerabilities
            vulnerabilities = assessment_results.get('vulnerabilities', [])
            if vulnerabilities:
                story.append(Paragraph("Vulnerabilities", styles['Heading2']))
                
                for vuln in vulnerabilities:
                    story.append(Paragraph(f"<b>{vuln.title}</b>", styles['Heading3']))
                    story.append(Paragraph(f"<b>Host:</b> {vuln.host}:{vuln.port}", styles['Normal']))
                    story.append(Paragraph(f"<b>Severity:</b> {vuln.severity}", styles['Normal']))
                    story.append(Paragraph(f"<b>Description:</b> {vuln.description}", styles['Normal']))
                    story.append(Paragraph(f"<b>Remediation:</b> {vuln.remediation}", styles['Normal']))
                    story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            logger.info(f"PDF report generated successfully: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"Failed to generate PDF report: {e}")
            return ""

    def generate_json_report(self, assessment_results: Dict[str, Any], 
                            filename: str = None) -> str:
        """
        Generate JSON report from assessment results
        
        Args:
            assessment_results: Results from vulnerability assessment
            filename: Output filename
            
        Returns:
            Path to generated report file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_assessment_report_{timestamp}.json"
            
        logger.info(f"Generating JSON report: {filename}")
        
        try:
            # Convert datetime objects to strings for JSON serialization
            json_data = self._prepare_json_data(assessment_results)
            
            report_path = self.reports_dir / filename
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"JSON report generated successfully: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"Failed to generate JSON report: {e}")
            return ""

    def _prepare_json_data(self, data: Any) -> Any:
        """Prepare data for JSON serialization"""
        if isinstance(data, dict):
            return {k: self._prepare_json_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._prepare_json_data(item) for item in data]
        elif isinstance(data, (Vulnerability, SecurityIssue)):
            return data.__dict__
        elif isinstance(data, datetime):
            return data.isoformat()
        elif isinstance(data, set):
            return list(data)
        else:
            return data

    def generate_csv_report(self, assessment_results: Dict[str, Any], 
                           filename: str = None) -> str:
        """
        Generate CSV report from assessment results
        
        Args:
            assessment_results: Results from vulnerability assessment
            filename: Output filename
            
        Returns:
            Path to generated report file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_assessment_report_{timestamp}.csv"
            
        logger.info(f"Generating CSV report: {filename}")
        
        try:
            import csv
            
            report_path = self.reports_dir / filename
            
            with open(report_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow([
                    'Type', 'Title', 'Host', 'Port', 'Severity/Risk', 
                    'Service', 'Description', 'Remediation', 'Timestamp'
                ])
                
                # Write vulnerabilities
                for vuln in assessment_results.get('vulnerabilities', []):
                    writer.writerow([
                        'Vulnerability',
                        vuln.title,
                        vuln.host,
                        vuln.port,
                        vuln.severity,
                        vuln.affected_service,
                        vuln.description,
                        vuln.remediation,
                        vuln.timestamp.isoformat() if hasattr(vuln.timestamp, 'isoformat') else str(vuln.timestamp)
                    ])
                
                # Write security issues
                for issue in assessment_results.get('security_issues', []):
                    writer.writerow([
                        'Security Issue',
                        issue.title,
                        issue.host,
                        '',  # No port for security issues
                        issue.risk_level,
                        issue.service,
                        issue.description,
                        issue.recommendation,
                        issue.timestamp.isoformat() if hasattr(issue.timestamp, 'isoformat') else str(issue.timestamp)
                    ])
            
            logger.info(f"CSV report generated successfully: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"Failed to generate CSV report: {e}")
            return ""

    def generate_all_reports(self, assessment_results: Dict[str, Any], 
                            base_filename: str = None) -> Dict[str, str]:
        """
        Generate all report formats
        
        Args:
            assessment_results: Results from vulnerability assessment
            base_filename: Base filename (without extension)
            
        Returns:
            Dictionary mapping format to file path
        """
        if base_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"security_assessment_report_{timestamp}"
            
        logger.info("Generating all report formats")
        
        report_files = {}
        
        # Generate HTML report
        html_file = self.generate_html_report(assessment_results, f"{base_filename}.html")
        if html_file:
            report_files['html'] = html_file
            
        # Generate PDF report
        pdf_file = self.generate_pdf_report(assessment_results, f"{base_filename}.pdf")
        if pdf_file:
            report_files['pdf'] = pdf_file
            
        # Generate JSON report
        json_file = self.generate_json_report(assessment_results, f"{base_filename}.json")
        if json_file:
            report_files['json'] = json_file
            
        # Generate CSV report
        csv_file = self.generate_csv_report(assessment_results, f"{base_filename}.csv")
        if csv_file:
            report_files['csv'] = csv_file
            
        logger.info(f"Generated {len(report_files)} report files")
        return report_files
