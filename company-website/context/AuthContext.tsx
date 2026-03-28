"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { authStorage } from "@/services/api";

interface AuthContextType {
  isAuthenticated: boolean;
  loading: boolean;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  loading: true,
  logout: () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = authStorage.getToken();
    setIsAuthenticated(!!token);
    setLoading(false);
  }, []);

  const logout = () => {
    authStorage.clear();
    setIsAuthenticated(false);
    router.push("/login");
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, loading, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
