// API Response Types
export interface LoginResponse {
  accessToken: string;
  refreshToken: string;
  email: string;
  firstName: string;
  lastName?: string;
  userId: string;
  tokenType: string;
}

export interface SignupResponse {
  id: string;
  email: string;
  firstName: string;
  lastName?: string;
}

export interface RefreshTokenResponse {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
}

// Manim Generation API Types
export interface ManimGenerationRequest {
  userQuery: string;
  format: string;
  quality: string;
  historyId: string;
}

export interface ManimGenerationResponse {
  task_id: string;
  historyId?: string; // Add optional historyId that might be returned
}

// Task Result API Types
export interface TaskResultResponse {
  status: "in_progress" | "completed" | "failed";
  state: "PROGRESS" | "SUCCESS" | "FAILURE";
  current_stage?: string;
  progress?: number;
  details?: string;
  timestamp?: string;
  data?: {
    success: boolean;
    link?: string;
    historyId?: string;
    reason?: string; // For failed cases
    message?: string; // For failed cases
    stage?: string; // For failed cases
    data?: {
      description: string;
      isCodeGood: boolean;
      filename: string;
      format: string;
      validationError: string | null;
      validationErrorHistory: string[];
      executionErrorHistory: string[];
      executionError: string;
      rewriteAttempts: number;
      executionSuccess: boolean;
      quality: string;
      createAgain: number;
      code: string;
    };
    chat_name?: string;
    description?: string;
    quality?: string;
    code?: string;
    filename?: string; // Direct access to filename
  };
}

// Cancel Task API Types
export interface CancelTaskResponse {
  status: "revoked";
  taskId: string;
}

// API Request Types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  firstName: string;
  lastName?: string;
  email: string;
  password: string;
}

export interface RefreshTokenRequest {
  refreshToken: string;
}
