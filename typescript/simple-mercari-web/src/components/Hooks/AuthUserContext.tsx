import React, { createContext, useContext, useEffect, useState } from "react"
import { Navigate, useNavigate } from "react-router-dom";

type OperationType = {
    login: (userEmail: string, userPassword: string) => void,
    logout: () => void
}

type AuthUser = {
    //   userId: string,
    userEmail: string,
    userPassword: string,
}

const AuthUserContext = createContext<AuthUser | null>(null)
const AuthOperationContext = createContext<OperationType>({
    login: (_) => console.error("Providerが設定されていません"),
    logout: () => console.error("Providerが設定されていません")
})

const AuthUserProvider: React.FC = ({ children }) => {
    const [authUser, setAuthUser] = useState<AuthUser | null>(null)

    const login = async (userEmail: string, userPassword: string) => {
        setAuthUser({ userEmail, userPassword })
        // console.log(userEmail)
        // console.log(authUser)
    }

    const logout = async () => {
        setAuthUser(null)
    }

    return (
        <AuthOperationContext.Provider value={{ login, logout }}>
            <AuthUserContext.Provider value={authUser}>
                {children}
            </AuthUserContext.Provider>
        </AuthOperationContext.Provider>
    )
}

export const useAuthUser = () => useContext(AuthUserContext)
export const useLogin = () => useContext(AuthOperationContext).login
export const useLogout = () => useContext(AuthOperationContext).logout

export default AuthUserProvider