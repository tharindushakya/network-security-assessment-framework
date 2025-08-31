# Security Configuration for NSAF

This document outlines the security configurations and best practices implemented in the Network Security Assessment Framework (NSAF).

## Security Improvements Made

### 1. Jinja2 Template Security (CVE Mitigation)
- **Issue**: Jinja2 autoescape was disabled by default, leading to potential XSS vulnerabilities
- **Fix**: Enabled `autoescape=True` in all Jinja2 Environment configurations
- **Impact**: Prevents XSS attacks in generated HTML reports
- **Location**: `nsaf/core/report_generator.py`

### 2. SSL Certificate Verification
- **Issue**: SSL certificate verification was disabled (`verify=False`) in HTTP requests
- **Fix**: 
  - Added `verify_ssl` parameter to VulnerabilityScanner (default: True)
  - Added warning logs when SSL verification is disabled
  - Enabled secure SSL verification by default
- **Impact**: Prevents man-in-the-middle attacks and ensures secure communications
- **Location**: `nsaf/core/vulnerability_scanner.py`

### 3. Improved Error Handling
- **Issue**: Generic `try/except/pass` blocks masked potential security issues
- **Fix**: 
  - Replaced with specific exception handling
  - Added proper logging for debugging
  - Maintained security through explicit error types
- **Impact**: Better error visibility and security monitoring
- **Locations**: `nsaf/core/scanner.py`, `nsaf/core/vulnerability_scanner.py`

### 4. Subprocess Security
- **Issue**: Bandit flagged subprocess usage as potential security risk
- **Fix**: 
  - Used secure subprocess patterns with explicit argument lists
  - Added proper timeout handling
  - Implemented specific exception handling
- **Impact**: Prevents command injection and improves process security
- **Location**: `nsaf/core/scanner.py`

## Security Configuration Options

### SSL Certificate Verification
```python
# Secure (default)
scanner = VulnerabilityScanner(verify_ssl=True)

# For testing environments only (with warnings)
scanner = VulnerabilityScanner(verify_ssl=False)
```

### Template Security
```python
# Secure template rendering with autoescape enabled
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=True  # Prevents XSS vulnerabilities
)
```

## Security Best Practices

### 1. Network Scanning Ethics
- Always obtain proper authorization before scanning networks
- Respect rate limits and target system resources
- Use appropriate scan intensities for the environment
- Document and report findings responsibly

### 2. Data Handling
- Scan results may contain sensitive information
- Store results securely with appropriate access controls
- Consider encryption for sensitive scan data
- Implement data retention policies

### 3. Deployment Security
- Use HTTPS for any web interfaces
- Implement proper authentication and authorization
- Keep dependencies updated
- Monitor for security vulnerabilities
- Use secure coding practices

### 4. Logging and Monitoring
- Enable appropriate logging levels for security monitoring
- Monitor for unusual scan patterns or errors
- Implement alerting for security-related events
- Regular security audits and reviews

## Compliance Considerations

### GDPR/Privacy
- Be aware of data protection regulations when scanning
- Implement data minimization principles
- Provide clear privacy notices for scan activities
- Allow for data subject rights where applicable

### Industry Standards
- Follow NIST Cybersecurity Framework guidelines
- Implement OWASP security best practices
- Consider ISO 27001 security management practices
- Adhere to responsible disclosure practices

## Security Reporting

### Vulnerability Disclosure
- Use the GitHub Security Advisory feature for sensitive issues
- Follow responsible disclosure timelines
- Provide clear reproduction steps and impact assessment
- Coordinate with maintainers for security patches

### Security Contact
- Security issues: Use GitHub Security Advisory
- General security questions: Create a GitHub issue with security label
- Critical vulnerabilities: Email maintainer privately (see SECURITY.md)

## Regular Security Tasks

### Monthly
- Review and update dependencies
- Check for new security advisories
- Update security configurations as needed

### Quarterly
- Conduct security code reviews
- Update threat models
- Review access controls and permissions

### Annually
- Comprehensive security audit
- Penetration testing (authorized)
- Security training and awareness updates
- Review and update security policies

## Security Tools Integration

### Static Analysis
- Bandit for Python security scanning
- CodeQL for comprehensive code analysis
- Safety for dependency vulnerability scanning

### Dynamic Analysis
- Regular automated security testing
- Integration with CI/CD security pipelines
- Continuous monitoring for security issues

## Security Metrics

### Key Performance Indicators
- Number of security vulnerabilities resolved
- Time to fix security issues
- Security scan coverage
- Dependency update frequency

### Monitoring
- Failed authentication attempts
- Unusual scan patterns
- Error rates and anomalies
- Security event correlation
