---
name: ⚡ Performance Issue
about: Report performance problems or optimization suggestions
title: '[PERFORMANCE] '
labels: 'performance, optimization'
assignees: ''

---

## ⚡ Performance Issue Overview
**What performance problem are you experiencing?**
<!-- Describe the performance issue clearly -->

## 📊 Performance Metrics
**Quantify the performance issue:**

### Timing Information
- **Scan Duration**: [e.g., 45 minutes for /24 network]
- **Expected Duration**: [e.g., should take ~10 minutes]
- **Comparison**: [X times slower than expected]

### Resource Usage
- **CPU Usage**: [e.g., 100% CPU usage throughout scan]
- **Memory Usage**: [e.g., 4GB RAM, growing continuously]
- **Network Bandwidth**: [e.g., minimal network utilization]
- **Disk I/O**: [heavy disk writing, etc.]

## 🎯 Scan Configuration
**Details about the scan that shows poor performance:**

### Target Information
- **Target Type**: [single host, subnet, IP range]
- **Target Size**: [e.g., /24 network = 254 hosts]
- **Network Environment**: [LAN, WAN, VPN, etc.]

### Scan Parameters
```bash
# Exact command used
nsaf_cli.py scan --target 192.168.1.0/24 --ports 1-65535 --threads 100
```

### Configuration
```yaml
# Any custom configuration used
scan_config:
  timeout: 5
  max_threads: 100
  scan_type: tcp_connect
```

## 🖥️ System Environment
**System specifications where performance issue occurs:**

### Hardware
- **CPU**: [e.g., Intel i7-12700K, 8 cores]
- **RAM**: [e.g., 16GB DDR4]
- **Storage**: [SSD/HDD, available space]
- **Network**: [Ethernet speed, WiFi, etc.]

### Software
- **OS**: [e.g., Windows 11, Ubuntu 22.04]
- **Python Version**: [e.g., 3.11.5]
- **NSAF Version**: [e.g., 1.0.0]

## 🔍 Performance Analysis
**Additional details about the performance issue:**

### When Does It Occur?
- [ ] During host discovery
- [ ] During port scanning
- [ ] During service detection
- [ ] During vulnerability assessment
- [ ] During report generation
- [ ] Throughout entire scan

### Performance Pattern
- [ ] Performance degrades over time
- [ ] Consistent slow performance
- [ ] Intermittent performance spikes
- [ ] Memory leaks observed
- [ ] CPU usage spikes
- [ ] Network bottleneck

### Comparison Data
**How does performance compare?**
- **Similar tools**: [nmap takes X minutes for same scan]
- **Different targets**: [smaller networks scan fine]
- **Different configurations**: [fewer threads = faster/slower]

## 📈 Expected Performance
**What performance would you expect?**
- **Target scan time**: [e.g., /24 network should complete in ~10 minutes]
- **Resource usage**: [should use moderate CPU/memory]
- **Scaling behavior**: [should scale linearly with target size]

## 🔧 Optimization Suggestions
**Do you have ideas for improving performance?**

### Potential Solutions
- [ ] Better multithreading implementation
- [ ] More efficient data structures
- [ ] Caching mechanisms
- [ ] Reduced memory footprint
- [ ] Optimized algorithms
- [ ] Batch processing

### Configuration Optimizations
<!-- Suggest configuration changes that might help -->

## 🧪 Testing Details
**Information to help reproduce and test:**

### Reproducible Test Case
```bash
# Minimal command that demonstrates the issue
nsaf_cli.py scan --target [small-test-range] --ports 1-1000
```

### Performance Baseline
- **Minimum acceptable performance**: [X seconds/minutes]
- **Comparison benchmark**: [other tools, previous versions]

### Profiling Data
**If you have profiling information:**
```
# Include any profiling output, timing data, or performance metrics
```

## 📊 Impact Assessment
**How does this performance issue affect usage?**

### Severity
- [ ] **Critical** - Makes NSAF unusable for intended purpose
- [ ] **High** - Significantly impacts productivity
- [ ] **Medium** - Noticeable but workable
- [ ] **Low** - Minor performance concern

### Use Case Impact
- [ ] Affects enterprise network scanning
- [ ] Impacts penetration testing workflows
- [ ] Slows down security assessments
- [ ] Makes tool impractical for large networks

## 🔄 Workarounds
**Any temporary solutions you've found:**
<!-- Describe configuration changes, alternative approaches, etc. -->

## 📚 Additional Context
**Any other relevant information:**
- Network topology details
- Firewall/security appliance interference
- Concurrent system load
- Previous versions that performed better

## ✅ Checklist
Before submitting, please confirm:
- [ ] I have provided specific performance metrics
- [ ] I have included system specifications
- [ ] I have provided the exact scan configuration
- [ ] I have compared with expected performance
- [ ] I have checked for system resource constraints
- [ ] I have tested with different configurations
- [ ] I have considered network environment factors
