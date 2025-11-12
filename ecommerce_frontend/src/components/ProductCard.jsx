import { Link } from 'react-router-dom';

export default function ProductCard({ product }) {
  return (
    <div className="border rounded p-4 hover:shadow-lg transition">
      <Link to={`/product/${product.id}`}>
        <img src={product.image} alt={product.name} className="w-full h-48 object-cover mb-2" />
        <h2 className="font-bold">{product.name}</h2>
      </Link>
      <p>${product.price}</p>
    </div>
  );
}
