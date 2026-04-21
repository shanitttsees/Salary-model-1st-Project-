# Home Network Vulnerability Scanner

A comprehensive Python-based network vulnerability scanner designed to identify security risks on your home or small office network.

## Features

🛡️ **Network Discovery**
- Automatically detects active devices on your network
- Scans for open ports and running services
- Comprehensive port mapping for common services

🔍 **Vulnerability Detection**
- Identifies exposed services (Telnet, FTP, SMB, etc.)
- Detects unencrypted protocols (HTTP, FTP, Telnet)
- Flags improperly exposed databases (MySQL, MongoDB, Redis)
- Checks for weak authentication protocols

📊 **Detailed Reporting**
- HTML reports with visual severity indicators
- Plain text reports for easy reading
- JSON export for programmatic access
- Severity classification (Critical, High, Medium, Low)

🔧 **Remediation Guidance**
- Actionable recommendations for each vulnerability
- Best practices for securing network services
- Quick reference guide for hardening measures

## Project Structure

```
falcon-s-1st-project/
├── vulnerability_scanner.py    # Main application entry point
├── network_scanner.py          # Core scanning functionality
├── report_generator.py         # Report generation engine
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── reports/                    # Generated reports directory
    ├── vulnerability_report_YYYYMMDD_HHMMSS.html
    └── vulnerability_report_YYYYMMDD_HHMMSS.txt
```

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/home-network-vuln-scanner.git
cd home-network-vuln-scanner
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### Basic Scan (Auto-detect Network)
```bash
python vulnerability_scanner.py
```

### Scan Specific Network
```bash
python vulnerability_scanner.py --network 192.168.1.0/24
```

### Generate HTML Report Only
```bash
python vulnerability_scanner.py --html
```

### Generate Text Report Only
```bash
python vulnerability_scanner.py --text
```

### Generate Both Reports
```bash
python vulnerability_scanner.py --both
```

### Generate All Formats (HTML, Text, and JSON)
```bash
python vulnerability_scanner.py --both --json
```

### Custom Network with Reports
```bash
python vulnerability_scanner.py --network 10.0.0.0/24 --both --json
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `--network NETWORK` | Specify network range (e.g., 192.168.1.0/24) |
| `--html` | Generate HTML report |
| `--text` | Generate text report |
| `--both` | Generate both HTML and text reports |
| `--json` | Save results as JSON file |
| `--help` | Show help message |

## Output

### Report Location
All reports are generated in the `reports/` directory with timestamps:
- `vulnerability_report_20240421_143022.html` - Interactive HTML report
- `vulnerability_report_20240421_143022.txt` - Text report
- `scan_results.json` - Raw data (if --json flag used)

### Report Contents

#### Executive Summary
- Quick overview of vulnerability counts by severity
- Network information and scan timestamp

#### Devices Found
- List of active devices on the network
- Open ports on each device
- Identified services

#### Vulnerabilities Detected
- Detailed list of security issues
- Severity classification
- Service descriptions
- Remediation recommendations

#### Risk Assessment
- Overall risk level (Critical/High/Medium/Low)
- Actionable next steps

## Vulnerability Categories

### Critical Issues
- Exposed databases (MongoDB, Redis, MySQL)
- File sharing without authentication

### High Severity
- Telnet (unencrypted remote access)
- FTP (unencrypted file transfer)
- SMB (ransomware risk)

### Medium Severity
- HTTP (unencrypted web traffic)
- SSH (ensure proper authentication)

### Low Severity
- Non-critical services or protocols

## Remediation Recommendations

### For Telnet Services
Use SSH instead for secure remote access.

### For FTP Services
Use SFTP, SCP, or other secure file transfer methods.

### For HTTP Services
Enable HTTPS/TLS encryption for all web traffic.

### For Exposed Databases
- Use firewall rules to restrict access
- Implement authentication
- Consider VPN for remote access

### For SMB Services
- Restrict to internal network only
- Use Windows Defender Firewall
- Keep systems patched

## Example Output

```
======================================================================
🛡️  HOME NETWORK VULNERABILITY SCANNER
======================================================================

📍 Network Information:
   Hostname:      DESKTOP-ABC123
   Local IP:      192.168.1.100
   Network Range: 192.168.1.0/24

🔍 Scanning network for active devices...
✓ Found 3 active device(s)

🔎 Analyzing for vulnerabilities...
✓ Found 2 vulnerability(ies)

📊 Vulnerability Summary:
   🔴 Critical: 0
   🟠 High:     1
   🟡 Medium:   1
   🟢 Low:      0

======================================================================
SCAN SUMMARY
======================================================================

📊 Results:
   Devices Found:     3
   Vulnerabilities:   2
   Critical Issues:   0
   High Issues:       1
   Medium Issues:     1
   Low Issues:        0

   🟠 RISK LEVEL: HIGH

======================================================================
```

## System Requirements

- Python 3.7 or higher
- Windows, macOS, or Linux
- Administrative/sudo access (for network scanning)
- Network connectivity

## Technical Details

### Network Scanning
- Uses socket programming for port scanning
- Threaded scanning for performance
- Automatic network detection via ICMP ping

### Vulnerability Detection
- Pattern matching against known vulnerability rules
- Service identification via port numbers
- Severity scoring algorithm

### Report Generation
- HTML reports with CSS styling
- Responsive design for mobile viewing
- Color-coded severity indicators

## Security Notes

⚠️ **Important:**
- Only scan networks you own or have permission to scan
- Unauthorized network scanning may be illegal
- Use responsibly in compliance with local laws
- Results are only as accurate as the network environment

## Limitations

- Scans common ports only (use custom port ranges for full scan)
- Does not perform deep vulnerability analysis
- Cannot detect zero-day vulnerabilities
- Requires network connectivity to target devices

## Future Enhancements

- [ ] Custom port range scanning
- [ ] Service version detection
- [ ] Web UI dashboard
- [ ] Scheduled scanning
- [ ] Email report delivery
- [ ] Integration with Slack notifications
- [ ] Database storage for historical reports
- [ ] Machine learning-based anomaly detection

## Contributing

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions:
1. Check existing issues on GitHub
2. Create a new issue with detailed description
3. Include sample output and system information

## Acknowledgments

- Python socket programming documentation
- OWASP security guidelines
- Community feedback and contributions

---

**Happy scanning! Stay secure! 🔒**
