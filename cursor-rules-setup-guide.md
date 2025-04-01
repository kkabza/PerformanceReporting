# Cursor Rules Setup Guide

This document provides guidelines for properly configuring cursor rules in the Performance Reporting app.

## Rule Structure

Each rule should have the following structure:

```md
---
description: Brief description of what the rule enforces
globs: ["pattern1", "pattern2"] # Files the rule applies to
alwaysApply: true/false # Whether to always check the rule
---

# Rule Title

## Description
Detailed description of the rule

## Problem
What issues the rule prevents

## Solution
How to follow the rule correctly

...
```

## Recommended Glob Patterns

Here are the recommended glob patterns for different rule types:

| Rule Type | Recommended Globs |
|-----------|-------------------|
| Flask Route Imports | `["app/routes/**/*.py"]` |
| Flask Blueprint Consistency | `["app/routes/**/*.py"]` |
| Flask URL Generation | `["app/templates/**/*.html"]` |
| Template Naming | `["app/templates/**/*.html", "app/routes/**/*.py"]` |
| UI Accessibility | `["app/templates/**/*.html", "app/static/css/**/*.css"]` |
| Build Versioning | `["**/*.py", "app/templates/base.html", "Dockerfile"]` |
| Logging Format | `["logs/**/*", "app/logs/**/*", "instance/logs/**/*", "**/logging.py"]` |
| TDD Practices | `["tests/**/*.py", "run.py", "app/utils/report_enforcer.py", "build_reports/**"]` |
| Environment Config | `[".env*", "**/*.py", "app/config.py"]` |

## Currently Broken Rules

The following rules need to be fixed with proper glob patterns:

1. `flask_route_blueprint_consistency.mdc` (only 46 bytes)
2. `flask_route_imports.mdc` (only 54 bytes)
3. `build_report_enforcement.mdc` (only 1 byte)
4. `environment_config.mdc` (only 1 byte)
5. `implementation_checklist.mdc` (only 1 byte)

## How to Fix Rules

For each broken rule:

1. Make a backup of the current file
2. Create a new file with the proper structure
3. Add appropriate metadata with globs
4. Add detailed rule content
5. Commit the updated rule file

Example:

```bash
# Fix a broken rule
cp .cursor/rules/flask_route_imports.mdc .cursor/rules/flask_route_imports.mdc.bak
cat > .cursor/rules/flask_route_imports.mdc << 'EOL'
---
description: Ensures all Flask route files have the correct imports for proper functionality
globs: ["app/routes/**/*.py"]
alwaysApply: true
---

# Flask Route Imports Consistency

... rest of the rule content ...
EOL
```

## Common Issues

If you're experiencing problems with rule files:
- Check file permissions
- Watch out for hidden characters
- Make sure the text editor is configured correctly
- Try deleting and recreating the file from scratch
- Verify the file using `cat` before committing 