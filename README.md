# 🛡️ SecureGate

A GitHub Action that scans Flutter/Dart dependencies for security vulnerabilities and license compliance issues.

[![GitHub](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/yourusername/securegate)](https://github.com/yourusername/securegate/releases)

> **📘 Want to use this in your project?** See the [Client Setup Guide](CLIENT_SETUP.md) for step-by-step instructions!

## Features

- 🔍 **Vulnerability Scanning** - Detects known security vulnerabilities using [OSV Scanner](https://github.com/google/osv-scanner)
- 📜 **License Detection** - Identifies and flags packages with banned licenses
- ⚖️ **Policy Enforcement** - Configurable rules to block or annotate PRs based on findings
- 📊 **Detailed Reporting** - Generates comprehensive reports in Markdown and JSON formats
- 💬 **PR Comments** - Automatically posts scan results to pull requests
- 🎯 **Severity Filtering** - Set custom thresholds for vulnerability severity
- ✨ **Easy Configuration** - Simple YAML configuration file

## Quick Start

### Basic Usage

Add this action to your workflow:

```yaml
name: Security Scan

on:
  pull_request:
  push:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: yourusername/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### With Custom Configuration

```yaml
- uses: yourusername/securegate@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    config-path: .github/security-gate.yml
    working-directory: ./
```

## Configuration

Create a `.github/security-gate.yml` file in your repository:

```yaml
# Enforcement mode: "block" or "annotate"
mode: block

# Banned licenses
banned_licenses:
  - GPL-3.0
  - AGPL-3.0
  - SSPL-1.0
  - proprietary

# Minimum severity to trigger action
# Options: INFO, LOW, MEDIUM, HIGH, CRITICAL
severity_threshold: HIGH

# Whitelist packages from license checking
whitelist:
  - some_approved_package

# Ignore packages from vulnerability scanning
ignore_packages:
  - test_package

# Ignore specific vulnerabilities
ignore_vulnerabilities:
  - CVE-2024-12345
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `mode` | Enforcement mode: `block` (fail CI) or `annotate` (comment only) | `block` |
| `banned_licenses` | List of licenses that are not allowed | See example |
| `severity_threshold` | Minimum vulnerability severity to act on | `HIGH` |
| `whitelist` | Packages exempt from license checks | `[]` |
| `ignore_packages` | Packages to skip in vulnerability scanning | `[]` |
| `ignore_vulnerabilities` | Specific CVE/GHSA IDs to ignore | `[]` |

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `github-token` | GitHub token for posting comments | Yes | `${{ github.token }}` |
| `config-path` | Path to configuration file | No | `.github/security-gate.yml` |
| `working-directory` | Directory containing pubspec.lock | No | `.` |

## Outputs

| Output | Description |
|--------|-------------|
| `vulnerabilities-found` | Number of vulnerabilities detected |
| `license-issues-found` | Number of license violations found |
| `status` | Scan result: `passed` or `failed` |

## Use Output in Workflow

```yaml
- name: Run Security Scan
  id: security
  uses: yourusername/securegate@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}

- name: Check Results
  run: |
    echo "Vulnerabilities: ${{ steps.security.outputs.vulnerabilities-found }}"
    echo "License Issues: ${{ steps.security.outputs.license-issues-found }}"
    echo "Status: ${{ steps.security.outputs.status }}"
```

## Reports

SecureGate generates the following reports as artifacts:

- **report.md** - Human-readable Markdown report
- **final-report.json** - Complete JSON report with all findings
- **osv-report.json** - Raw OSV scanner output
- **license-report.json** - License scanning results

Access reports in the Actions tab → Artifacts section.

## Examples

### Example 1: Strict Security for Production

```yaml
name: Production Security

on:
  push:
    branches: [main, release/*]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: yourusername/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

Configuration (`.github/security-gate.yml`):
```yaml
mode: block
severity_threshold: MEDIUM
banned_licenses:
  - GPL-3.0
  - AGPL-3.0
  - proprietary
```

### Example 2: Lenient Scanning for Development

```yaml
name: Dev Security Check

on:
  pull_request:
    branches: [develop]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: yourusername/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

Configuration:
```yaml
mode: annotate  # Don't block PRs, just comment
severity_threshold: CRITICAL
ignore_packages:
  - dev_dependency
```

### Example 3: Monorepo with Multiple Flutter Apps

```yaml
name: Security Scan

on: [pull_request, push]

jobs:
  scan-app1:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: yourusername/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          working-directory: ./apps/app1
          config-path: ./apps/app1/.github/security-gate.yml
  
  scan-app2:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: yourusername/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          working-directory: ./apps/app2
          config-path: ./apps/app2/.github/security-gate.yml
```

## How It Works

1. **Setup** - Installs Python, OSV Scanner, Dart SDK, and dependencies
2. **Vulnerability Scan** - Runs OSV Scanner on `pubspec.lock`
3. **License Check** - Analyzes package licenses using Dart tools
4. **Policy Enforcement** - Compares findings against your configuration
5. **Reporting** - Generates detailed reports and artifacts
6. **PR Comment** - Posts results to pull requests (if applicable)
7. **Exit** - Fails the job if blocking issues are found (in `block` mode)

## Severity Levels

Vulnerabilities are classified into five levels:

- **CRITICAL** - Immediate action required
- **HIGH** - Should be addressed urgently
- **MEDIUM** - Should be addressed
- **LOW** - Minor issues
- **INFO** - Informational only

## Common Use Cases

### Block PRs with High Severity Vulnerabilities

```yaml
mode: block
severity_threshold: HIGH
```

### Alert on Any Vulnerability, Don't Block

```yaml
mode: annotate
severity_threshold: INFO
```

### Strict License Compliance

```yaml
mode: block
banned_licenses:
  - GPL-2.0
  - GPL-3.0
  - AGPL-3.0
  - SSPL-1.0
  - proprietary
  - Commons Clause
```

### Temporary Exception for Known Issue

```yaml
ignore_vulnerabilities:
  - CVE-2024-12345  # Tracked in JIRA-123, will be fixed next sprint
```

## Troubleshooting

### "pubspec.lock not found"
Ensure your repository contains a `pubspec.lock` file. Run `flutter pub get` or `dart pub get` locally and commit the file.

### License detection not working
The action requires packages to have proper license metadata. Some packages may not include license information.

### OSV Scanner fails
Check that your `pubspec.lock` is valid and up-to-date. Try running `flutter pub get` to regenerate it.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

- [OSV Scanner](https://github.com/google/osv-scanner) by Google
- [pana](https://pub.dev/packages/pana) for Dart package analysis

## Support

- 📝 [Report Issues](https://github.com/yourusername/securegate/issues)
- 💡 [Feature Requests](https://github.com/yourusername/securegate/issues/new)
- 📖 [Documentation](https://github.com/yourusername/securegate)

## Documentation

- 📘 **[Client Setup Guide](CLIENT_SETUP.md)** - How to configure SecureGate in your project
- 🏗️ **[Architecture](ARCHITECTURE.md)** - How SecureGate works internally
- 📋 **[Quick Reference](QUICK_REFERENCE.md)** - Quick command reference
- 🚀 **[Publishing Guide](PUBLISHING.md)** - How to publish this action
- 🤝 **[Contributing](CONTRIBUTING.md)** - Contribution guidelines

---

Made with ❤️ for the Flutter/Dart community
