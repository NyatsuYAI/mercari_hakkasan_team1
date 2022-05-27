import React from 'react';
import './Header.css'
import mercarilogo from '../../../image/mercarilogo.png'

export const Header = () =>{
    return (
        <div className="navigation-top">
            <div className="start-section">
                <img className="mercari-logo" src={mercarilogo}></img>
            </div>
            <div className="center-section">
                <input type="search" placeholder='なにをお探しですか？'></input>
            </div>
            <div className="end-section">
                <div className="desktop-container">
                    <a className="desktop-container-list">お知らせ</a>
                    <a className="desktop-container-list">やることリスト</a>
                    <a className="desktop-container-list">ログアウト</a>
                    <a className="desktop-container-list">出品</a>
                </div>
            </div>
        </div>
    )
};