# 🎉 Hurray Cafe - Digital Menu & Ordering System

A modern, responsive web application for cafe menu browsing and online ordering, built with HTML, CSS, JavaScript, Tailwind CSS, JSON, and Python Flask.

![Hurray Cafe Screenshot](https://via.placeholder.com/800x400/f97316/ffffff?text=Hurray+Cafe+-+Scan.+Order.+Enjoy.)

## ✨ Features

- **📱 Mobile-First Design** - Optimized for mobile devices with responsive layout
- **🍕 Menu Categories** - Pizza, Desserts, Chai, Mocktails, Ice Cream, Shakes, Cold Coffee, Beer, Chili, French Fries, Corn, and Sandwiches
- **🛒 Shopping Cart** - Add items to cart with quantity management
- **💫 Smooth Animations** - Beautiful transitions and loading animations
- **🎨 Modern UI** - Clean design with Tailwind CSS
- **⚡ Fast Loading** - Optimized images and lazy loading
- **🔄 Real-time Updates** - Dynamic menu loading from JSON data
- **📊 Order Management** - Complete order processing system

## 🛠️ Tech Stack

### Frontend
- **HTML5** - Semantic markup structure
- **CSS3** - Custom styles and animations
- **JavaScript (ES6+)** - Interactive functionality
- **Tailwind CSS** - Utility-first CSS framework
- **Font Awesome** - Icons and visual elements

### Backend
- **Python 3.8+** - Server-side programming
- **Flask** - Lightweight web framework
- **Flask-CORS** - Cross-origin resource sharing
- **JSON** - Data storage and API responses

### Data Storage
- **JSON Files** - Menu data storage
- **In-Memory Storage** - Session and cart management (development)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser

### Installation

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd hurray-cafe
   
   # Or download and extract the files
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Flask server**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
hurray-cafe/
├── index.html          # Main HTML file
├── styles.css          # Custom CSS styles
├── script.js           # JavaScript functionality
├── menu_data.json      # Menu items and categories
├── app.py              # Flask backend server
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## 🎯 Usage

### For Customers
1. **Browse Menu** - Scroll through various food categories
2. **View Items** - Click on any category to see detailed items
3. **Add to Cart** - Click the "Add" button on items you want
4. **Place Order** - Complete your order through the cart system

### For Developers
1. **Customize Menu** - Edit `menu_data.json` to update menu items
2. **Modify Styles** - Update `styles.css` or use Tailwind classes
3. **Add Features** - Extend `script.js` for new functionality
4. **API Integration** - Use Flask endpoints for data management

## 🔧 API Endpoints

### Menu Management
```
GET  /api/menu                    # Get complete menu
GET  /api/categories              # Get all categories
GET  /api/categories/<id>         # Get specific category
GET  /api/items/<id>              # Get specific item
```

### Cart Management
```
GET  /api/cart                    # Get cart contents
POST /api/cart                    # Add item to cart
DELETE /api/cart/<session_id>     # Clear cart
PUT  /api/cart/<session_id>/items/<item_id>  # Update item
```

### Order Management
```
GET  /api/orders                  # Get all orders
POST /api/orders                  # Create new order
GET  /api/orders/<id>             # Get specific order
PUT  /api/orders/<id>/status      # Update order status
```

### System
```
GET  /api/health                  # Health check
```

## 🎨 Customization

### Menu Items
Edit `menu_data.json` to add/remove categories and items:

```json
{
  "categories": [
    {
      "id": "pizza",
      "name": "Pizza",
      "image": "https://your-image-url.com/pizza.jpg",
      "description": "Authentic wood-fired pizzas",
      "items": [
        {
          "id": "margherita",
          "name": "Margherita Pizza",
          "price": 12.99,
          "description": "Classic tomato sauce and mozzarella",
          "image": "https://your-image-url.com/margherita.jpg"
        }
      ]
    }
  ]
}
```

### Styling
- **Colors**: Modify Tailwind classes or CSS custom properties
- **Fonts**: Update font imports in HTML head section
- **Layout**: Adjust grid and flexbox classes
- **Animations**: Customize CSS animations in `styles.css`

### Functionality
- **Cart Logic**: Modify cart management in `script.js`
- **API Calls**: Update endpoint URLs and request handling
- **UI Components**: Add new modals, forms, or interactive elements

## 🔧 Development

### Local Development
```bash
# Start development server with auto-reload
python app.py

# The server will automatically restart when you make changes
```

### Adding Features
1. **New Menu Category**: Add to `menu_data.json`
2. **UI Components**: Create in `script.js` and style with CSS
3. **API Endpoints**: Add routes in `app.py`
4. **Styling**: Use Tailwind classes or custom CSS

### Testing
- **Frontend**: Open browser developer tools
- **Backend**: Test API endpoints with tools like Postman
- **Mobile**: Use browser responsive design mode

## 📱 Mobile Optimization

- **Responsive Grid**: Adapts to different screen sizes
- **Touch-Friendly**: Large buttons and touch targets
- **Fast Loading**: Optimized images and lazy loading
- **Smooth Scrolling**: Native mobile scroll behavior
- **Offline-Ready**: Service worker support (optional)

## 🚀 Production Deployment

### Heroku
```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export PORT=5000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Tailwind CSS** - For the amazing utility-first CSS framework
- **Font Awesome** - For the beautiful icons
- **Unsplash** - For high-quality placeholder images
- **Flask Community** - For the excellent web framework

## 📞 Support

If you have any questions or need help:
- Check the documentation above
- Review the code comments
- Open an issue for bugs or feature requests

---

**Made with ❤️ for Hurray Cafe**