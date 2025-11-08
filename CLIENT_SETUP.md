# 🚀 Client Setup Guide for SecureGate

This guide is for developers who want to use SecureGate in their Flutter/Dart projects.

## Prerequisites

- GitHub repository with a Flutter or Dart project
- `pubspec.lock` file in your repository
- GitHub Actions enabled

## Step-by-Step Setup

### 1️⃣ Create Workflow File

In your Flutter/Dart project, create this file:

**`.github/workflows/security.yml`**

```yaml
name: Security Scan

on:
  pull_request:
  push:
    branches: [main, master, develop]

jobs:
  security:
    name: SecureGate Scan
    runs-on: ubuntu-latest
    
    permissions:
      contents: read
      pull-requests: write
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Run security scan
        uses: YOUR_USERNAME/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

**Important:** Replace `YOUR_USERNAME` with the actual GitHub username where SecureGate is published.

### 2️⃣ Create Configuration File (Optional)

If you want custom settings, create:

**`.github/security-gate.yml`**

```yaml
# Choose "block" to fail CI or "annotate" to just comment
mode: block

# Licenses you don't allow in your project
banned_licenses:
  - GPL-3.0
  - AGPL-3.0
  - SSPL-1.0
  - proprietary

# Minimum severity to trigger action
# Options: INFO, LOW, MEDIUM, HIGH, CRITICAL
severity_threshold: HIGH

# Approved packages (skip license check for these)
whitelist:
  # - some_package_you_trust

# Skip vulnerability scanning for these packages
ignore_packages:
  # - test_only_package

# Ignore specific vulnerabilities (use with caution!)
ignore_vulnerabilities:
  # - CVE-2024-12345
```

### 3️⃣ Commit and Push

```bash
git add .github/
git commit -m "Add SecureGate security scanning"
git push
```

### 4️⃣ That's It! 🎉

SecureGate will now:
- ✅ Run on every pull request
- ✅ Run on pushes to main/develop branches
- ✅ Scan for vulnerabilities
- ✅ Check license compliance
- ✅ Post results as PR comments
- ✅ Block/annotate based on your configuration

## Configuration Examples

### Example 1: Strict Mode (Recommended for Production)

```yaml
mode: block
severity_threshold: MEDIUM
banned_licenses:
  - GPL-3.0
  - AGPL-3.0
  - SSPL-1.0
  - proprietary
  - Commons Clause
```

**Use case:** Production apps where security is critical

### Example 2: Warning Mode (Good for Development)

```yaml
mode: annotate
severity_threshold: HIGH
```

**Use case:** Development branches where you want visibility but not blocking

### Example 3: Balanced Approach

```yaml
mode: block
severity_threshold: HIGH
banned_licenses:
  - GPL-3.0
  - AGPL-3.0
whitelist:
  - flutter
  - dart
ignore_packages:
  - test
  - mockito
```

**Use case:** Most teams - blocks high severity issues, allows common dev tools

## Advanced Configuration

### Different Rules for Different Branches

**`.github/workflows/security.yml`**

```yaml
name: Security Scan

on:
  pull_request:
  push:
    branches: [main, develop]

jobs:
  # Strict scanning for main branch
  security-main:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: YOUR_USERNAME/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          config-path: .github/security-gate-strict.yml
  
  # Lenient scanning for develop branch
  security-dev:
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: YOUR_USERNAME/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          config-path: .github/security-gate-lenient.yml
```

### Monorepo Setup (Multiple Flutter Apps)

```yaml
jobs:
  scan-mobile-app:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: YOUR_USERNAME/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          working-directory: ./apps/mobile
          config-path: ./apps/mobile/.github/security-gate.yml
  
  scan-web-app:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: YOUR_USERNAME/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          working-directory: ./apps/web
          config-path: ./apps/web/.github/security-gate.yml
```

### Schedule Regular Scans

```yaml
name: Weekly Security Scan

on:
  schedule:
    # Run every Monday at 9 AM UTC
    - cron: '0 9 * * 1'
  workflow_dispatch:  # Allow manual trigger

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: YOUR_USERNAME/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Understanding the Results

### Where to Find Results

1. **GitHub Actions Tab**: See detailed logs
2. **Pull Request Comments**: Automatic reports posted on PRs
3. **Artifacts**: Download detailed reports (report.md, JSON files)

### Reading the Report

```markdown
# 🛡️ SecureGate Security Scan Report

## Summary
- Vulnerabilities Found: 2
- License Issues: 1
- Mode: block
- Severity Threshold: HIGH

## 🔴 Vulnerabilities
### CRITICAL (1)
- package_name@1.0.0
  - ID: CVE-2024-12345
  - Summary: Remote code execution vulnerability
  
### HIGH (1)
- another_package@2.0.0
  - ID: GHSA-xxxx-xxxx-xxxx
  - Summary: SQL injection vulnerability

## ⚠️ License Issues
- problematic_package@1.5.0
  - License: GPL-3.0
  - Reason: License 'GPL-3.0' is banned
```

### What to Do When Issues Are Found

#### For Vulnerabilities:
1. **Update the package**: `flutter pub upgrade package_name`
2. **Check if patch available**: Look at package changelog
3. **Temporary workaround**: Add to `ignore_vulnerabilities` with comment explaining why
4. **Find alternative**: Switch to a different package

#### For License Issues:
1. **Check if correct**: Sometimes license detection is wrong
2. **Get approval**: Discuss with legal team
3. **Add to whitelist**: If approved for use
4. **Find alternative**: Use package with compatible license

## Customization Options

### Input Parameters

```yaml
- uses: YOUR_USERNAME/securegate@v1
  with:
    # GitHub token (required)
    github-token: ${{ secrets.GITHUB_TOKEN }}
    
    # Path to config file (optional)
    config-path: .github/security-gate.yml
    
    # Working directory (optional, for monorepos)
    working-directory: ./
```

### Configuration File Options

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `mode` | string | `block` or `annotate` | `block` |
| `banned_licenses` | list | Licenses to block | `[GPL-3.0, AGPL-3.0, SSPL-1.0, proprietary]` |
| `severity_threshold` | string | Minimum severity | `HIGH` |
| `whitelist` | list | Packages exempt from license check | `[]` |
| `ignore_packages` | list | Skip vulnerability scan | `[]` |
| `ignore_vulnerabilities` | list | Ignore specific CVEs | `[]` |

## Troubleshooting

### Common Issues

#### ❌ "pubspec.lock not found"
**Solution:** Make sure `pubspec.lock` is committed to your repository
```bash
flutter pub get
git add pubspec.lock
git commit -m "Add pubspec.lock"
git push
```

#### ❌ "Permission denied" when posting comments
**Solution:** Add permissions to workflow file
```yaml
permissions:
  contents: read
  pull-requests: write
```

#### ❌ Action fails with timeout
**Solution:** OSV Scanner might be slow. This is normal for large projects.

#### ❌ Too many false positives
**Solution:** Adjust configuration
```yaml
severity_threshold: CRITICAL  # Only block critical issues
ignore_packages:
  - dev_dependency_1
  - test_package_2
```

### Getting Help

- 📖 Check [full documentation](README.md)
- 🐛 Report issues on GitHub
- 💡 Check existing issues for solutions

## Best Practices

### ✅ Do's
- ✅ Commit `pubspec.lock` to version control
- ✅ Start with `annotate` mode to understand findings
- ✅ Review and address high/critical vulnerabilities promptly
- ✅ Document why you ignore specific issues
- ✅ Run scans on PRs and main branch
- ✅ Schedule regular scans (weekly recommended)

### ❌ Don'ts
- ❌ Don't ignore all vulnerabilities blindly
- ❌ Don't disable scanning because of false positives (adjust config instead)
- ❌ Don't forget to update ignored vulnerabilities list when fixed
- ❌ Don't skip license compliance checks

## Quick Start Checklist

- [ ] Create `.github/workflows/security.yml`
- [ ] (Optional) Create `.github/security-gate.yml`
- [ ] Replace `YOUR_USERNAME` with actual username
- [ ] Commit and push files
- [ ] Create a test PR to see it in action
- [ ] Adjust configuration based on results
- [ ] Add to team documentation

## Example: Real-World Configuration

Here's what a typical production Flutter app might use:

```yaml
# .github/security-gate.yml
mode: block
severity_threshold: HIGH

banned_licenses:
  - GPL-3.0
  - AGPL-3.0
  - SSPL-1.0
  - proprietary

# Allow common Flutter/Dart packages
whitelist:
  - flutter
  - flutter_test
  - dart

# Ignore test-only packages
ignore_packages:
  - mockito
  - test
  - integration_test

# Documented exceptions (with tracking)
ignore_vulnerabilities:
  # JIRA-123: Vendor evaluating patch, temporary exception until Q1 2025
  # - CVE-2024-12345
```

## Updating SecureGate

To update to a newer version:

```yaml
# Use specific version
- uses: YOUR_USERNAME/securegate@v1.0.1

# Or use major version (auto-updates to latest v1.x.x)
- uses: YOUR_USERNAME/securegate@v1

# Or pin to specific commit (most stable)
- uses: YOUR_USERNAME/securegate@abc1234
```

## FAQ

**Q: Will this slow down my CI/CD?**
A: Typically adds 1-3 minutes. Runs in parallel with other jobs.

**Q: Can I run this locally?**
A: Yes, but requires setup. It's designed for CI/CD.

**Q: What if a package has no license?**
A: It will be flagged as "UNKNOWN" - review manually.

**Q: Can I use this for Dart packages (not Flutter)?**
A: Yes! Works with any Dart project with `pubspec.lock`.

**Q: Does this replace my security audit?**
A: No, it's an automated first line of defense. Human review is still important.

---

**Need help?** Open an issue on the SecureGate repository!

Happy secure coding! 🔒✨
