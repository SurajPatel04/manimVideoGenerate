import React, { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import axios from 'axios';
import type { LoginResponse, SignupResponse } from '@/types/api';

interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
}

interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
}

interface AuthContextType {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  signup: (userData: SignupData) => Promise<any>;
  logout: () => void;
  loading: boolean;
}

interface SignupData {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [tokens, setTokens] = useState<AuthTokens | null>(null);
  const [loading, setLoading] = useState(false);

  // Token management utilities
  const saveTokensToStorage = (authTokens: AuthTokens) => {
    localStorage.setItem('accessToken', authTokens.accessToken);
    localStorage.setItem('refreshToken', authTokens.refreshToken);
    localStorage.setItem('tokenType', authTokens.tokenType);
    setTokens(authTokens);
  };

  const clearTokensFromStorage = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('tokenType');
    setTokens(null);
  };

  const getStoredTokens = (): AuthTokens | null => {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');
    const tokenType = localStorage.getItem('tokenType');

    if (accessToken && refreshToken && tokenType) {
      return { accessToken, refreshToken, tokenType };
    }
    return null;
  };

  const login = async (email: string, password: string): Promise<boolean> => {
    setLoading(true);
    try {
      // Make API call to login endpoint
      const response = await axios.post<LoginResponse>('/api/user/login', {
        email,
        password,
      }, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 10000,
      });
      
      // Extract tokens and user data from response
      const { accessToken, refreshToken, tokenType, email: userEmail, firstName, lastName, userId } = response.data;
      
      // Save tokens to localStorage and state
      const authTokens: AuthTokens = { accessToken, refreshToken, tokenType };
      saveTokensToStorage(authTokens);
      
      // Create user object from response data
      const userData: User = {
        id: userId,
        email: userEmail,
        firstName,
        lastName: lastName || '',
      };
      
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      return true;
    } catch (error: any) {
      console.error('Login failed:', error);
      // Handle specific error messages
      if (error.response?.status === 401) {
        throw new Error('Invalid email or password');
      }
      throw new Error(error.response?.data?.detail || error.response?.data?.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const signup = async (userData: SignupData): Promise<any> => {
    setLoading(true);
    try {
      // Make API call to signup endpoint
      const response = await axios.post('/api/user/signUp', {
        firstName: userData.firstName,
        lastName: userData.lastName || '', // lastName is optional
        email: userData.email,
        password: userData.password,
      }, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 10000,
      });

      // If API returns a created user payload, try to set user (backward-compatible)
      if (response.data && response.data.id) {
        const newUser: User = {
          id: response.data.id,
          email: response.data.email,
          firstName: response.data.firstName,
          lastName: response.data.lastName || '',
        };
        setUser(newUser);
        localStorage.setItem('user', JSON.stringify(newUser));
      }

      // Return the full API response data so callers can react to status/message
      return response.data;
    } catch (error: any) {
      console.error('Signup failed:', error);
      // Handle specific error messages from the API
      if (error.response?.status === 409 && error.response?.data?.detail === 'Email already exists') {
        throw new Error('Email already exists');
      }
      throw new Error(error.response?.data?.detail || error.response?.data?.message || 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    clearTokensFromStorage();
    localStorage.removeItem('user');
  };

  // Check for existing user and tokens on mount
  React.useEffect(() => {
    const savedUser = localStorage.getItem('user');
    const storedTokens = getStoredTokens();
    
    if (savedUser && storedTokens) {
      try {
        setUser(JSON.parse(savedUser));
        setTokens(storedTokens);
      } catch (error) {
        console.error('Failed to parse saved user:', error);
        localStorage.removeItem('user');
        clearTokensFromStorage();
      }
    }
  }, []);

  const value: AuthContextType = {
    user,
    tokens,
    isAuthenticated: !!user && !!tokens,
    login,
    signup,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
