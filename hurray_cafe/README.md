# Hurray Cafe - Web Application

A modern, responsive web application for Hurray Cafe featuring a beautiful menu interface with interactive category browsing and ordering capabilities.

## Features

- 🍕 **Interactive Menu Categories**: Browse through 12 different food and beverage categories
- 📱 **Responsive Design**: Mobile-first design that works on all devices
- 🎨 **Modern UI**: Clean, modern interface with Tailwind CSS
- 🔍 **Search Functionality**: Search through menu items
- 📋 **Order System**: Place orders through the web interface
- 🎯 **Real-time Updates**: Dynamic content loading with JavaScript
- 🌐 **RESTful API**: Backend API for data management

## Menu Categories

1. **Pizza** - Delicious pizzas with fresh toppings
2. **Desserts** - Sweet treats and pastries
3. **Chai** - Traditional Indian tea varieties
4. **Mocktails** - Refreshing non-alcoholic beverages
5. **Ice Cream** - Creamy and delicious ice cream
6. **Shakes** - Thick and creamy milkshakes
7. **Cold Coffee** - Refreshing cold coffee drinks
8. **Beer** - Refreshing beer varieties
9. **Chilli** - Spicy and flavorful chili dishes
10. **French Fries** - Crispy and golden French fries
11. **Corn** - Fresh and sweet corn dishes
12. **Sandwich** - Fresh and delicious sandwiches

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Tailwind CSS
- **Backend**: Python Flask
- **Data**: JSON
- **Images**: Unsplash (high-quality food photography)

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download

```bash
# If you have the files locally, navigate to the hurray_cafe directory
cd hurray_cafe
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
# Start the Flask development server
python app.py
```

### Step 4: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
hurray_cafe/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/
│   └── menu_categories.json    # Menu data in JSON format
├── static/
│   ├── css/
│   │   └── style.css          # Custom CSS styles
│   └── js/
│       └── app.js             # Frontend JavaScript
└── templates/
    └── index.html             # Main HTML template
```

## API Endpoints

The application provides the following REST API endpoints:

- `GET /api/categories` - Get all menu categories
- `GET /api/categories/<id>` - Get specific category by ID
- `GET /api/restaurant-info` - Get restaurant information
- `GET /api/search?q=<query>` - Search menu items
- `POST /api/order` - Place a new order
- `GET /api/health` - Health check endpoint

## Customization

### Adding New Menu Items

1. Edit `data/menu_categories.json`
2. Add new items to existing categories or create new categories
3. Follow the existing JSON structure

### Modifying Styles

1. Edit `static/css/style.css` for custom styles
2. Modify Tailwind classes in `templates/index.html`
3. Update Tailwind configuration in the HTML head section

### Changing Images

1. Replace image URLs in `data/menu_categories.json`
2. Use high-quality images (recommended: 300x300px for category images, 200x200px for item images)
3. Ensure images are publicly accessible

## Features in Detail

### Frontend Features

- **Responsive Grid Layout**: 2-column grid that adapts to screen size
- **Interactive Cards**: Hover effects and smooth transitions
- **Modal Windows**: Detailed category views with item listings
- **Search Functionality**: Real-time search through menu items
- **Notification System**: Toast notifications for user feedback
- **Keyboard Navigation**: ESC key to close modals
- **Loading States**: Fallback content if API is unavailable

### Backend Features

- **RESTful API**: Clean, RESTful endpoints
- **Error Handling**: Comprehensive error handling and logging
- **Data Validation**: Input validation for orders
- **Health Monitoring**: Health check endpoint
- **Static File Serving**: Efficient static file delivery

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development

### Running in Development Mode

```bash
python app.py
```

The application will run in debug mode with auto-reload enabled.

### Production Deployment

For production deployment, consider:

1. Using a production WSGI server (Gunicorn, uWSGI)
2. Setting up a reverse proxy (Nginx)
3. Configuring environment variables
4. Setting up a database for order management
5. Implementing user authentication
6. Adding SSL/TLS certificates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please contact:
- Email: info@hurraycafe.com
- Phone: 8008978656
- Address: 2nd Floor, Badshahi Sai Square, Civil Line Road, Irrigation, Panna, Madhya Pradesh - 488001

---

**Designed by Fintness** 🎨