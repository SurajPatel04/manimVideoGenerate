import axios from 'axios';
import type { ManimGenerationRequest, ManimGenerationResponse, TaskResultResponse } from '@/types/api';

export class ManimApiService {
  private static getAuthHeaders(accessToken: string) {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
    };
  }

  static async generateAnimation(
    request: ManimGenerationRequest, 
    accessToken: string
  ): Promise<ManimGenerationResponse> {
    try {
      const response = await axios.post<ManimGenerationResponse>(
        '/api/manimGeneration/',
        request,
        {
          withCredentials: true,
          headers: this.getAuthHeaders(accessToken),
          timeout: 30000, // 30 seconds
        }
      );
      
      // Log the full response for debugging
      console.log('API Response:', response.data);
      
      return response.data;
    } catch (error: any) {
      console.error('Manim generation API error:', error);
      
      if (error.response) {
        // Server responded with error status
        throw new Error(
          error.response.data?.detail || 
          error.response.data?.message || 
          `HTTP ${error.response.status}: ${error.response.statusText}`
        );
      } else if (error.request) {
        // Request was made but no response received
        throw new Error('Network error: Unable to reach the server');
      } else {
        // Something else happened
        throw new Error(`Request error: ${error.message}`);
      }
    }
  }

  static async pollTaskStatus(taskId: string, accessToken: string): Promise<TaskResultResponse> {
    try {
      const response = await axios.get<TaskResultResponse>(`/api/manimGeneration/result/${taskId}`, {
        withCredentials: true,
        headers: this.getAuthHeaders(accessToken),
        timeout: 10000,
      });
      
      return response.data;
    } catch (error: any) {
      console.error('Task status polling error:', error);
      throw error;
    }
  }
}
