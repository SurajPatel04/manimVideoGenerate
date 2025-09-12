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
