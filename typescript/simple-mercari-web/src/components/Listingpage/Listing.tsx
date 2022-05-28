import React, { useState } from "react";
import "./Listing.css";
import axios from "axios";
import { useAuthUser } from "../Hooks/AuthUserContext";

const server = process.env.API_URL || "http://127.0.0.1:9000";

type formDataType = {
  name: string;
  category: string;
  image: string;
  price?: string;
  info: string;
  status?: string;
};

export const Listing = () => {
  const authUser = useAuthUser();
  const initialState = {
    name: "",
    category: "",
    price: "",
    status: "",
    info: "",
    image: "",
  };
  const [values, setValues] = useState<formDataType>(initialState);
  const onValueChange = (event: React.ChangeEvent<HTMLInputElement>) =>
    setValues({
      ...values,
      [event.target.name]: event.target.value,
    });
  const onSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) =>
    setValues({
      ...values,
      [event.target.name]: event.target.value,
    });
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const data = new FormData();
    // data.append("user_name", authUser?.name);
    data.append("name", values.name);
    data.append("info", values.info);
    data.append("category", values.category);
    data.append("image", values.image);
    axios
      .post(server.concat("/items"), {
        data,
      })
      .then((response) => {
        console.log("POST status:", response.statusText);
      })
      .catch((error) => {
        console.error("POST error:", error);
      });
  };
  return (
    <div className="listing-container">
      <div className="center-column">
        <h1>商品の出品</h1>
        <form onSubmit={handleSubmit}>
          <p>出品画像</p>
          <label>
            画像を選択する
            <input
              onChange={onValueChange}
              type="file"
              name="image"
              id="image"
            />
          </label>
          <br />
          <h2>商品の詳細</h2>
          <p>カテゴリー</p>
          <select
            name="category"
            className="select-category"
            placeholder="選択してください"
            onChange={onSelectChange}
          >
            <option hidden disabled selected>
              選択してください
            </option>
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
          <select
            // name="status"
            className="select-condition"
            onChange={onSelectChange}
          >
            <option hidden disabled selected>
              選択してください
            </option>
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
          <input name="name" onChange={onValueChange}></input>
          <p>商品の説明</p>
          <input name="info" onChange={onValueChange}></input>
          <br />
          <h2>販売価格</h2>
          <p>販売価格</p>
          <input
            onChange={onValueChange}
            name="price"
            placeholder="0"
            type="number"
            min="0"
            inputMode="numeric"
          ></input>
          <br /> <br />
          <br />
          <button className="listing-button">出品する</button>
          <br /> <br />
          <br />
        </form>
      </div>
    </div>
  );
};
