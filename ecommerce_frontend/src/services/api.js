const mockProducts = [
    { id: 1, name: 'Product 1', price: 29.99, image: 'https://via.placeholder.com/300', description: 'Description of product 1' },
    { id: 2, name: 'Product 2', price: 49.99, image: 'https://via.placeholder.com/300', description: 'Description of product 2' },
    { id: 3, name: 'Product 3', price: 19.99, image: 'https://via.placeholder.com/300', description: 'Description of product 3' },
    { id: 4, name: 'Product 4', price: 29.99, image: 'https://via.placeholder.com/300', description: 'Description of product 1' },
    { id: 5, name: 'Product 5', price: 49.99, image: 'https://via.placeholder.com/300', description: 'Description of product 2' },
    { id: 6, name: 'Product 6', price: 19.99, image: 'https://via.placeholder.com/300', description: 'Description of product 3' },
    { id: 7, name: 'Product 7', price: 29.99, image: 'https://via.placeholder.com/300', description: 'Description of product 1' },
    { id: 8, name: 'Product 8', price: 49.99, image: 'https://via.placeholder.com/300', description: 'Description of product 2' },
    { id: 9, name: 'Product 9', price: 19.99, image: 'https://via.placeholder.com/300', description: 'Description of product 3' },
    { id: 10, name: 'Product 10', price: 29.99, image: 'https://via.placeholder.com/300', description: 'Description of product 1' },
    { id: 11, name: 'Product 11', price: 49.99, image: 'https://via.placeholder.com/300', description: 'Description of product 2' },
    { id: 12, name: 'Product 12', price: 19.99, image: 'https://via.placeholder.com/300', description: 'Description of product 3' },
    { id: 13, name: 'Product 13', price: 29.99, image: 'https://via.placeholder.com/300', description: 'Description of product 1' },
    { id: 14, name: 'Product 14', price: 49.99, image: 'https://via.placeholder.com/300', description: 'Description of product 2' },
    { id: 15, name: 'Product 15', price: 19.99, image: 'https://via.placeholder.com/300', description: 'Description of product 3' },
    { id: 16, name: 'Product 16', price: 29.99, image: 'https://via.placeholder.com/300', description: 'Description of product 1' },
    { id: 17, name: 'Product 17', price: 49.99, image: 'https://via.placeholder.com/300', description: 'Description of product 2' },
    { id: 18, name: 'Product 18', price: 19.99, image: 'https://via.placeholder.com/300', description: 'Description of product 3' },
];
  
  export async function fetchProducts() {
    return new Promise((resolve) => setTimeout(() => resolve(mockProducts), 500));
  }
  
  export async function fetchProductById(id) {
    return new Promise((resolve) =>
      setTimeout(() => resolve(mockProducts.find((p) => p.id === parseInt(id))), 500)
    );
  }
  