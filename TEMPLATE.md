# Flask Multi-Environment Template

This is a template for Flask applications with multi-environment support. It provides a solid foundation for creating Flask applications with separate configurations for development, production, and testing environments.

## Features

- **Multi-Environment Support**: Development, Production, and Testing configurations
- **Configuration System**: Centralized configuration with environment-specific overrides
- **Environment Management**: Scripts for switching between environments
- **Docker Support**: Docker and Docker Compose configurations for containerized development
- **Sentry Integration**: Error monitoring with Sentry.io
- **TDD Support**: Test-driven development with build report generation
- **Git Hooks**: Pre-commit and pre-push hooks for quality control

## Getting Started

### Using GitHub Template (Recommended)

1. Click the "Use this template" button on the GitHub repository page
2. Name your new repository and create it
3. Clone the new repository
4. Initialize the project:

```bash
./init_project.py --name "My New Project" --description "A detailed description of the project"
```

### Manual Setup

1. Clone this repository
2. Remove the existing Git history:

```bash
rm -rf .git
```

3. Initialize a new Git repository:

```bash
git init
```

4. Initialize the project:

```bash
./init_project.py --name "My New Project" --description "A detailed description of the project"
```

## Project Structure

```
.
├── app/                      # Application package
│   ├── routes/               # Route definitions
│   ├── static/               # Static assets
│   ├── templates/            # HTML templates
│   └── utils/                # Utility modules
├── config/                   # Configuration package
│   ├── __init__.py           # Config loader
│   ├── base.py               # Base configuration
│   ├── development.py        # Development configuration
│   ├── production.py         # Production configuration
│   └── testing.py            # Testing configuration
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── ...                   # Other test types
├── .env.development          # Development environment variables
├── .env.production           # Production environment variables
├── .env.testing              # Testing environment variables
├── .env.example              # Example environment variables
├── app.py                    # Application entry point
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── requirements-test.txt     # Testing dependencies
├── run_env.py                # Environment runner script
└── switch_env.py             # Environment switcher script
```

## Running the Application

### Development Mode

```bash
# Switch to development environment
./switch_env.py development

# Run the application
./run_env.py development
```

### Production Mode

```bash
# Switch to production environment
./switch_env.py production

# Run the application
./run_env.py production
```

### Docker Mode

```bash
# Start the development container
./run_env.py development --docker

# Start the production container
./run_env.py production --docker
```

## Customizing the Template

This template is designed to be customized to fit your specific needs. Here are some common customizations:

### Adding New Dependencies

1. Add production dependencies to `requirements.txt`
2. Add development dependencies to `requirements-dev.txt`
3. Add testing dependencies to `requirements-test.txt`

### Changing Database

1. Update the database configuration in `config/base.py`, `config/development.py`, etc.
2. Update the `DATABASE_URL` in the environment files

### Adding New Routes

1. Create a new route file in `app/routes/`
2. Register the blueprint in `app.py`

## Template Maintenance

To update this template:

1. Make changes to the `template` branch
2. Test the changes
3. Push the changes to GitHub
4. Update existing projects by cherry-picking relevant commits 