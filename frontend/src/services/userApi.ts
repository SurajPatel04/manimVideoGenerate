import axios from 'axios';
import type { UserHistoryResponse } from '@/types/api';

export class UserApiService {
  private static getAuthHeaders(accessToken: string) {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
    };
  }

  static async getUserHistory(
    accessToken: string,
    page: number = 1,
    limit: number = 15
  ): Promise<UserHistoryResponse> {
    try {
      const response = await axios.get<UserHistoryResponse>(
        '/api/user/userHistory',
        {
          params: { page, limit },
          withCredentials: true,
          headers: this.getAuthHeaders(accessToken),
          timeout: 10000,
        }
      );
      
      return response.data;
    } catch (error: any) {
      console.error('User history API error:', error);
      
      if (error.response) {
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