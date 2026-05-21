export type RegisterPayload = {
  name?: string;
  email: string;
  password: string;
};

export type LoginPayload = {
  email: string;
  password: string;
};

export type AuthUser = {
  id?: string;
  user_id?: string;
  name?: string;
  email?: string;
  role?: string;
};

export type AuthResponse = {
  access_token: string;
  token_type?: string;
  user?: AuthUser;
};
