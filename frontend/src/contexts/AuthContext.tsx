import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { authAPI } from '../services/api';
import toast from 'react-hot-toast';

// Types
interface User {
  username: string;
  email: string;
  profile?: {
    full_name?: string;
    avatar?: string;
    preferences?: {
      default_quality?: string;
      download_location?: string;
      auto_subtitle?: boolean;
    };
  };
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
}

interface AuthContextType extends AuthState {
  login: (username: string, password: string) => Promise<boolean>;
  register: (userData: RegisterData) => Promise<boolean>;
  logout: () => void;
  updateProfile: (profileData: any) => Promise<boolean>;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

// Action types
type AuthAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'LOGIN_SUCCESS'; payload: { user: User; token: string } }
  | { type: 'LOGIN_FAILURE' }
  | { type: 'LOGOUT' }
  | { type: 'UPDATE_USER'; payload: User };

// Initial state
const initialState: AuthState = {
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: false,
  loading: true,
};

// Reducer
const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        loading: false,
      };
    case 'LOGIN_FAILURE':
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        loading: false,
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        loading: false,
      };
    case 'UPDATE_USER':
      return {
        ...state,
        user: action.payload,
      };
    default:
      return state;
  }
};

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider component
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await authAPI.getProfile();
          if (response.data.success) {
            dispatch({
              type: 'LOGIN_SUCCESS',
              payload: {
                user: response.data.user,
                token,
              },
            });
          } else {
            localStorage.removeItem('token');
            dispatch({ type: 'LOGIN_FAILURE' });
          }
        } catch (error) {
          localStorage.removeItem('token');
          dispatch({ type: 'LOGIN_FAILURE' });
        }
      } else {
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    };

    checkAuth();
  }, []);

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      
      const response = await authAPI.login({ username, password });
      
      if (response.data.success) {
        const { user, access_token } = response.data;
        
        localStorage.setItem('token', access_token);
        
        dispatch({
          type: 'LOGIN_SUCCESS',
          payload: {
            user,
            token: access_token,
          },
        });
        
        toast.success(`Welcome back, ${user.username}!`);
        return true;
      } else {
        toast.error(response.data.error || 'Login failed');
        dispatch({ type: 'LOGIN_FAILURE' });
        return false;
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Login failed';
      toast.error(errorMessage);
      dispatch({ type: 'LOGIN_FAILURE' });
      return false;
    }
  };

  const register = async (userData: RegisterData): Promise<boolean> => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      
      const response = await authAPI.register(userData);
      
      if (response.data.success) {
        const { user, access_token } = response.data;
        
        localStorage.setItem('token', access_token);
        
        dispatch({
          type: 'LOGIN_SUCCESS',
          payload: {
            user,
            token: access_token,
          },
        });
        
        toast.success(`Welcome to EagleEye, ${user.username}!`);
        return true;
      } else {
        toast.error(response.data.error || 'Registration failed');
        dispatch({ type: 'LOGIN_FAILURE' });
        return false;
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Registration failed';
      toast.error(errorMessage);
      dispatch({ type: 'LOGIN_FAILURE' });
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    dispatch({ type: 'LOGOUT' });
    toast.success('Logged out successfully');
  };

  const updateProfile = async (profileData: any): Promise<boolean> => {
    try {
      const response = await authAPI.updateProfile(profileData);
      
      if (response.data.success && state.user) {
        const updatedUser = {
          ...state.user,
          profile: response.data.profile,
        };
        
        dispatch({ type: 'UPDATE_USER', payload: updatedUser });
        toast.success('Profile updated successfully');
        return true;
      } else {
        toast.error(response.data.error || 'Profile update failed');
        return false;
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Profile update failed';
      toast.error(errorMessage);
      return false;
    }
  };

  const value: AuthContextType = {
    ...state,
    login,
    register,
    logout,
    updateProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Hook to use auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
