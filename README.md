# Flask Multi-Environment Template

A comprehensive Flask template with multi-environment support, designed for rapid development of web applications with best practices built in.

## About This Template

This template provides a solid foundation for building Flask web applications with:

- **Multiple environment configurations**: Development, testing, and production environments
- **Automated testing**: Unit, integration, and functional tests with pytest
- **Build reporting**: Automated test report generation
- **Error tracking**: Sentry.io integration
- **Docker support**: Containerized development and deployment
- **Git hooks**: Pre-commit and pre-push hooks for quality assurance

## Getting Started

To use this template, follow these steps:

### Option 1: GitHub Template (Recommended)

1. Click "Use this template" on the GitHub repository page
2. Name your repository and create it
3. Clone your new repository
4. Run the initialization script:

```bash
./init_project.py --name "Your Project Name" --description "Your project description"
```

### Option 2: Manual Setup

1. Clone this repository
2. Remove the Git history and initialize a new repository:

```bash
rm -rf .git
git init
```

3. Run the initialization script:

```bash
./init_project.py --name "Your Project Name" --description "Your project description"
```

## Environment Setup

This template uses environment-specific configuration files:

- `.env.development` - Development environment variables
- `.env.testing` - Testing environment variables
- `.env.production` - Production environment variables

To switch between environments, use the `switch_env.py` script:

```bash
# Switch to development environment
./switch_env.py development

# Switch to testing environment
./switch_env.py testing

# Switch to production environment
./switch_env.py production
```

## Running the Application

Use the `run_env.py` script to run the application in the specified environment:

```bash
# Run in development mode
./run_env.py development

# Run in testing mode
./run_env.py testing

# Run in production mode
./run_env.py production
```

## Docker Support

For containerized development and deployment:

```bash
# Start development environment
docker-compose up

# Build and run production container
docker build -t myapp .
docker run -p 5000:5000 myapp
```

## Test-Driven Development

This template enforces TDD practices with automated build reporting:

```bash
# Run all tests
make test

# Generate a build report
make report

# Verify build reports exist
make verify-reports
```

## Directory Structure

```
.
├── app/                  # Application package
│   ├── routes/           # Route definitions
│   ├── static/           # Static assets
│   ├── templates/        # HTML templates
│   └── utils/            # Utility modules
├── config/               # Configuration package
│   ├── __init__.py       # Config loader
│   ├── base.py           # Base configuration
│   ├── development.py    # Development configuration
│   ├── production.py     # Production configuration
│   └── testing.py        # Testing configuration
├── tests/                # Test suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── functional/       # Functional tests
├── build_reports/        # Test reports
├── instance/             # Instance-specific data
│   └── logs/             # Application logs
└── scripts/              # Utility scripts
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Template Documentation

For detailed information about using and customizing this template, see [TEMPLATE.md](TEMPLATE.md). 