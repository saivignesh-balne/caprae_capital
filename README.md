# Caprae Capital - AI Lead Generation Tool

A powerful AI-powered lead generation and analysis tool that helps identify and score potential business leads from LinkedIn profiles.

## Features

- 🤖 Advanced AI-powered lead scoring
- 📊 Comprehensive profile analysis
- 💡 Actionable insights and recommendations
- 📈 Multiple export formats (CSV, JSON, Excel)
- 🔒 Secure LinkedIn integration
- 🎨 Modern, responsive UI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/caprae-capital.git
cd caprae-capital
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
.env
# Edit .env with your credentials and settings
```

## Usage

1. Start the application:
```bash
python web_app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Connect your LinkedIn account and start analyzing profiles!

## Configuration

The application can be configured using environment variables in the `.env` file:

- `FLASK_ENV`: Set to 'development' or 'production'
- `FLASK_DEBUG`: Enable/disable debug mode
- `LINKEDIN_EMAIL`: Your LinkedIn account email
- `LINKEDIN_PASSWORD`: Your LinkedIn account password

## Security

- All sessions are secured with HTTPS
- Cookies are protected with secure flags
- Input validation and sanitization
- Rate limiting and request size limits
- Secure credential storage

## Export Formats

- CSV: Spreadsheet-friendly format
- JSON: Full data export with all details
- Excel: Formatted workbook with multiple sheets

## Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Troubleshooting

Common issues and solutions:

1. LinkedIn Login Issues:
   - Ensure your credentials are correct in `.env`
   - Check if your account has 2FA enabled
   - Try logging out and back in

2. Scraping Problems:
   - Verify the profile URL format
   - Check your internet connection
   - Ensure you're not rate limited

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue if needed

## Credits

Built with:
- Flask
- Selenium
- scikit-learn
- TailwindCSS
- And more great open source projects!