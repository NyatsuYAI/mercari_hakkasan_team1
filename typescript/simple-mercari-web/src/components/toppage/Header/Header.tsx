import React, { useEffect } from "react";
import "./Header.css";
import { useLogout } from "../../Hooks/AuthUserContext";
import mercarilogo from "../../../image/mercarilogo.png";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useAuthUser } from "../../Hooks/AuthUserContext";

export const Header = () => {
  const logout = useLogout();
  const authUser = useAuthUser();
  const navigate = useNavigate();
  useEffect(() => {
    if (!authUser) {
      navigate("/login");
    }
  }, [authUser]);
  return (
    <div className="navigation-top">
      <div className="start-section">
        <img className="mercari-logo" src={mercarilogo}></img>
      </div>
      <div className="center-section">
        <input type="search" placeholder="なにをお探しですか？"></input>
      </div>
      <div className="end-section">
        <div className="desktop-container">
          <a className="desktop-container-list">お知らせ</a>
          <a className="desktop-container-list">やることリスト</a>
          <button onClick={() => logout()} className="desktop-container-list">
            ログアウト
          </button>
          <Link to="Listing" className="desktop-container-list">
            出品
          </Link>
        </div>
      </div>
    </div>
  );
};
