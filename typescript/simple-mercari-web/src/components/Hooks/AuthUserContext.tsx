import React, { createContext, useContext, useEffect, useState } from "react";

type OperationType = {
  login: ({ user_name, email, password }: newUser) => void;
  logout: () => void;
};

type AuthUser = {
  id?: number;
  user_name: string;
  email: string;
  password: string;
};

type newUser = {
  user_name: string;
  email: string;
  password: string;
};

const AuthUserContext = createContext<AuthUser | null>(null);
const AuthOperationContext = createContext<OperationType>({
  login: (_) => console.error("Providerが設定されていません"),
  logout: () => console.error("Providerが設定されていません"),
});

const AuthUserProvider: React.FC = ({ children }) => {
  const [authUser, setAuthUser] = useState<AuthUser | null>(null);

  const login = async ({ user_name, email, password }: newUser) => {
    setAuthUser({ user_name, email, password });
  };
  const logout = async () => {
    setAuthUser(null);
  };
  return (
    <AuthOperationContext.Provider value={{ login, logout }}>
      <AuthUserContext.Provider value={authUser}>
        {children}
      </AuthUserContext.Provider>
    </AuthOperationContext.Provider>
  );
};

export const useAuthUser = () => useContext(AuthUserContext);
export const useLogin = () => useContext(AuthOperationContext).login;
export const useLogout = () => useContext(AuthOperationContext).logout;

export default AuthUserProvider;
