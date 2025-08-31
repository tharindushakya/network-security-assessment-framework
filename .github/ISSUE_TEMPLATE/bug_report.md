---
name: 🐛 Bug Report
about: Report a bug or unexpected behavior in NSAF
title: '[BUG] '
labels: 'bug, needs-triage'
assignees: ''

---

## 🐛 Bug Description
**Provide a clear and concise description of the bug:**
<!-- Describe what went wrong -->

## 🔄 Steps to Reproduce
**Please provide detailed steps to reproduce the issue:**
1. Run command/scan: `nsaf_cli.py ...`
2. Target network/host: `...`
3. Configuration used: `...`
4. Error occurs at: `...`

## ✅ Expected Behavior
**What should have happened instead?**
<!-- Describe the expected outcome -->

## ❌ Actual Behavior
**What actually happened?**
<!-- Include error messages, unexpected outputs, etc. -->

## 📋 Environment Information
**System Details:**
- **OS**: [e.g., Windows 11, Ubuntu 22.04, macOS 14.0]
- **Python Version**: [e.g., 3.11.5]
- **NSAF Version**: [e.g., 1.0.0]
- **Installation Method**: [pip, git clone, etc.]

**Network Environment:**
- **Target Network**: [e.g., local LAN, VPN, cloud environment]
- **Network Restrictions**: [firewalls, proxies, etc.]
- **Scan Permissions**: [authorized scan, own network, etc.]

## 📊 Scan Configuration
**Command/Configuration Used:**
```bash
# Paste the exact command or configuration that caused the issue
nsaf_cli.py scan --target ... --ports ...
```

**Configuration Files (if applicable):**
```yaml
# Include relevant configuration snippets
```

## 📝 Log Output
**Error Messages/Logs:**
```
Paste relevant error messages, stack traces, or log output here
```

**Verbose Output (if available):**
```
Include --verbose or debug output if available
```

## 🔍 Additional Context
**Screenshots/Output Files:**
<!-- Attach any relevant screenshots, report files, or output samples -->

**Related Issues:**
<!-- Link to any related issues or discussions -->

**Possible Cause:**
<!-- If you have an idea about what might be causing the issue -->

**Workaround (if any):**
<!-- Describe any temporary workaround you've found -->

## 🛡️ Security Considerations
**Is this a security-related bug?**
- [ ] This bug could have security implications
- [ ] This bug affects vulnerability detection accuracy
- [ ] This bug could expose sensitive information

**If security-related, please also email the maintainer privately**

## ✅ Checklist
Before submitting, please confirm:
- [ ] I have searched existing issues for duplicates
- [ ] I have provided all required environment information
- [ ] I have included steps to reproduce the issue
- [ ] I have the necessary permissions to scan the target network
- [ ] I have reviewed the documentation and this isn't expected behavior
- [ ] I have included relevant log output or error messages
