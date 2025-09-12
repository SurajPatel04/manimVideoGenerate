import { useAuth } from '@/contexts/AuthContext';
import api from '@/lib/api';

export const useApi = () => {
  const { tokens, logout } = useAuth();

  // Function to make authenticated API calls
  const authenticatedRequest = async (config: any) => {
    if (!tokens?.accessToken) {
      logout();
      throw new Error('No access token available');
    }

    try {
      return await api(config);
    } catch (error: any) {
      if (error.response?.status === 401) {
        logout();
      }
      throw error;
    }
  };

  return {
    api: authenticatedRequest,
    isAuthenticated: !!tokens?.accessToken,
  };
};
