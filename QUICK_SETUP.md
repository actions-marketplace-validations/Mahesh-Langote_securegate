# 🎯 SecureGate - 5 Minute Setup

Get security scanning in your Flutter/Dart project in 5 minutes!

## Step 1: Create Workflow (2 minutes)

Create file: `.github/workflows/security.yml`

```yaml
name: Security Scan
on: [pull_request, push]

jobs:
  security:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: YOUR_USERNAME/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

**Replace `YOUR_USERNAME`** with the actual GitHub username!

## Step 2: Configure (1 minute) - OPTIONAL

Create file: `.github/security-gate.yml`

```yaml
mode: block                    # or "annotate" for warnings only
severity_threshold: HIGH       # or CRITICAL, MEDIUM, LOW, INFO
banned_licenses:
  - GPL-3.0
  - AGPL-3.0
  - proprietary
```

## Step 3: Commit & Push (1 minute)

```bash
git add .github/
git commit -m "Add security scanning"
git push
```

## Step 4: Test (1 minute)

1. Create a pull request
2. Wait for the action to run
3. See results in PR comments

## Done! 🎉

SecureGate is now protecting your project!

---

## What Happens Next?

### ✅ Every Pull Request:
- Scans for vulnerabilities
- Checks license compliance
- Posts results as comments
- Blocks/warns based on your config

### 📊 You Get:
- Detailed reports
- Severity ratings
- Actionable recommendations
- Artifact downloads

### 🔧 You Can:
- Adjust severity threshold
- Whitelist packages
- Ignore specific issues
- Change enforcement mode

---

## Quick Configurations

### 🔴 Strict (Production)
```yaml
mode: block
severity_threshold: MEDIUM
```

### 🟡 Balanced (Recommended)
```yaml
mode: block
severity_threshold: HIGH
```

### 🟢 Lenient (Development)
```yaml
mode: annotate
severity_threshold: CRITICAL
```

---

## Need More Help?

📖 **Full Guide**: [CLIENT_SETUP.md](CLIENT_SETUP.md)  
❓ **Questions**: Open an issue  
📚 **Docs**: [README.md](README.md)

---

**That's it!** Your project is now more secure! 🔒
