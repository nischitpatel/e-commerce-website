import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { fetchProductById } from '../services/api';
import Loader from '../components/Loader';
import { useCart } from '../context/CartContext';

export default function Product() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const { addToCart } = useCart();

  useEffect(() => {
    fetchProductById(id).then((data) => {
      setProduct(data);
      setLoading(false);
    });
  }, [id]);

  if (loading) return <Loader />;

  return (
    <div className="max-w-2xl mx-auto border p-4 rounded shadow">
      <img src={product.image} alt={product.name} className="w-full h-96 object-cover mb-4" />
      <h1 className="text-2xl font-bold">{product.name}</h1>
      <p className="mt-2">${product.price}</p>
      <p className="mt-2">{product.description}</p>
      <button
        onClick={() => addToCart(product)}
        className="mt-4 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
      >
        Add to Cart
      </button>
    </div>
  );
}
