import React from "react";
import './TabItems.css'

export const TabItems = () => {
    return (
        <div>
            <div className="mer-tab-list">
                <a className="selected">タイムライン</a>
                <a>おすすめ</a>
                <a>マイリスト</a>
                <a>ピックアップ</a>
            </div>
        </div>
    )
};