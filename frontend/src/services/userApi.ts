import axios from 'axios';
import type { UserHistoryResponse } from '@/types/api';

export class UserApiService {
  private static getAuthHeaders(accessToken?: string) {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // If an explicit bearer token is provided and it's not the cookie placeholder,
    // include the Authorization header. For cookie-based auth (where the frontend
    // uses a placeholder like 'cookie') we must NOT send an invalid Authorization
    // header because it will cause the backend to try verifying the header token
    // and fail before falling back to cookie-based auth.
    if (accessToken && accessToken !== 'cookie') {
      headers['Authorization'] = `Bearer ${accessToken}`;
    }

    return headers;
  }

  static async getUserHistory(
    accessToken?: string,
    page: number = 1,
    limit: number = 15
  ): Promise<UserHistoryResponse> {
    try {
      const response = await axios.get<UserHistoryResponse>('/api/user/userHistory', {
        params: { page, limit },
        withCredentials: true,
        headers: this.getAuthHeaders(accessToken),
        timeout: 10000,
      });
      
      return response.data;
    } catch (error: any) {
      console.error('User history API error:', error);
      
      if (error.response) {
        if (error.response.status === 204) {
          return {
            page: 1,
            limit: limit,
            total: 0,
            pages: 0,
            data: []
          };
        }
        
        throw new Error(
          error.response.data?.detail || 
          error.response.data?.message || 
          `HTTP ${error.response.status}: ${error.response.statusText}`
        );
      } else if (error.request) {
        throw new Error('Network error: Unable to reach the server');
      } else {
        throw new Error(`Request error: ${error.message}`);
      }
    }
  }
}