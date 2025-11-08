# Publishing SecureGate to GitHub

This guide will help you publish SecureGate as a public GitHub Action that other developers can use.

## Prerequisites

- GitHub account
- Git installed on your machine
- Repository ready with all the action files

## Step 1: Create GitHub Repository

1. Go to GitHub.com and sign in
2. Click the **+** icon → **New repository**
3. Repository settings:
   - **Name**: `securegate` (or your preferred name)
   - **Description**: "Security scanner for Flutter/Dart dependencies"
   - **Visibility**: Public ✅
   - **Initialize**: Don't initialize (we have files already)
4. Click **Create repository**

## Step 2: Initialize Git and Push Code

Open terminal in your project directory and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial release of SecureGate v1.0.0"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/securegate.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Create a Release

Creating a release allows others to use your action with `@v1` syntax:

1. Go to your repository on GitHub
2. Click **Releases** (right sidebar)
3. Click **Create a new release**
4. Fill in the details:
   - **Tag**: `v1.0.0`
   - **Target**: `main`
   - **Title**: `SecureGate v1.0.0 - Initial Release`
   - **Description**: Copy from CHANGELOG.md
5. Click **Publish release**

## Step 4: Create Version Tags

To enable users to use `@v1` (which auto-updates to latest v1.x.x):

```bash
# Create and push v1 tag
git tag -a v1 -m "Version 1"
git push origin v1

# If you make updates later, move the v1 tag:
git tag -fa v1 -m "Version 1"
git push origin v1 --force
```

## Step 5: Test Your Action

Create a test repository with a Flutter/Dart project:

1. Create a new repository with a Flutter app
2. Add `.github/workflows/security-scan.yml`:

```yaml
name: Test SecureGate

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: YOUR_USERNAME/securegate@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

3. Push and verify the action runs successfully

## Step 6: Register with GitHub Marketplace (Optional)

To make your action discoverable:

1. Go to your repository
2. Edit the `action.yml` file on GitHub
3. GitHub will show an option to publish to Marketplace
4. Click **Draft a release** → **Publish to GitHub Marketplace**
5. Follow the prompts

## Step 7: Update README

Update the README.md with your actual GitHub username:

```markdown
- uses: YOUR_USERNAME/securegate@v1
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Usage for Other Developers

After publishing, developers can use your action like this:

```yaml
- uses: YOUR_USERNAME/securegate@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

Or pin to a specific version:

```yaml
- uses: YOUR_USERNAME/securegate@v1.0.0
```

## Releasing Updates

When you make changes:

1. Update CHANGELOG.md
2. Commit changes
3. Create new tag and release:

```bash
git tag -a v1.0.1 -m "Bug fixes"
git push origin v1.0.1

# Update v1 to point to latest
git tag -fa v1 -m "Version 1"
git push origin v1 --force
```

## Best Practices

### Versioning
- **v1.0.0**: Major.Minor.Patch
- **v1**: Major version (auto-updates)
- Use semantic versioning

### Documentation
- Keep README updated
- Document breaking changes
- Add examples for common use cases

### Testing
- Test action before releasing
- Use test repositories
- Verify on different project types

### Support
- Respond to issues promptly
- Welcome contributions
- Keep dependencies updated

## File Structure

Your published repository should have:

```
securegate/
├── .github/
│   ├── workflows/
│   │   └── security-scan.yml    # Example workflow
│   └── security-gate.yml         # Default config
├── action.yml                    # Action definition
├── scanner.py                    # Main script
├── requirements.txt              # Python dependencies
├── README.md                     # Documentation
├── LICENSE                       # MIT License
├── CHANGELOG.md                  # Version history
├── CONTRIBUTING.md               # Contribution guide
├── .gitignore                   # Git ignore
└── requirnment.md               # Original requirements
```

## Troubleshooting

### Action not found
- Ensure repository is public
- Verify the action path is correct
- Check that action.yml exists in the root

### Permission denied
- Check repository permissions
- Verify GITHUB_TOKEN has required scopes

### Action fails to run
- Test the Python script locally first
- Check all dependencies are installed correctly
- Verify OSV Scanner installs properly

## Promotion

Share your action:
- Tweet about it
- Post on Reddit (r/FlutterDev)
- Share in Flutter Discord servers
- Write a blog post
- Add to Awesome Lists

## Support

Provide support through:
- GitHub Issues
- GitHub Discussions
- Documentation updates
- Example repositories

---

Good luck with your action! 🚀
