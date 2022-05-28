import { memo, VFC, useState, ChangeEvent, useCallback } from "react";
import { useLogin, useAuthUser } from "../Hooks/AuthUserContext";
import "../toppage/Header/Header.css";
import "./Login.css";
import mercarilogo from "../../image/mercarilogo.png";
import axios from "axios";

const server = process.env.API_URL || "http://127.0.0.1:9000";

type newUser = {
  user_name: string;
  email: string;
  password: string;
};

export const Login: VFC = memo(() => {
  const authUser = useAuthUser();
  const [newUser, setNewUser] = useState<newUser>({
    email: "",
    password: "",
    user_name: "",
  });
  const login = useLogin();
  const navigationTopStyle = {
    padding: "6px",
    borderBottom: "2px solid rgb(228, 228, 228)",
  };
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setNewUser({ ...newUser, [e.target.name]: e.target.value });
  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const data = new FormData();
    data.append("user_name", newUser.user_name);
    axios
      .post(server.concat("/user"), data)
      .then((response) => {
        console.log("POST status:", response.statusText);
        login(newUser);
      })
      .catch((error) => {
        console.error("POST error:", error);
      });
  };
  return (
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
          <form className="loginform" onSubmit={onSubmit}>
            <p>ユーザー名</p>
            <input
              type="text"
              name="user_name"
              className="input-userName"
              value={newUser.user_name}
              onChange={handleChange}
            ></input>
            <p>メールまたは電話番号</p>
            <input
              type="email"
              name="email"
              className="input-userEmail"
              value={newUser.email}
              onChange={handleChange}
            ></input>
            <p>パスワード</p>
            <input
              name="password"
              className="input-password"
              value={newUser.password}
              onChange={handleChange}
              type="password"
            ></input>
            <br /> <br />
            <br />
            <button className="login-button">ログイン</button>
          </form>
        </div>
      </div>
    </>
  );
});
