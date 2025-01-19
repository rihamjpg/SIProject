export interface User {
  id: number;
  email: string;
  username: string;
  is_employee: boolean;
  is_hr: boolean;
  is_manager: boolean;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user_type: "employee" | "hr" | "manager" | "admin";
}
