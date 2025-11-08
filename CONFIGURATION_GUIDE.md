# 🎯 Client Configuration Guide - Which Setup is Right for You?

Not sure how to configure SecureGate? Follow this decision tree!

---

## Step 1: Choose Your Enforcement Mode

```
Do you want SecureGate to BLOCK your CI when it finds issues?

├─ YES, block CI if issues found
│  └─ Use: mode: block
│     (Recommended for production branches)
│
└─ NO, just show warnings/comments
   └─ Use: mode: annotate
      (Good for development, gradual adoption)
```

**Example:**
```yaml
# .github/security-gate.yml
mode: block  # or "annotate"
```

---

## Step 2: Choose Your Severity Threshold

```
What's the MINIMUM severity you care about?

├─ Only the most critical issues (CVE 9.0+)
│  └─ severity_threshold: CRITICAL
│     Use for: Legacy projects with many issues
│
├─ Urgent security issues (CVE 7.0+)
│  └─ severity_threshold: HIGH  ⭐ RECOMMENDED
│     Use for: Most production applications
│
├─ Moderate issues (CVE 4.0+)
│  └─ severity_threshold: MEDIUM
│     Use for: Highly secure environments
│
├─ Minor issues (CVE 0.1+)
│  └─ severity_threshold: LOW
│     Use for: Internal tools
│
└─ Everything including informational
   └─ severity_threshold: INFO
      Use for: Security audit mode
```

**Example:**
```yaml
severity_threshold: HIGH  # Most common choice
```

---

## Step 3: Choose License Restrictions

```
Do you have license restrictions?

├─ YES, my company has strict policies
│  └─ List banned licenses:
│     banned_licenses:
│       - GPL-3.0
│       - AGPL-3.0
│       - proprietary
│
├─ SOME restrictions
│  └─ banned_licenses:
│     - GPL-3.0      # Most restrictive
│     - proprietary  # Unknown/closed source
│
└─ NO, we're flexible
   └─ banned_licenses: []  # Empty list
```

**Example:**
```yaml
banned_licenses:
  - GPL-3.0
  - AGPL-3.0
  - SSPL-1.0
  - proprietary
```

---

## Step 4: Do You Need Exceptions?

```
Do you need to allow specific packages or ignore known issues?

├─ YES, some packages are approved despite license
│  └─ whitelist:
│       - approved_package_name
│
├─ YES, some dev dependencies can be ignored
│  └─ ignore_packages:
│       - test
│       - mockito
│
├─ YES, we're tracking a specific CVE but can't fix yet
│  └─ ignore_vulnerabilities:
│       - CVE-2024-12345  # Document why!
│
└─ NO, scan everything with no exceptions
   └─ Leave these lists empty
```

**Example:**
```yaml
# Allow Flutter core packages
whitelist:
  - flutter
  - dart

# Skip test dependencies
ignore_packages:
  - mockito
  - test

# Temporary exception (document!)
ignore_vulnerabilities:
  # JIRA-123: Waiting for vendor patch
  - CVE-2024-12345
```

---

## 🎨 Complete Configuration Templates

### Template 1: Strict Production
**Use when:** Deploying to production, high security requirements

```yaml
mode: block
severity_threshold: MEDIUM
banned_licenses:
  - GPL-2.0
  - GPL-3.0
  - AGPL-3.0
  - SSPL-1.0
  - proprietary
  - Commons Clause
whitelist:
  - flutter
  - dart
ignore_packages: []
ignore_vulnerabilities: []
```

### Template 2: Balanced (Recommended)
**Use when:** Most production applications

```yaml
mode: block
severity_threshold: HIGH
banned_licenses:
  - GPL-3.0
  - AGPL-3.0
  - proprietary
whitelist:
  - flutter
  - dart
ignore_packages:
  - test
  - mockito
  - integration_test
ignore_vulnerabilities: []
```

### Template 3: Development Friendly
**Use when:** Development branches, gradual adoption

```yaml
mode: annotate
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
  - build_runner
  - json_serializable
ignore_vulnerabilities: []
```

### Template 4: Security Audit
**Use when:** Initial assessment, understanding your security posture

```yaml
mode: annotate
severity_threshold: INFO
banned_licenses: []
whitelist: []
ignore_packages: []
ignore_vulnerabilities: []
```

### Template 5: Minimal Restrictions
**Use when:** Internal tools, prototypes

```yaml
mode: annotate
severity_threshold: CRITICAL
banned_licenses:
  - proprietary
whitelist: []
ignore_packages: []
ignore_vulnerabilities: []
```

---

## 📊 Decision Matrix

| Project Type | Mode | Threshold | Banned Licenses | Template |
|--------------|------|-----------|-----------------|----------|
| Public App | block | HIGH | Yes | Balanced |
| Enterprise App | block | MEDIUM | Strict | Strict |
| Internal Tool | annotate | HIGH | Some | Dev Friendly |
| Prototype | annotate | CRITICAL | Minimal | Minimal |
| Open Source | block | HIGH | Yes | Balanced |
| Legacy Project | annotate | CRITICAL | Yes | Dev Friendly |

---

## 🚀 Getting Started Workflow

### New Projects (Greenfield)
1. Start with **Template 2: Balanced**
2. Adjust based on first scan results
3. Gradually tighten as needed

### Existing Projects (Brownfield)
1. Start with **Template 4: Security Audit** (mode: annotate, INFO)
2. Review all findings
3. Create exceptions for known issues
4. Switch to **Template 2: Balanced**
5. Gradually remove exceptions

### High-Security Projects
1. Start with **Template 1: Strict Production**
2. Add necessary whitelists
3. Document all exceptions
4. Review regularly

---

## 🔄 Gradual Adoption Strategy

### Week 1: Discovery
```yaml
mode: annotate
severity_threshold: INFO
```
**Goal:** Understand what issues exist

### Week 2-3: Prioritize
```yaml
mode: annotate
severity_threshold: HIGH
```
**Goal:** Fix critical and high issues

### Week 4: Enforce
```yaml
mode: block
severity_threshold: HIGH
```
**Goal:** Prevent new high/critical issues

### Ongoing: Tighten
```yaml
mode: block
severity_threshold: MEDIUM
```
**Goal:** Improve overall security posture

---

## 💡 Pro Tips

### Tip 1: Different Rules for Different Branches
```yaml
# .github/workflows/security.yml
jobs:
  main-strict:
    if: github.ref == 'refs/heads/main'
    # Use strict config
  
  dev-lenient:
    if: github.ref == 'refs/heads/develop'
    # Use lenient config
```

### Tip 2: Always Document Exceptions
```yaml
ignore_vulnerabilities:
  # JIRA-123: False positive, doesn't affect our use case
  - CVE-2024-12345
  # JIRA-456: Vendor patch coming in Q2, monitoring
  - GHSA-xxxx-yyyy-zzzz
```

### Tip 3: Review Exceptions Regularly
Schedule monthly reviews of your ignore lists

### Tip 4: Start Lenient, Get Stricter
It's easier to tighten rules than to loosen them

---

## ❓ Still Unsure?

### Ask Yourself:

1. **"What's my risk tolerance?"**
   - High risk = Lower threshold (MEDIUM/LOW)
   - Moderate = HIGH
   - Low = CRITICAL

2. **"Will my team be frustrated by blocked PRs?"**
   - Yes = Start with `annotate`
   - No = Use `block`

3. **"Do I have legal requirements?"**
   - Yes = Strict banned licenses
   - No = Minimal restrictions

4. **"Am I starting fresh or adding to existing project?"**
   - Fresh = Start strict
   - Existing = Start lenient, tighten over time

---

## 📞 Need Help Deciding?

1. Check [CLIENT_SETUP.md](CLIENT_SETUP.md) for detailed examples
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
3. Start with **Template 2: Balanced** - works for 80% of projects
4. Open an issue if you have specific requirements

---

**Remember:** You can always adjust your configuration! Start somewhere and iterate. 🎯
