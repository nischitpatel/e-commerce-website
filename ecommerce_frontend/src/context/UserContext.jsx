import { createContext, useState, useContext, useEffect } from 'react';
import { loginUser, registerUser, getUserProfile } from '../services/auth';

const UserContext = createContext();

export function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  // On app load, check if token exists
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Fetch user info using token
      getUserProfile(token).then((data) => {
        setUser(data.user);
      }).catch(() => {
        localStorage.removeItem('token'); // remove invalid token
      });
    }
  }, []);

  const login = async (username, password) => {
    setLoading(true);
    try {
      const data = await loginUser(username, password);
      localStorage.setItem('token', data.access);
      setUser(data.user);
    } catch (error) {
      console.error('Login failed:', error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (username, password) => {
    setLoading(true);
    try {
      const data = await registerUser(username, password);
      setUser(data.user);
      localStorage.setItem('token', data.access);
    } catch (error) {
      console.error('Registration failed:', error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
  };

  return (
    <UserContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </UserContext.Provider>
  );
}

export const useUser = () => useContext(UserContext);
