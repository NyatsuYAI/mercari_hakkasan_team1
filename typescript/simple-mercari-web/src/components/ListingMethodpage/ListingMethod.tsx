import React from 'react' 
import './ListingMethod.css'

export const ListingMethod = () => {
    return(
        <div className="listing-container">
            <div className="center-column">
                <h1>出品</h1>
                <div className="flex_wrapper">
                    <a></a>
                    <a></a>
                </div>
                <h2>商品の出品</h2>
                <h2>売れやすい持ち物</h2>
                <form className="loginform" method="POST">
                    <p>ユーザー名</p>
                    <input className="input-username"></input>
                    <p>パスワード</p>
                    <input className="input-password"></input>
                    <br /> <br /><br />
                    <button>ログイン</button>
                </form>
            </div>
        </div>
    )
};