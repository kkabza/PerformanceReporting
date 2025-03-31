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

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Start the development server:
```bash
./start.sh
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