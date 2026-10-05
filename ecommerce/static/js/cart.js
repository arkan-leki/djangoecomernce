document.addEventListener('alpine:init', () => {
    Alpine.data('cart', () => ({
      items: [],  // Placeholder for cart items
      options: [1, 2, 3, 4],  // Quantity options
      total: 0,
      count: 0,
      lastAdded: null,

      init() {
        this.loadCart();
      },

      async loadCart() {
        try {
          const response = await fetch(window.cartDataUrl);
          const data = await response.json();
          this.items = data.cart_items;
          this.total = data.cart_total;
          this.count = this.items.reduce((n, i) => n + (parseInt(i.qyt) || 0), 0);
        } catch (error) {
          console.error('Error loading cart:', error);
        }
      },

      // Add a product to the Django session cart (POST form-encoded to cart-add)
      async addItem(productId, productQuantity = 1, size = '', color = '') {
        const body = new FormData();
        body.append('product_id', productId);
        body.append('product_quantity', productQuantity);
        body.append('size', size);
        body.append('color', color);
        try {
          const response = await fetch(window.cartAddUrl, {
            method: 'POST',
            headers: { 'X-CSRFToken': window.csrfToken },
            body: body,
          });
          const data = await response.json();
          if (data.success) {
            this.count = data.cart_quantity;
            this.lastAdded = data.product_title;
            await this.loadCart();
          }
          return data;
        } catch (error) {
          console.error('Error adding to cart:', error);
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
          this.count = data.cart_quantity;
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
          this.count = data.cart_quantity;
        } catch (error) {
          console.error('Error deleting item:', error);
        }
      }
    }));
  });
