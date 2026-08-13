"use client"
import React, { createContext, useContext, useState, useEffect, useRef } from 'react';
import api from '../lib/api';
import { useRouter } from 'next/navigation';

interface User {
  id: string;
  email: string;
  full_name: string | null;
}

interface AuthContextType {
  user: User | null;
  login: (token: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const initialized = useRef(false);

  // Initialize on mount
  useEffect(() => {
    const initAuth = async () => {
      try {
        // Check if we have a token
        const token = localStorage.getItem('token');
        
        if (!token) {
          setLoading(false);
          return;
        }

        // Try to fetch user
        try {
          const response = await api.get('/auth/me');
          const userData = response.data;
          
          if (userData && userData.id) {
            setUser(userData);
          } else {
            localStorage.removeItem('token');
          }
        } catch (fetchError) {
          console.error("Failed to fetch user:", fetchError);
          localStorage.removeItem('token');
        }
      } finally {
        setLoading(false);
      }
    };

    if (!initialized.current) {
      initialized.current = true;
      initAuth();
    }
  }, []);

  const login = async (token: string) => {
    try {
      localStorage.setItem('token', token);
      
      // Add delay to let interceptor pick up the token
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const response = await api.get('/auth/me');
      const userData = response.data;
      
      if (userData && userData.id) {
        setUser(userData);
        // Redirect after state is set
        setTimeout(() => router.push('/dashboard'), 100);
      } else {
        throw new Error('No user data received');
      }
    } catch (error) {
      console.error("Login error:", error);
      localStorage.removeItem('token');
      setUser(null);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout');
    } catch (e) {
      console.error("Logout error:", e);
    }
    localStorage.removeItem('token');
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
