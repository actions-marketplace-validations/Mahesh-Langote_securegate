Requirements
Functional Requirements

Dependency Vulnerability Scanning

Use osv-scanner to detect vulnerabilities in Dart/Flutter dependencies via pubspec.lock.

Parse results and classify by severity (INFO → CRITICAL).

License Detection

Detect package licenses using pana or dart_pubspec_licenses.

Compare each dependency’s license against a configurable banned list.

Policy Enforcement

Read a configuration file .github/security-gate.yml with parameters:

Mode (block or annotate)

Banned license list

Severity threshold for vulnerabilities

Whitelist/ignore lists

Decide whether to block a PR (fail the job) or annotate it with a comment.

Reporting

Generate a report.md and final-report.json summarizing vulnerabilities and license issues.

Post report as a PR comment or fail the CI job.

Artifact Storage

Upload scan outputs (OSV report, license report, final report) as build artifacts.

Non-Functional Requirements

Must run on ubuntu-latest GitHub runner.

Use stable versions of Flutter/Dart.

No external API credentials required (use GITHUB_TOKEN only).

Average runtime < 3 minutes for small-to-medium projects.

Compatible with both Flutter apps and Dart packages.

Configurable to be lenient (annotate) or strict (block).