import React from 'react' 
import './Listing.css'

export const Listing = () => {
    return(
        <div className="listing-container">
            <div className="center-column">
                <h1>商品の出品</h1>
                <form method="POST">
                    <p>出品画像</p>
                    <label>
                        画像を選択する
                        <input type='file' name='image' id='image' />
                    </label>
                    <br />
                    <h2>商品の詳細</h2>
                    <p>カテゴリー</p>
                    <select className="select-category" placeholder="選択してください">
                        <option hidden disabled selected>選択してください</option>
                        <option>レディース</option>
                        <option>メンズ</option>
                        <option>ベビー・キッズ</option>
                        <option>インテリア・住まい</option>
                        <option>本・音楽・ゲーム</option>
                        <option>おもちゃ・ホビー・グッズ</option>
                        <option>コスメ・香水・美容</option>
                        <option>家電・スマホ・カメラ</option>
                        <option>スポーツ・レジャー</option>
                        <option>ハンドメイド</option>
                        <option>チケット</option>
                        <option>自転車・オートバイ</option>
                        <option>その他</option>
                    </select>
                    <p>商品の状態</p>
                    <select className="select-condition">
                        <option hidden disabled selected>選択してください</option>
                        <option>新品・未使用</option>
                        <option>未使用に近い</option>
                        <option>目立った傷や汚れなし</option>
                        <option>やや傷や汚れあり</option>
                        <option>傷や汚れあり</option>
                        <option>全体的に状態が悪い</option>
                    </select>
                    <br />
                    <h2>商品名と説明</h2>
                    <p>商品名</p>
                    <input></input>
                    <p>商品の説明</p>
                    <input></input>
                    <br />
                    <h2>販売価格</h2>
                    <p>販売価格</p>
                    <input placeholder="0" type="number" min="0" inputMode='numeric'></input>
                    <br /> <br /><br />
                    <button className="listing-button">出品する</button>
                    <br /> <br /><br />
                </form>
            </div>
        </div>
    )
};
