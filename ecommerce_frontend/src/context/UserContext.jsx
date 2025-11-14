import { createContext, useState, useContext, useEffect } from 'react';
import { loginUser, registerUser, getUserProfile } from '../services/auth';

const UserContext = createContext();

export function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  // On app load, check if token exists
  useEffect(() => {
    const token = localStorage.getItem('access');
    if (token) {
      // Fetch user info using token
      getUserProfile(token).then((data) => {
        setUser(data.user);
      }).catch(() => {
        localStorage.removeItem('access'); // remove invalid token
      });
    }
  }, []);

  const login = async (username, password) => {
    setLoading(true);
    try {
      const data = await loginUser(username, password);
      localStorage.setItem('access', data.access);
      localStorage.setItem('refresh', data.refresh);
      localStorage.setItem('user', data.user.username);
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
      localStorage.setItem('access', data.access);
      localStorage.setItem('refresh', data.refresh);
      localStorage.setItem('user', data.user);
    } catch (error) {
      console.error('Registration failed:', error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('user');
  };

  return (
    <UserContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </UserContext.Provider>
  );
}

export const useUser = () => useContext(UserContext);

// import { createContext, useState, useEffect } from "react";
// import { loginUser, registerUser, getUserProfile } from "../services/auth";

// export const UserContext = createContext();

// export function UserProvider({ children }) {
//   const [user, setUser] = useState(null);
//   const [loading, setLoading] = useState(true);

//   // Load user on page refresh
//   useEffect(() => {
//     const token = localStorage.getItem("token");
//     if (token) {
//       getUserProfile(token)
//         .then(data => {
//           setUser(data.user);
//         })
//         .catch(() => {
//           setUser(null);
//         })
//         .finally(() => {
//           setLoading(false);
//         });
//     } else {
//       setLoading(false);
//     }
//   }, []);

//   // LOGIN FUNCTION
//   const login = async (username, password) => {
//     setLoading(true);
//     try {
//       const data = await loginUser(username, password);

//       // Save tokens
//       localStorage.setItem("token", data.access);
//       localStorage.setItem("refresh", data.refresh);

//       // Save user
//       localStorage.setItem("user", JSON.stringify(data.user));
//       setUser(data.user);

//       return data;
//     } catch (error) {
//       console.error("Login failed:", error);
//       throw error;
//     } finally {
//       setLoading(false);
//     }
//   };

//   // REGISTER FUNCTION
//   const register = async (username, email, password) => {
//     setLoading(true);
//     try {
//       const data = await registerUser(username, email, password);

//       // Save tokens
//       localStorage.setItem("token", data.access);
//       localStorage.setItem("refresh", data.refresh);

//       // Save user
//       localStorage.setItem("user", JSON.stringify(data.user));
//       setUser(data.user);

//       return data;
//     } catch (error) {
//       console.error("Registration failed:", error);
//       throw error;
//     } finally {
//       setLoading(false);
//     }
//   };

//   // LOGOUT FUNCTION
//   const logout = () => {
//     localStorage.removeItem("token");
//     localStorage.removeItem("refresh");
//     localStorage.removeItem("user");
//     setUser(null);
//   };

//   return (
//     <UserContext.Provider
//       value={{
//         user,
//         loading,
//         login,
//         register,
//         logout,
//         setUser,
//       }}
//     >
//       {children}
//     </UserContext.Provider>
//   );
// }

// export function useUser() {
//   return useContext(UserContext);
// }