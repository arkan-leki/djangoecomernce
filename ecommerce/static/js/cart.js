document.addEventListener('alpine:init', () => {
    Alpine.data('cart', () => ({
      items: [],  // Placeholder for cart items
      options: [1, 2, 3, 4],  // Quantity options
      total: 0,
  
      init() {
        this.loadCart();
      },
  
      async loadCart() {
        try {
          const response = await fetch(window.cartDataUrl);
          const data = await response.json();
          this.items = data.cart_items;
          this.total = data.cart_total;
        } catch (error) {
          console.error('Error loading cart:', error);
        }
      },
  
      async updateQuantity(item) {
        try {
          const response = await fetch(window.cartUpdateUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': window.csrfToken,
            },
            body: JSON.stringify({
              cart_item_id: item.id,
              product_quantity: item.qyt,
            }),
          });
          const data = await response.json();
          this.total = data.cart_total;
        } catch (error) {
          console.error('Error updating quantity:', error);
        }
      },
  
      async deleteItem(itemId) {
        try {
          const response = await fetch(window.cartDeleteUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': window.csrfToken,
            },
            body: JSON.stringify({
              cart_item_id: itemId,
            }),
          });
          const data = await response.json();
          this.items = this.items.filter(item => item.id !== itemId);
          this.total = data.cart_total;
        } catch (error) {
          console.error('Error deleting item:', error);
        }
      }
    }));
  });
  