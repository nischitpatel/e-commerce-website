// Replace these URLs with your Django backend endpoints
const API_URL = 'http://localhost:8000/api/users';

export async function loginUser(username, password) {
  const res = await fetch(`${API_URL}/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error('Invalid credentials');
  return res.json();
}

export async function registerUser(name, email, password) {
  const res = await fetch(`${API_URL}/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password }),
  });
  if (!res.ok) throw new Error('Registration failed');
  return res.json();
}

export async function getUserProfile(token) {
    // `${API_URL}/profile/`
    const res = await fetch('http://localhost:8000/api/users/profile/', {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`, // send JWT token
      },
    });
    if (!res.ok) throw new Error('Failed to fetch user profile');
    return res.json(); // expected: { user: {...} }
  }