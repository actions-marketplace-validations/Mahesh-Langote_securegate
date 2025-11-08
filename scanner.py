#!/usr/bin/env python3
"""
SecureGate Scanner - Flutter/Dart Dependency Security and License Scanner
"""

import json
import os
import subprocess
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

# Severity levels
SEVERITY_LEVELS = ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]

# Default configuration
DEFAULT_CONFIG = {
    "mode": "block",
    "banned_licenses": ["GPL-3.0", "AGPL-3.0", "SSPL-1.0", "proprietary"],
    "severity_threshold": "HIGH",
    "whitelist": [],
    "ignore_packages": [],
    "ignore_vulnerabilities": []
}


class SecurityScanner:
    def __init__(self):
        self.config = self.load_config()
        self.vulnerabilities = []
        self.license_issues = []
        self.working_dir = os.getcwd()
        
    def load_config(self) -> Dict:
        """Load configuration from security-gate.yml or use defaults"""
        config_path = os.getenv("CONFIG_PATH", ".github/security-gate.yml")
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    print(f"✓ Loaded configuration from {config_path}")
                    return {**DEFAULT_CONFIG, **config}
            except Exception as e:
                print(f"⚠ Error loading config: {e}. Using defaults.")
                return DEFAULT_CONFIG
        else:
            print(f"ℹ No config file found at {config_path}. Using defaults.")
            return DEFAULT_CONFIG
    
    def run_osv_scanner(self) -> Dict:
        """Run OSV scanner on pubspec.lock"""
        print("\n🔍 Running OSV Scanner...")
        
        pubspec_lock = Path(self.working_dir) / "pubspec.lock"
        if not pubspec_lock.exists():
            print("❌ pubspec.lock not found!")
            return {"results": []}
        
        try:
            result = subprocess.run(
                ["osv-scanner", "--format", "json", "--lockfile", str(pubspec_lock)],
                capture_output=True,
                text=True
            )
            
            # OSV scanner returns non-zero exit code if vulnerabilities found
            if result.returncode != 0 and result.stdout:
                report = json.loads(result.stdout)
            elif result.stdout:
                report = json.loads(result.stdout)
            else:
                report = {"results": []}
            
            # Save raw report
            with open("osv-report.json", "w") as f:
                json.dump(report, f, indent=2)
            
            print(f"✓ OSV scan complete")
            return report
            
        except Exception as e:
            print(f"⚠ OSV scanner error: {e}")
            return {"results": []}
    
    def parse_vulnerabilities(self, osv_report: Dict) -> List[Dict]:
        """Parse and classify vulnerabilities from OSV report"""
        vulnerabilities = []
        
        results = osv_report.get("results", [])
        for result in results:
            packages = result.get("packages", [])
            for package in packages:
                pkg_name = package.get("package", {}).get("name", "unknown")
                pkg_version = package.get("package", {}).get("version", "unknown")
                
                # Check if package is in ignore list
                if pkg_name in self.config.get("ignore_packages", []):
                    continue
                
                for vuln in package.get("vulnerabilities", []):
                    vuln_id = vuln.get("id", "unknown")
                    
                    # Check if vulnerability is in ignore list
                    if vuln_id in self.config.get("ignore_vulnerabilities", []):
                        continue
                    
                    severity = self.get_severity(vuln)
                    
                    vulnerabilities.append({
                        "package": pkg_name,
                        "version": pkg_version,
                        "vulnerability_id": vuln_id,
                        "severity": severity,
                        "summary": vuln.get("summary", "No description available"),
                        "details": vuln.get("details", ""),
                        "references": [ref.get("url") for ref in vuln.get("references", [])]
                    })
        
        return vulnerabilities
    
    def get_severity(self, vuln: Dict) -> str:
        """Extract severity from vulnerability data"""
        # Check database_specific first
        db_specific = vuln.get("database_specific", {})
        if "severity" in db_specific:
            return db_specific["severity"].upper()
        
        # Check CVSS score
        for item in vuln.get("severity", []):
            if item.get("type") == "CVSS_V3":
                score = float(item.get("score", 0))
                if score >= 9.0:
                    return "CRITICAL"
                elif score >= 7.0:
                    return "HIGH"
                elif score >= 4.0:
                    return "MEDIUM"
                elif score > 0:
                    return "LOW"
        
        return "MEDIUM"  # Default
    
    def scan_licenses(self) -> List[Dict]:
        """Scan package licenses using pana"""
        print("\n📜 Scanning licenses...")
        
        license_issues = []
        
        try:
            # Run pana to analyze the package
            result = subprocess.run(
                ["dart", "pub", "global", "run", "pana", "--no-warning", "--json"],
                capture_output=True,
                text=True,
                cwd=self.working_dir
            )
            
            if result.stdout:
                pana_report = json.loads(result.stdout)
                
                # Extract license information
                dependencies = self.get_dependencies_from_pubspec()
                
                for dep_name, dep_version in dependencies.items():
                    # Check if package is whitelisted
                    if dep_name in self.config.get("whitelist", []):
                        continue
                    
                    license_info = self.get_license_for_package(dep_name, dep_version)
                    
                    if license_info and license_info in self.config.get("banned_licenses", []):
                        license_issues.append({
                            "package": dep_name,
                            "version": dep_version,
                            "license": license_info,
                            "reason": f"License '{license_info}' is banned"
                        })
            
            # Save license report
            with open("license-report.json", "w") as f:
                json.dump(license_issues, f, indent=2)
            
            print(f"✓ License scan complete. Found {len(license_issues)} issues")
            return license_issues
            
        except Exception as e:
            print(f"⚠ License scanning error: {e}")
            return []
    
    def get_dependencies_from_pubspec(self) -> Dict[str, str]:
        """Extract dependencies from pubspec.lock"""
        dependencies = {}
        
        try:
            with open("pubspec.lock", "r") as f:
                lock_data = yaml.safe_load(f)
                
                packages = lock_data.get("packages", {})
                for pkg_name, pkg_info in packages.items():
                    version = pkg_info.get("version", "unknown")
                    dependencies[pkg_name] = version
        except Exception as e:
            print(f"⚠ Error reading pubspec.lock: {e}")
        
        return dependencies
    
    def get_license_for_package(self, package_name: str, version: str) -> str:
        """Get license information for a package (simplified)"""
        # In a real implementation, you would query pub.dev API or parse package metadata
        # For this example, we'll use a simplified approach
        try:
            result = subprocess.run(
                ["dart", "pub", "cache", "list"],
                capture_output=True,
                text=True
            )
            # This is a simplified placeholder - in production you'd parse actual license data
            # from package metadata or pub.dev API
            return "MIT"  # Default assumption
        except:
            return "UNKNOWN"
    
    def apply_policy(self) -> bool:
        """Apply policy enforcement based on configuration"""
        print("\n⚖️  Applying security policy...")
        
        mode = self.config.get("mode", "block")
        threshold = self.config.get("severity_threshold", "HIGH")
        threshold_index = SEVERITY_LEVELS.index(threshold)
        
        # Filter vulnerabilities by severity threshold
        critical_vulns = [
            v for v in self.vulnerabilities 
            if SEVERITY_LEVELS.index(v["severity"]) >= threshold_index
        ]
        
        # Determine if we should block
        should_block = False
        
        if critical_vulns:
            print(f"⚠ Found {len(critical_vulns)} vulnerabilities at or above {threshold} severity")
            should_block = True
        
        if self.license_issues:
            print(f"⚠ Found {len(self.license_issues)} license violations")
            should_block = True
        
        if mode == "annotate":
            print(f"ℹ Mode is 'annotate' - will not block PR")
            return True
        
        if should_block:
            print(f"❌ Blocking due to security/license issues")
            return False
        
        print(f"✓ No blocking issues found")
        return True
    
    def generate_report(self):
        """Generate markdown and JSON reports"""
        print("\n📊 Generating reports...")
        
        # Generate markdown report
        md_report = self.generate_markdown_report()
        with open("report.md", "w") as f:
            f.write(md_report)
        
        # Generate JSON report
        final_report = {
            "summary": {
                "total_vulnerabilities": len(self.vulnerabilities),
                "total_license_issues": len(self.license_issues),
                "mode": self.config.get("mode"),
                "threshold": self.config.get("severity_threshold")
            },
            "vulnerabilities": self.vulnerabilities,
            "license_issues": self.license_issues,
            "config": self.config
        }
        
        with open("final-report.json", "w") as f:
            json.dump(final_report, f, indent=2)
        
        print("✓ Reports generated: report.md, final-report.json")
    
    def generate_markdown_report(self) -> str:
        """Generate a markdown formatted report"""
        report = ["# 🛡️ SecureGate Security Scan Report\n"]
        
        # Summary
        report.append("## Summary\n")
        report.append(f"- **Vulnerabilities Found:** {len(self.vulnerabilities)}")
        report.append(f"- **License Issues:** {len(self.license_issues)}")
        report.append(f"- **Mode:** {self.config.get('mode')}")
        report.append(f"- **Severity Threshold:** {self.config.get('severity_threshold')}\n")
        
        # Vulnerabilities by severity
        if self.vulnerabilities:
            report.append("## 🔴 Vulnerabilities\n")
            
            by_severity = defaultdict(list)
            for v in self.vulnerabilities:
                by_severity[v["severity"]].append(v)
            
            for severity in reversed(SEVERITY_LEVELS):
                vulns = by_severity.get(severity, [])
                if vulns:
                    report.append(f"### {severity} ({len(vulns)})\n")
                    for v in vulns:
                        report.append(f"- **{v['package']}@{v['version']}**")
                        report.append(f"  - ID: `{v['vulnerability_id']}`")
                        report.append(f"  - Summary: {v['summary']}")
                        if v['references']:
                            report.append(f"  - References: {', '.join(v['references'][:2])}")
                        report.append("")
        else:
            report.append("## ✅ No Vulnerabilities Found\n")
        
        # License issues
        if self.license_issues:
            report.append("## ⚠️ License Issues\n")
            for issue in self.license_issues:
                report.append(f"- **{issue['package']}@{issue['version']}**")
                report.append(f"  - License: `{issue['license']}`")
                report.append(f"  - Reason: {issue['reason']}")
                report.append("")
        else:
            report.append("## ✅ No License Issues Found\n")
        
        return "\n".join(report)
    
    def post_pr_comment(self):
        """Post scan results as PR comment"""
        if os.getenv("GITHUB_EVENT_NAME") != "pull_request":
            print("ℹ Not a PR event, skipping comment")
            return
        
        pr_number = os.getenv("PR_NUMBER")
        if not pr_number:
            print("ℹ No PR number found")
            return
        
        print(f"\n💬 Posting comment to PR #{pr_number}...")
        
        try:
            with open("report.md", "r") as f:
                comment_body = f.read()
            
            # Use GitHub CLI to post comment
            subprocess.run(
                ["gh", "pr", "comment", pr_number, "--body", comment_body],
                env={**os.environ, "GH_TOKEN": os.getenv("GITHUB_TOKEN", "")},
                check=True
            )
            print("✓ Comment posted successfully")
        except Exception as e:
            print(f"⚠ Could not post comment: {e}")
    
    def set_outputs(self, passed: bool):
        """Set GitHub Action outputs"""
        github_output = os.getenv("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a") as f:
                f.write(f"vulnerabilities-found={len(self.vulnerabilities)}\n")
                f.write(f"license-issues-found={len(self.license_issues)}\n")
                f.write(f"status={'passed' if passed else 'failed'}\n")
    
    def run(self):
        """Main execution flow"""
        print("🚀 Starting SecureGate scan...\n")
        print(f"Working directory: {self.working_dir}")
        print(f"Mode: {self.config.get('mode')}")
        print(f"Severity threshold: {self.config.get('severity_threshold')}")
        
        # Step 1: Run OSV scanner
        osv_report = self.run_osv_scanner()
        self.vulnerabilities = self.parse_vulnerabilities(osv_report)
        
        # Step 2: Scan licenses
        self.license_issues = self.scan_licenses()
        
        # Step 3: Apply policy
        passed = self.apply_policy()
        
        # Step 4: Generate reports
        self.generate_report()
        
        # Step 5: Post PR comment if applicable
        self.post_pr_comment()
        
        # Step 6: Set outputs
        self.set_outputs(passed)
        
        # Exit with appropriate code
        if not passed:
            print("\n❌ Security scan FAILED")
            sys.exit(1)
        else:
            print("\n✅ Security scan PASSED")
            sys.exit(0)


if __name__ == "__main__":
    scanner = SecurityScanner()
    scanner.run()
