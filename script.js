// Hurray Cafe JavaScript
class HurrayCafe {
    constructor() {
        this.menuData = null;
        this.currentCategory = null;
        this.cart = [];
        this.init();
    }

    async init() {
        this.showLoading();
        await this.loadMenuData();
        this.renderCategories();
        this.setupEventListeners();
        this.hideLoading();
    }

    async loadMenuData() {
        try {
            const response = await fetch('menu_data.json');
            this.menuData = await response.json();
        } catch (error) {
            console.error('Failed to load menu data:', error);
            this.showError('Failed to load menu data. Please try again.');
        }
    }

    renderCategories() {
        const menuGrid = document.getElementById('menu-grid');
        
        if (!this.menuData || !this.menuData.categories) {
            this.showError('No menu data available');
            return;
        }

        menuGrid.innerHTML = this.menuData.categories.map(category => `
            <div class="category-card bg-white rounded-xl shadow-sm overflow-hidden cursor-pointer transform hover:scale-105 transition-all duration-300" 
                 data-category="${category.id}">
                <div class="category-image h-32 bg-gray-200 relative overflow-hidden">
                    <img src="${category.image}" 
                         alt="${category.name}" 
                         class="w-full h-full object-cover"
                         onerror="this.src='https://via.placeholder.com/300x200/f3f4f6/9ca3af?text=${category.name}'"
                         loading="lazy">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
                </div>
                <div class="p-4">
                    <h3 class="font-semibold text-gray-900 mb-2">${category.name}</h3>
                    <button class="explore-btn flex items-center text-sm text-gray-600 hover:text-gray-900 transition-colors duration-200">
                        <span>Explore</span>
                        <i class="fas fa-chevron-right ml-2 text-xs"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }

    setupEventListeners() {
        // Category card clicks
        document.addEventListener('click', (e) => {
            const categoryCard = e.target.closest('.category-card');
            if (categoryCard) {
                const categoryId = categoryCard.dataset.category;
                this.openCategoryModal(categoryId);
            }

            // Close modal
            if (e.target.id === 'close-modal' || e.target.closest('#close-modal')) {
                this.closeCategoryModal();
            }

            // Close modal when clicking outside
            if (e.target.id === 'category-modal') {
                this.closeCategoryModal();
            }

            // Add to cart buttons
            if (e.target.closest('.add-to-cart-btn')) {
                const itemId = e.target.closest('.add-to-cart-btn').dataset.itemId;
                this.addToCart(itemId);
            }
        });

        // Escape key to close modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeCategoryModal();
            }
        });

        // Prevent modal content clicks from closing modal
        document.addEventListener('click', (e) => {
            if (e.target.closest('.modal-content')) {
                e.stopPropagation();
            }
        });
    }

    openCategoryModal(categoryId) {
        const category = this.menuData.categories.find(cat => cat.id === categoryId);
        if (!category) return;

        this.currentCategory = category;
        
        const modal = document.getElementById('category-modal');
        const modalTitle = document.getElementById('modal-title');
        const modalContent = document.getElementById('modal-content');

        modalTitle.textContent = category.name;
        
        modalContent.innerHTML = `
            <div class="mb-6">
                <img src="${category.image}" 
                     alt="${category.name}" 
                     class="w-full h-48 object-cover rounded-lg"
                     onerror="this.src='https://via.placeholder.com/400x200/f3f4f6/9ca3af?text=${category.name}'">
                <p class="text-gray-600 mt-3">${category.description}</p>
            </div>
            
            <div class="space-y-4">
                ${category.items.map(item => `
                    <div class="menu-item bg-gray-50 rounded-lg p-4 flex items-center space-x-4 hover:bg-gray-100 transition-colors duration-200">
                        <img src="${item.image}" 
                             alt="${item.name}" 
                             class="w-16 h-16 object-cover rounded-lg flex-shrink-0"
                             onerror="this.src='https://via.placeholder.com/64x64/f3f4f6/9ca3af?text=Food'">
                        <div class="flex-1">
                            <h4 class="font-semibold text-gray-900">${item.name}</h4>
                            <p class="text-sm text-gray-600 mt-1">${item.description}</p>
                            <div class="flex items-center justify-between mt-3">
                                <span class="text-lg font-bold text-orange-600">$${item.price.toFixed(2)}</span>
                                <button class="add-to-cart-btn bg-orange-500 text-white px-4 py-2 rounded-lg text-sm hover:bg-orange-600 transition-colors duration-200 flex items-center space-x-2" 
                                        data-item-id="${item.id}">
                                    <i class="fas fa-plus text-xs"></i>
                                    <span>Add</span>
                                </button>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        
        // Add animation class
        setTimeout(() => {
            modal.querySelector('.bg-white').classList.add('animate-slide-up');
        }, 10);
    }

    closeCategoryModal() {
        const modal = document.getElementById('category-modal');
        modal.classList.add('hidden');
        document.body.style.overflow = '';
        this.currentCategory = null;
    }

    addToCart(itemId) {
        if (!this.currentCategory) return;

        const item = this.currentCategory.items.find(item => item.id === itemId);
        if (!item) return;

        // Check if item already exists in cart
        const existingItem = this.cart.find(cartItem => cartItem.id === itemId);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.cart.push({
                ...item,
                quantity: 1,
                categoryName: this.currentCategory.name
            });
        }

        this.showAddToCartFeedback(item.name);
        this.updateCartUI();
    }

    showAddToCartFeedback(itemName) {
        // Create a temporary notification
        const notification = document.createElement('div');
        notification.className = 'fixed top-20 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-all duration-300';
        notification.innerHTML = `
            <div class="flex items-center space-x-2">
                <i class="fas fa-check-circle"></i>
                <span>${itemName} added to cart!</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translate(-50%, 0)';
        }, 10);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translate(-50%, -100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    updateCartUI() {
        // This would update cart count in header, cart total, etc.
        const cartCount = this.cart.reduce((total, item) => total + item.quantity, 0);
        console.log(`Cart items: ${cartCount}`);
        console.log('Cart contents:', this.cart);
    }

    showLoading() {
        document.getElementById('loading').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loading').classList.add('hidden');
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'fixed top-20 left-1/2 transform -translate-x-1/2 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        errorDiv.innerHTML = `
            <div class="flex items-center space-x-2">
                <i class="fas fa-exclamation-circle"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(errorDiv);
        
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    // Utility method to get cart total
    getCartTotal() {
        return this.cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    }

    // Utility method to clear cart
    clearCart() {
        this.cart = [];
        this.updateCartUI();
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.hurrayCafe = new HurrayCafe();
});

// Add some utility functions for potential future use
const utils = {
    formatPrice: (price) => `$${price.toFixed(2)}`,
    
    formatTime: (date) => {
        return new Intl.DateTimeFormat('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        }).format(date);
    },
    
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Service Worker registration for potential PWA features
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}