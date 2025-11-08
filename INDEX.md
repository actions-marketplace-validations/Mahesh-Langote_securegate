# 📚 SecureGate Documentation Index

Welcome to SecureGate! Choose your path:

## 🚀 I Want to USE SecureGate (Clients/Developers)

### Quick Start
1. **[5-Minute Setup](QUICK_SETUP.md)** ⭐ START HERE
   - Fastest way to get started
   - Copy-paste workflow file
   - Basic configuration

2. **[Complete Setup Guide](CLIENT_SETUP.md)**
   - Detailed step-by-step instructions
   - Configuration examples for every scenario
   - Troubleshooting guide
   - Best practices

### Reference Materials
- **[Quick Reference Card](QUICK_REFERENCE.md)** - Commands, configs, common patterns
- **[Architecture Overview](ARCHITECTURE.md)** - How SecureGate works under the hood

---

## 🛠️ I Want to PUBLISH/MAINTAIN SecureGate

### For Publishers
1. **[Publishing Guide](PUBLISHING.md)** ⭐ START HERE
   - How to publish to GitHub
   - Creating releases
   - GitHub Marketplace
   - Version management

### For Contributors
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute
- **[Changelog](CHANGELOG.md)** - Version history
- **[Architecture](ARCHITECTURE.md)** - Technical details

---

## 📖 Documentation by Topic

### Configuration
| Document | What You'll Learn |
|----------|-------------------|
| [Client Setup](CLIENT_SETUP.md) | All configuration options explained |
| [Quick Reference](QUICK_REFERENCE.md) | Quick config snippets |
| [Example Config](.github/security-gate.yml) | Default configuration file |

### Workflows
| Document | What You'll Learn |
|----------|-------------------|
| [Example Workflow](.github/workflows/security-scan.yml) | Basic workflow example |
| [Client Setup - Advanced](CLIENT_SETUP.md#advanced-configuration) | Complex workflows (monorepos, schedules) |

### Technical Details
| Document | What You'll Learn |
|----------|-------------------|
| [Architecture](ARCHITECTURE.md) | How it works internally |
| [scanner.py](scanner.py) | Source code for scanner |
| [action.yml](action.yml) | Action definition |

### Getting Help
| Document | What You'll Learn |
|----------|-------------------|
| [Client Setup - Troubleshooting](CLIENT_SETUP.md#troubleshooting) | Common issues and solutions |
| [Client Setup - FAQ](CLIENT_SETUP.md#faq) | Frequently asked questions |
| [Contributing](CONTRIBUTING.md) | How to report bugs |

---

## 📋 By User Type

### Flutter/Dart Developer (Using SecureGate)
1. Read: [5-Minute Setup](QUICK_SETUP.md)
2. Implement in your project
3. Reference: [Quick Reference](QUICK_REFERENCE.md)
4. Advanced: [Client Setup](CLIENT_SETUP.md)

### DevOps Engineer (Implementing SecureGate)
1. Read: [Client Setup Guide](CLIENT_SETUP.md)
2. Review: [Architecture](ARCHITECTURE.md)
3. Customize: [Example Workflows](.github/workflows/)
4. Reference: [Quick Reference](QUICK_REFERENCE.md)

### Security Team (Evaluating SecureGate)
1. Read: [README](README.md) - Features overview
2. Review: [Architecture](ARCHITECTURE.md) - How it works
3. Check: [Client Setup](CLIENT_SETUP.md) - Configuration options
4. Evaluate: [scanner.py](scanner.py) - Source code

### Action Publisher (Publishing SecureGate)
1. Read: [Publishing Guide](PUBLISHING.md)
2. Review: [Contributing](CONTRIBUTING.md)
3. Update: [Changelog](CHANGELOG.md)
4. Reference: [README](README.md)

### Contributor (Improving SecureGate)
1. Read: [Contributing](CONTRIBUTING.md)
2. Review: [Architecture](ARCHITECTURE.md)
3. Check: [Changelog](CHANGELOG.md)
4. Code: [scanner.py](scanner.py)

---

## 🗂️ All Files Reference

### Core Action Files
- `action.yml` - GitHub Action definition
- `scanner.py` - Python scanner script
- `requirements.txt` - Python dependencies

### Configuration
- `.github/security-gate.yml` - Default configuration
- `.github/workflows/security-scan.yml` - Example workflow

### Documentation
- `README.md` - Main documentation
- `QUICK_SETUP.md` - 5-minute setup guide
- `CLIENT_SETUP.md` - Complete client guide
- `ARCHITECTURE.md` - Technical architecture
- `QUICK_REFERENCE.md` - Quick reference card
- `PUBLISHING.md` - Publishing guide
- `INDEX.md` - This file

### Project Files
- `LICENSE` - MIT License
- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - Contribution guidelines
- `.gitignore` - Git ignore rules
- `requirnment.md` - Original requirements

---

## 🎯 Common Tasks

### "I want to add SecureGate to my Flutter project"
→ [5-Minute Setup](QUICK_SETUP.md)

### "I need to configure custom rules"
→ [Client Setup - Configuration Examples](CLIENT_SETUP.md#configuration-examples)

### "SecureGate is blocking my PR but I think it's a false positive"
→ [Client Setup - What to Do When Issues Are Found](CLIENT_SETUP.md#what-to-do-when-issues-are-found)

### "I want to scan multiple apps in a monorepo"
→ [Client Setup - Monorepo Setup](CLIENT_SETUP.md#monorepo-setup-multiple-flutter-apps)

### "How do I publish this action?"
→ [Publishing Guide](PUBLISHING.md)

### "I want to contribute to SecureGate"
→ [Contributing Guidelines](CONTRIBUTING.md)

### "I need to understand how severity levels work"
→ [Architecture - Severity Classification](ARCHITECTURE.md#severity-classification)

### "What reports does SecureGate generate?"
→ [Client Setup - Understanding Results](CLIENT_SETUP.md#understanding-the-results)

---

## 🔍 Search by Feature

### Vulnerability Scanning
- How it works: [Architecture](ARCHITECTURE.md)
- Configuration: [Client Setup](CLIENT_SETUP.md)
- Results: [Client Setup - Understanding Results](CLIENT_SETUP.md#understanding-the-results)

### License Detection
- How it works: [Architecture](ARCHITECTURE.md)
- Banned lists: [Client Setup - Configuration](CLIENT_SETUP.md#configuration-options)
- Whitelisting: [Client Setup - Examples](CLIENT_SETUP.md#example-3-balanced-approach)

### Policy Enforcement
- Modes: [Client Setup - Configuration](CLIENT_SETUP.md#configuration-options)
- Examples: [Client Setup - Examples](CLIENT_SETUP.md#configuration-examples)
- Decision flow: [Architecture - Decision Tree](ARCHITECTURE.md#decision-tree)

### PR Comments
- How it works: [Architecture - Integration Points](ARCHITECTURE.md#integration-points)
- Configuration: [Client Setup - Workflow](CLIENT_SETUP.md#step-by-step-setup)
- Troubleshooting: [Client Setup - Troubleshooting](CLIENT_SETUP.md#troubleshooting)

---

## 📞 Get Help

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/securegate/issues)
- 💡 **Feature Requests**: [GitHub Issues](https://github.com/yourusername/securegate/issues/new)
- 📖 **Documentation Issues**: [Contributing](CONTRIBUTING.md)
- ❓ **Questions**: Check [FAQ](CLIENT_SETUP.md#faq) first

---

**Still can't find what you need?** Open an issue on GitHub!
