# Florida Tax Certificate Sale Auctions

## Overview
This web application provides a platform for participating in Florida Tax Certificate Sale Auctions. Tax certificate sales are a process where tax liens on properties with delinquent taxes are sold to investors through an auction system.

## Features
- Real-time auction monitoring
- User registration and authentication
- Search and filter tax certificates
- Bidding system
- Payment processing
- Certificate management
- Historical data tracking
- County-specific auction information
- Error monitoring with Sentry

## Technology Stack
- Frontend: React.js
- Backend: Flask (Python)
- Database: PostgreSQL
- Authentication: JWT
- Real-time Updates: WebSocket
- Error Monitoring: Sentry.io

## Environment Setup

This project supports multiple environments:

### Environment Types
- **Development**: For local development with debugging features enabled
- **Testing**: For running automated tests
- **Production**: For deployment with optimized settings and security features

### Environment Files
Each environment has its own configuration file:
- `.env.development` - Development settings
- `.env.testing` - Testing settings
- `.env.production` - Production settings  
- `.env.example` - Template for creating new environment files

### Switching Environments
Use the provided script to switch between environments:

```bash
# Switch to development environment
./switch_env.py development

# Switch to production environment
./switch_env.py production

# Switch to testing environment
./switch_env.py testing
```

### Running in Different Environments
Use the run_env.py script to start the application in the desired environment:

```bash
# Run in development mode
./run_env.py development

# Run in production mode
./run_env.py production

# Run with Docker Compose
./run_env.py development --docker

# Run in production with custom settings
./run_env.py production --port 8000 --workers 4
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
├── app.py                    # Application entry point
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── requirements-test.txt     # Testing dependencies
├── run_env.py                # Environment runner script
└── switch_env.py             # Environment switcher script
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip
- PostgreSQL

### Installation
1. Clone the repository:
```bash
git clone https://github.com/kkabza/taxsale.git
cd taxsale
```

2. Set up environment:
```bash
# Copy example environment file
cp .env.example .env

# Switch to development environment
./switch_env.py development
```

3. Install dependencies:
```bash
# For production
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

4. Start the application:
```bash
# Run in development mode
./run_env.py development
```

## Error Monitoring with Sentry

This application uses Sentry.io for error monitoring and performance tracking. To enable Sentry:

1. Sign up for a free account at [Sentry.io](https://sentry.io)
2. Create a new Python Flask project in Sentry
3. Copy the DSN provided by Sentry
4. Add the DSN to your `.env` file:
```
SENTRY_DSN=your-sentry-dsn-here
```

To test Sentry integration:
- Visit `/debug-sentry` to send a test message to Sentry
- Visit `/debug-sentry-error` to trigger a test error

The application includes the following Sentry features:
- Automatic error capturing
- Performance monitoring
- Release tracking
- User context tracking
- Custom event capturing

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
Keith Kabza - [GitHub](https://github.com/kkabza)

Project Link: [https://github.com/kkabza/taxsale](https://github.com/kkabza/taxsale) 