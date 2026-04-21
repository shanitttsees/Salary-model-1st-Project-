"""
Report Generation Module
Generates HTML and text reports for vulnerability scan results.
"""

from datetime import datetime
from typing import Dict, List
import os


class ReportGenerator:
    """Generates vulnerability scan reports in various formats."""
    
    def __init__(self, output_dir: str = 'reports'):
        """
        Initialize the report generator.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_html_report(self, scan_data: Dict) -> str:
        """
        Generate an HTML report.
        
        Args:
            scan_data: Scan results dictionary
            
        Returns:
            Path to generated report
        """
        html_content = self._build_html(scan_data)
        
        filename = f"vulnerability_report_{self.timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return filepath
    
    def generate_text_report(self, scan_data: Dict) -> str:
        """
        Generate a text report.
        
        Args:
            scan_data: Scan results dictionary
            
        Returns:
            Path to generated report
        """
        text_content = self._build_text(scan_data)
        
        filename = f"vulnerability_report_{self.timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(text_content)
        
        return filepath
    
    def _build_html(self, scan_data: Dict) -> str:
        """Build HTML report content."""
        network_info = scan_data.get('network_info', {})
        devices = scan_data.get('devices_found', [])
        vulnerabilities = scan_data.get('vulnerabilities', [])
        severity_summary = scan_data.get('severity_summary', {})
        recommendations = scan_data.get('remediation_advice', [])
        
        # Color coding for severity
        severity_colors = {
            'CRITICAL': '#d32f2f',
            'HIGH': '#f57c00',
            'MEDIUM': '#fbc02d',
            'LOW': '#388e3c'
        }
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Home Network Vulnerability Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1976d2;
            border-bottom: 3px solid #1976d2;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #424242;
            margin-top: 30px;
            border-left: 4px solid #1976d2;
            padding-left: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .summary-card {{
            padding: 20px;
            background-color: #f9f9f9;
            border-left: 4px solid #ccc;
            border-radius: 4px;
        }}
        .severity-critical {{ border-left-color: #d32f2f; }}
        .severity-high {{ border-left-color: #f57c00; }}
        .severity-medium {{ border-left-color: #fbc02d; }}
        .severity-low {{ border-left-color: #388e3c; }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #424242;
        }}
        .summary-card .count {{
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th {{
            background-color: #1976d2;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .severity-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            color: white;
            font-weight: bold;
            font-size: 12px;
        }}
        .critical {{ background-color: #d32f2f; }}
        .high {{ background-color: #f57c00; }}
        .medium {{ background-color: #fbc02d; color: #000; }}
        .low {{ background-color: #388e3c; }}
        .info-box {{
            background-color: #e3f2fd;
            border-left: 4px solid #1976d2;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .warning-box {{
            background-color: #fff3e0;
            border-left: 4px solid #f57c00;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .recommendation {{
            background-color: #f1f8e9;
            border-left: 4px solid #388e3c;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
        }}
        .risk-level {{
            padding: 10px;
            border-radius: 4px;
            font-weight: bold;
            text-align: center;
        }}
        .risk-critical {{
            background-color: #ffcdd2;
            color: #b71c1c;
        }}
        .risk-high {{
            background-color: #ffe0b2;
            color: #e65100;
        }}
        .risk-medium {{
            background-color: #fff9c4;
            color: #f57f17;
        }}
        .risk-low {{
            background-color: #c8e6c9;
            color: #2e7d32;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Home Network Vulnerability Scan Report</h1>
        
        <div class="info-box">
            <strong>Scan Information:</strong><br>
            Network: {network_info.get('network_range', 'N/A')}<br>
            Local IP: {network_info.get('local_ip', 'N/A')}<br>
            Scan Time: {network_info.get('scan_time', 'N/A')}
        </div>
        
        <h2>📊 Executive Summary</h2>
        <div class="summary">
            <div class="summary-card severity-critical">
                <h3>🔴 Critical</h3>
                <div class="count">{severity_summary.get('CRITICAL', 0)}</div>
            </div>
            <div class="summary-card severity-high">
                <h3>🟠 High</h3>
                <div class="count">{severity_summary.get('HIGH', 0)}</div>
            </div>
            <div class="summary-card severity-medium">
                <h3>🟡 Medium</h3>
                <div class="count">{severity_summary.get('MEDIUM', 0)}</div>
            </div>
            <div class="summary-card severity-low">
                <h3>🟢 Low</h3>
                <div class="count">{severity_summary.get('LOW', 0)}</div>
            </div>
        </div>
        
        <h2>🖥️ Devices Found</h2>
        {self._build_devices_table_html(devices)}
        
        <h2>⚠️ Vulnerabilities Detected</h2>
        {self._build_vulnerabilities_table_html(vulnerabilities, severity_colors)}
        
        <h2>🔧 Remediation Recommendations</h2>
        {self._build_recommendations_html(recommendations)}
        
        <h2>📋 Risk Assessment</h2>
        {self._build_risk_assessment_html(severity_summary)}
        
        <div class="footer">
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Home Network Vulnerability Scanner</p>
        </div>
    </div>
</body>
</html>"""
        return html
    
    def _build_devices_table_html(self, devices: List[Dict]) -> str:
        """Build HTML table for devices."""
        if not devices:
            return "<p>No devices found on the network.</p>"
        
        html = "<table><thead><tr><th>Host IP</th><th>Open Ports</th><th>Services</th></tr></thead><tbody>"
        
        for device in devices:
            ports = ', '.join(map(str, device.get('open_ports', [])))
            services = ', '.join(device.get('services', []))
            html += f"<tr><td>{device['host']}</td><td>{ports}</td><td>{services}</td></tr>"
        
        html += "</tbody></table>"
        return html
    
    def _build_vulnerabilities_table_html(self, vulnerabilities: List[Dict], colors: Dict) -> str:
        """Build HTML table for vulnerabilities."""
        if not vulnerabilities:
            return "<div class='info-box'>✅ No vulnerabilities detected!</div>"
        
        html = "<table><thead><tr><th>Host</th><th>Port</th><th>Service</th><th>Vulnerability</th><th>Severity</th><th>Description</th></tr></thead><tbody>"
        
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'LOW').lower()
            html += f"""<tr>
                <td>{vuln['host']}</td>
                <td>{vuln['port']}</td>
                <td>{vuln['service']}</td>
                <td>{vuln['vulnerability']}</td>
                <td><span class='severity-badge {severity}'>{vuln['severity']}</span></td>
                <td>{vuln['description']}</td>
            </tr>"""
        
        html += "</tbody></table>"
        return html
    
    def _build_recommendations_html(self, recommendations: List[Dict]) -> str:
        """Build HTML for recommendations."""
        if not recommendations:
            return "<div class='info-box'>✅ No recommendations at this time.</div>"
        
        html = ""
        for rec in recommendations:
            html += f"""<div class="recommendation">
                <strong>{rec['vulnerability']} (Port {rec['port']} on {rec['host']})</strong><br>
                ✓ {rec['recommendation']}
            </div>"""
        
        return html
    
    def _build_risk_assessment_html(self, severity_summary: Dict) -> str:
        """Build risk assessment section."""
        total = sum(severity_summary.values())
        
        if severity_summary.get('CRITICAL', 0) > 0:
            risk_level = "critical"
            risk_text = "🔴 CRITICAL - Immediate action required"
        elif severity_summary.get('HIGH', 0) > 0:
            risk_level = "high"
            risk_text = "🟠 HIGH - Urgent attention needed"
        elif severity_summary.get('MEDIUM', 0) > 0:
            risk_level = "medium"
            risk_text = "🟡 MEDIUM - Should be addressed soon"
        else:
            risk_level = "low"
            risk_text = "🟢 LOW - Minimal risk detected"
        
        return f"""<div class="risk-level risk-{risk_level}">
            {risk_text}
        </div>
        <p>Total Issues Found: {total}</p>"""
    
    def _build_text(self, scan_data: Dict) -> str:
        """Build text report content."""
        network_info = scan_data.get('network_info', {})
        devices = scan_data.get('devices_found', [])
        vulnerabilities = scan_data.get('vulnerabilities', [])
        severity_summary = scan_data.get('severity_summary', {})
        recommendations = scan_data.get('remediation_advice', [])
        
        text = f"""
╔════════════════════════════════════════════════════════════════════╗
║   HOME NETWORK VULNERABILITY SCAN REPORT                          ║
╚════════════════════════════════════════════════════════════════════╝

SCAN INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Network Range:    {network_info.get('network_range', 'N/A')}
Local IP:         {network_info.get('local_ip', 'N/A')}
Hostname:         {network_info.get('hostname', 'N/A')}
Scan Time:        {network_info.get('scan_time', 'N/A')}

EXECUTIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Critical Issues:  {severity_summary.get('CRITICAL', 0)}
High Issues:      {severity_summary.get('HIGH', 0)}
Medium Issues:    {severity_summary.get('MEDIUM', 0)}
Low Issues:       {severity_summary.get('LOW', 0)}
Total Issues:     {sum(severity_summary.values())}

DEVICES FOUND ({len(devices)})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        if devices:
            for device in devices:
                text += f"\nHost: {device['host']}\n"
                text += f"  Open Ports: {', '.join(map(str, device.get('open_ports', [])))}\n"
                text += f"  Services:   {', '.join(device.get('services', []))}\n"
        else:
            text += "\nNo devices found on the network.\n"
        
        text += f"""
VULNERABILITIES DETECTED ({len(vulnerabilities)})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        if vulnerabilities:
            for i, vuln in enumerate(vulnerabilities, 1):
                text += f"\n{i}. [{vuln['severity']}] {vuln['vulnerability']}\n"
                text += f"   Host:        {vuln['host']}\n"
                text += f"   Port:        {vuln['port']}\n"
                text += f"   Service:     {vuln['service']}\n"
                text += f"   Description: {vuln['description']}\n"
        else:
            text += "\n✅ No vulnerabilities detected!\n"
        
        text += f"""
REMEDIATION RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                text += f"\n{i}. {rec['vulnerability']} (Port {rec['port']} on {rec['host']})\n"
                text += f"   ✓ {rec['recommendation']}\n"
        else:
            text += "\n✅ No recommendations at this time.\n"
        
        # Determine overall risk
        if severity_summary.get('CRITICAL', 0) > 0:
            risk_text = "🔴 CRITICAL - Immediate action required"
        elif severity_summary.get('HIGH', 0) > 0:
            risk_text = "🟠 HIGH - Urgent attention needed"
        elif severity_summary.get('MEDIUM', 0) > 0:
            risk_text = "🟡 MEDIUM - Should be addressed soon"
        else:
            risk_text = "🟢 LOW - Minimal risk detected"
        
        text += f"""
OVERALL RISK ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{risk_text}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
╚════════════════════════════════════════════════════════════════════╝
"""
        return text
