# SecureGate Quick Reference

## Basic Workflow

```yaml
- uses: yourusername/securegate@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Configuration Options

| Option | Values | Description |
|--------|--------|-------------|
| `mode` | `block`, `annotate` | Fail CI or just comment |
| `severity_threshold` | `INFO`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` | Min severity to act on |
| `banned_licenses` | List of strings | Licenses to block |
| `whitelist` | List of strings | Exempt packages |
| `ignore_packages` | List of strings | Skip vulnerability scan |
| `ignore_vulnerabilities` | List of CVE IDs | Skip specific CVEs |

## Common Configurations

### Strict (Production)
```yaml
mode: block
severity_threshold: MEDIUM
banned_licenses: [GPL-3.0, AGPL-3.0, proprietary]
```

### Lenient (Development)
```yaml
mode: annotate
severity_threshold: CRITICAL
```

### Custom
```yaml
mode: block
severity_threshold: HIGH
banned_licenses: [GPL-3.0, AGPL-3.0]
whitelist: [approved_package]
ignore_vulnerabilities: [CVE-2024-12345]
```

## Action Inputs

```yaml
with:
  github-token: ${{ secrets.GITHUB_TOKEN }}  # Required
  config-path: .github/security-gate.yml     # Optional
  working-directory: ./                      # Optional
```

## Action Outputs

```yaml
steps.securegate.outputs.vulnerabilities-found     # Number
steps.securegate.outputs.license-issues-found      # Number
steps.securegate.outputs.status                    # passed/failed
```

## Generated Files

- `osv-report.json` - Raw vulnerability data
- `license-report.json` - License issues
- `report.md` - Human-readable summary
- `final-report.json` - Complete results

## Severity Levels (High → Low)

1. CRITICAL - Immediate action
2. HIGH - Urgent
3. MEDIUM - Should fix
4. LOW - Minor
5. INFO - Informational

## Quick Commands

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run scanner
python scanner.py
```

### Update Action Version
```bash
git tag -a v1.0.1 -m "Update"
git push origin v1.0.1
git tag -fa v1
git push origin v1 --force
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| pubspec.lock not found | Run `flutter pub get` |
| Permission denied | Check token permissions |
| Scanner fails | Verify OSV Scanner installed |
| No comments posted | Check PR context and token |

## Example: Multiple Projects

```yaml
jobs:
  scan-app1:
    steps:
      - uses: yourusername/securegate@v1
        with:
          working-directory: ./app1
          
  scan-app2:
    steps:
      - uses: yourusername/securegate@v1
        with:
          working-directory: ./app2
```

## Resources

- [Full Documentation](README.md)
- [Publishing Guide](PUBLISHING.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
