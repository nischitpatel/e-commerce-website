import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useUser } from '../context/UserContext';

export default function Navbar() {
  const { cart } = useCart();
  const { user, logout } = useUser();

  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-between items-center">
      <Link to="/" className="font-bold text-xl">E-Shop</Link>
      <div className="space-x-4">
        <Link to="/">Home</Link>
        <Link to="/cart">Cart ({cart.length})</Link>
        {user ? (
          <>
            <span>Hello, {localStorage.user}</span>
            <button onClick={logout} className="ml-2 bg-red-600 py-1 px-3 rounded hover:bg-red-700">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
