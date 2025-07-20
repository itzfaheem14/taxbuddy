// Hurray Cafe Frontend JavaScript

class HurrayCafeApp {
    constructor() {
        this.categories = [];
        this.currentCategory = null;
        this.init();
    }

    async init() {
        await this.loadCategories();
        this.setupEventListeners();
        this.renderCategories();
    }

    async loadCategories() {
        try {
            const response = await fetch('/api/categories');
            this.categories = await response.json();
        } catch (error) {
            console.error('Error loading categories:', error);
            // Fallback to default categories if API fails
            this.categories = this.getDefaultCategories();
        }
    }

    getDefaultCategories() {
        return [
            {
                id: 1,
                name: "Pizza",
                image: "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=300&h=300&fit=crop",
                description: "Delicious pizzas with fresh toppings",
                items: [
                    { name: "Margherita Pizza", price: "₹299", description: "Classic tomato and mozzarella" },
                    { name: "Pepperoni Pizza", price: "₹399", description: "Spicy pepperoni with cheese" },
                    { name: "Veggie Supreme", price: "₹349", description: "Fresh vegetables and cheese" }
                ]
            },
            {
                id: 2,
                name: "Desserts",
                image: "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=300&h=300&fit=crop",
                description: "Sweet treats to satisfy your cravings",
                items: [
                    { name: "Chocolate Cake", price: "₹150", description: "Rich chocolate cake with ganache" },
                    { name: "Cheesecake", price: "₹180", description: "Creamy New York style cheesecake" },
                    { name: "Tiramisu", price: "₹200", description: "Italian coffee-flavored dessert" }
                ]
            },
            {
                id: 3,
                name: "Chai",
                image: "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=300&h=300&fit=crop",
                description: "Traditional Indian tea varieties",
                items: [
                    { name: "Masala Chai", price: "₹50", description: "Spiced Indian tea with milk" },
                    { name: "Ginger Chai", price: "₹60", description: "Ginger-infused tea" },
                    { name: "Cardamom Chai", price: "₹55", description: "Cardamom flavored tea" }
                ]
            },
            {
                id: 4,
                name: "Mocktails",
                image: "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=300&h=300&fit=crop",
                description: "Refreshing non-alcoholic beverages",
                items: [
                    { name: "Virgin Mojito", price: "₹120", description: "Mint and lime mocktail" },
                    { name: "Pina Colada", price: "₹140", description: "Pineapple and coconut mocktail" },
                    { name: "Berry Blast", price: "₹130", description: "Mixed berry mocktail" }
                ]
            },
            {
                id: 5,
                name: "Ice Cream",
                image: "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=300&h=300&fit=crop",
                description: "Creamy and delicious ice cream",
                items: [
                    { name: "Vanilla", price: "₹80", description: "Classic vanilla ice cream" },
                    { name: "Chocolate", price: "₹90", description: "Rich chocolate ice cream" },
                    { name: "Strawberry", price: "₹85", description: "Fresh strawberry ice cream" }
                ]
            },
            {
                id: 6,
                name: "Shakes",
                image: "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=300&h=300&fit=crop",
                description: "Thick and creamy milkshakes",
                items: [
                    { name: "Chocolate Shake", price: "₹120", description: "Rich chocolate milkshake" },
                    { name: "Strawberry Shake", price: "₹110", description: "Fresh strawberry milkshake" },
                    { name: "Oreo Shake", price: "₹130", description: "Oreo cookie milkshake" }
                ]
            },
            {
                id: 7,
                name: "Cold Coffee",
                image: "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=300&h=300&fit=crop",
                description: "Refreshing cold coffee drinks",
                items: [
                    { name: "Dalgona Coffee", price: "₹150", description: "Whipped coffee over milk" },
                    { name: "Iced Latte", price: "₹140", description: "Cold coffee with milk" },
                    { name: "Cold Brew", price: "₹160", description: "Smooth cold brewed coffee" }
                ]
            },
            {
                id: 8,
                name: "Beer",
                image: "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=300&h=300&fit=crop",
                description: "Refreshing beer varieties",
                items: [
                    { name: "Lager", price: "₹200", description: "Crisp and refreshing lager" },
                    { name: "Wheat Beer", price: "₹220", description: "Smooth wheat beer" },
                    { name: "IPA", price: "₹250", description: "Hoppy India Pale Ale" }
                ]
            },
            {
                id: 9,
                name: "Chilli",
                image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=300&fit=crop",
                description: "Spicy and flavorful chili dishes",
                items: [
                    { name: "Beef Chili", price: "₹180", description: "Spicy beef chili with beans" },
                    { name: "Veg Chili", price: "₹160", description: "Vegetarian chili with vegetables" },
                    { name: "Chili Cheese Fries", price: "₹200", description: "Fries topped with chili and cheese" }
                ]
            },
            {
                id: 10,
                name: "French Fries",
                image: "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=300&h=300&fit=crop",
                description: "Crispy and golden French fries",
                items: [
                    { name: "Classic Fries", price: "₹100", description: "Crispy golden French fries" },
                    { name: "Cheese Fries", price: "₹130", description: "Fries topped with melted cheese" },
                    { name: "Spicy Fries", price: "₹120", description: "Fries with spicy seasoning" }
                ]
            },
            {
                id: 11,
                name: "Corn",
                image: "https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=300&h=300&fit=crop",
                description: "Fresh and sweet corn dishes",
                items: [
                    { name: "Grilled Corn", price: "₹80", description: "Charred corn on the cob" },
                    { name: "Corn Salad", price: "₹90", description: "Fresh corn salad with vegetables" },
                    { name: "Corn Soup", price: "₹110", description: "Creamy corn soup" }
                ]
            },
            {
                id: 12,
                name: "Sandwich",
                image: "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=300&h=300&fit=crop",
                description: "Fresh and delicious sandwiches",
                items: [
                    { name: "Club Sandwich", price: "₹140", description: "Triple-decker club sandwich" },
                    { name: "Veg Sandwich", price: "₹120", description: "Fresh vegetable sandwich" },
                    { name: "Chicken Sandwich", price: "₹160", description: "Grilled chicken sandwich" }
                ]
            }
        ];
    }

    renderCategories() {
        const container = document.getElementById('menu-categories');
        container.innerHTML = '';

        this.categories.forEach(category => {
            const card = this.createCategoryCard(category);
            container.appendChild(card);
        });
    }

    createCategoryCard(category) {
        const card = document.createElement('div');
        card.className = 'category-card bg-white rounded-lg shadow-md overflow-hidden cursor-pointer';
        card.innerHTML = `
            <div class="relative">
                <img src="${category.image}" alt="${category.name}" 
                     class="category-image w-full h-32 object-cover">
                <div class="absolute inset-0 bg-black bg-opacity-20 opacity-0 hover:opacity-100 transition-opacity"></div>
            </div>
            <div class="p-4">
                <h3 class="font-bold text-cafe-dark mb-2">${category.name}</h3>
                <button class="explore-btn text-sm text-cafe-dark hover:text-cafe-yellow font-medium">
                    Explore >
                </button>
            </div>
        `;

        card.addEventListener('click', () => this.openCategoryModal(category));
        return card;
    }

    openCategoryModal(category) {
        this.currentCategory = category;
        const modal = document.getElementById('category-modal');
        const title = document.getElementById('modal-title');
        const content = document.getElementById('modal-content');

        title.textContent = category.name;
        content.innerHTML = this.createModalContent(category);

        modal.classList.remove('hidden');
        modal.classList.add('modal-enter');
    }

    createModalContent(category) {
        return `
            <div class="space-y-4">
                <div class="text-center">
                    <img src="${category.image}" alt="${category.name}" 
                         class="w-full h-48 object-cover rounded-lg mb-4">
                    <p class="text-gray-600">${category.description}</p>
                </div>
                <div class="space-y-3">
                    <h4 class="font-bold text-cafe-dark">Menu Items:</h4>
                    ${category.items.map(item => `
                        <div class="border-b border-gray-200 pb-3">
                            <div class="flex justify-between items-start">
                                <div>
                                    <h5 class="font-semibold text-cafe-dark">${item.name}</h5>
                                    <p class="text-sm text-gray-600">${item.description}</p>
                                </div>
                                <span class="font-bold text-cafe-yellow">${item.price}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
                <div class="pt-4">
                    <button class="w-full bg-cafe-yellow text-cafe-dark font-bold py-3 px-4 rounded-lg hover:bg-yellow-400 transition-colors">
                        Order Now
                    </button>
                </div>
            </div>
        `;
    }

    closeModal() {
        const modal = document.getElementById('category-modal');
        modal.classList.add('modal-exit');
        setTimeout(() => {
            modal.classList.remove('modal-exit', 'modal-enter');
            modal.classList.add('hidden');
        }, 300);
    }

    setupEventListeners() {
        // Close modal button
        document.getElementById('close-modal').addEventListener('click', () => {
            this.closeModal();
        });

        // Close modal when clicking outside
        document.getElementById('category-modal').addEventListener('click', (e) => {
            if (e.target.id === 'category-modal') {
                this.closeModal();
            }
        });

        // Close modal with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });

        // Notification bell
        document.querySelector('button svg').parentElement.addEventListener('click', () => {
            this.showNotification('Notifications feature coming soon!');
        });
    }

    showNotification(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'fixed top-20 right-4 bg-cafe-dark text-white px-4 py-2 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform';
        notification.textContent = message;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new HurrayCafeApp();
});