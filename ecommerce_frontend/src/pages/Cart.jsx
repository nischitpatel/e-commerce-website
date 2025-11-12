import { useCart } from '../context/CartContext';
import { Link } from 'react-router-dom';

export default function Cart() {
  const { cart, removeFromCart, clearCart } = useCart();

  if (cart.length === 0) {
    return <p>Your cart is empty. <Link to="/">Go shopping</Link></p>;
  }

  const total = cart.reduce((sum, item) => sum + item.price, 0);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Your Cart</h1>
      <ul className="space-y-2">
        {cart.map((item) => (
          <li key={item.id} className="flex justify-between border p-2 rounded">
            <span>{item.name}</span>
            <span>${item.price}</span>
            <button onClick={() => removeFromCart(item.id)} className="text-red-600">Remove</button>
          </li>
        ))}
      </ul>
      <p className="mt-4 font-bold">Total: ${total}</p>
      <div className="mt-4 space-x-2">
        <button onClick={clearCart} className="bg-red-600 text-white py-2 px-4 rounded">Clear Cart</button>
        <Link to="/checkout" className="bg-blue-600 text-white py-2 px-4 rounded">Checkout</Link>
      </div>
    </div>
  );
}
