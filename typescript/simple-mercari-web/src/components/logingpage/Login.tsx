import { memo, VFC, useState, ChangeEvent, useCallback } from "react";
import { useLogin } from "../Hooks/AuthUserContext";
import '../toppage/Header/Header.css'
import './Login.css'
import mercarilogo from '../../image/mercarilogo.png'

// export const useAuth = () => {
//     const navigate = useNavigate();
//     const login = useLogin()
//     // login(userEmail, userPassword)
//     // return { login(userEmail, userPassword) }
// };

export const Login: VFC = memo(() => {
    const [userEmail, setUserEmail] = useState("");
    const [userPassword, setUserPassword] = useState("");
    const login = useLogin()
    
    const navigationTopStyle = {
        padding: '6px',
        borderBottom: '2px solid rgb(228, 228, 228)'
    };
    
    const onChangeUserEmail = (e: ChangeEvent<HTMLInputElement>) => setUserEmail(e.target.value)
    const onChangeUserPassword = (e: ChangeEvent<HTMLInputElement>) => setUserPassword(e.target.value)
    const onClickLoginButton = () => login(userEmail, userPassword)
    
    return(
        <>
            <div className="navigation-top" style={navigationTopStyle}>
                <div className="start-section">
                    <img className="mercari-logo" src={mercarilogo}></img>
                </div>
                <div className="center-section"></div>
                <div className="end-section"></div>
            </div>
            <div className="login-container">
                <div className="center-column">
                    <h1>ログイン</h1>
                    <form className="loginform">
                        <p>メールまたは電話番号</p>
                        <input className="input-userEmail" value={userEmail} onChange={onChangeUserEmail}></input>
                        <p>パスワード</p>
                        <input className="input-password" value={userPassword} onChange={onChangeUserPassword} type="password"></input>
                        <br /> <br /><br />
                        <button className="login-button" onClick={onClickLoginButton}>ログイン</button>
                    </form>
                </div>
            </div>
        </>
    )
});