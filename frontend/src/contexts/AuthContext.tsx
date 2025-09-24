import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import axios from 'axios';

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
  login: (email: string, password: string) => Promise<any>;
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

  // Verify cookie-based session (used by backend Google OAuth flow)
  const verifyAuthSession = async () => {
    try {
      const response = await axios.get('/api/user/me', {
        withCredentials: true,
      });

      if (response.data && response.data.userId) {
        const userData: User = {
          id: response.data.userId,
          email: response.data.email,
          firstName: response.data.firstName,
          lastName: response.data.lastName || '',
        };
        setUser(userData);

        setTokens({ accessToken: 'cookie', refreshToken: 'cookie', tokenType: 'bearer' });
        localStorage.setItem('user', JSON.stringify(userData));
      }
    } catch (error) {
      logout();
    }
  };

  const login = async (email: string, password: string): Promise<any> => {
    setLoading(true);
    try {
      // Make API call to login endpoint
      const response = await axios.post('/api/user/login', {
        email,
        password,
      }, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 10000,
      });

      // If backend indicates the account is not verified, return the payload and do not save tokens
      if (response.data && (response.data.isVerified === false || response.data.isVerified === 'False')) {
        return response.data;
      }

      // After backend sets HttpOnly cookies, call /me to fetch user profile
      try {
        const me = await axios.get('/api/user/me', { withCredentials: true });
        if (me.data && me.data.userId) {
          const userData: User = {
            id: me.data.userId,
            email: me.data.email,
            firstName: me.data.firstName,
            lastName: me.data.lastName || '',
          };
          setUser(userData);
          localStorage.setItem('user', JSON.stringify(userData));
          setTokens({ accessToken: 'cookie', refreshToken: 'cookie', tokenType: 'bearer' });
          return me.data;
        }
        return response.data;
      } catch (errMe) {
        // If /me fails, fall back to previous response if it provided tokens
        console.warn('Failed to fetch /me after login', errMe);
        return response.data;
      }
    } catch (error: any) {
      console.error('Login failed:', error);
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
        lastName: userData.lastName || '',
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
      if (error.response?.status === 409 && error.response?.data?.detail === 'Email already exists') {
        throw new Error('Email already exists');
      }
      throw new Error(error.response?.data?.detail || error.response?.data?.message || 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    // Call backend logout to clear HttpOnly cookies, then clear local state
    try {
      axios.post('/api/user/logout', {}, { withCredentials: true }).catch(() => {});
    } catch (e) {}
    setUser(null);
    clearTokensFromStorage();
    localStorage.removeItem('user');
  };

  // Check for existing user and tokens on mount. If none found, verify cookie session
  useEffect(() => {
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
        // Fall through to verify cookie session
        verifyAuthSession();
      }
    } else {
      verifyAuthSession();
    }
  }, []);

  const value: AuthContextType = {
    user,
    tokens,
    isAuthenticated: !!user,
    login,
    signup,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
