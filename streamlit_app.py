import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 画面の設定
st.set_page_config(page_title="アイム機械割信頼区間", layout="centered")

# タイトル（GOGOランプ風）
st.markdown("<h1 style='text-align: center; color: #a855f7; text-shadow: 0 0 10px #ff00ff, 0 0 20px #00ffff;'>GOGO! INTERVAL</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a1a1aa; font-size: 0.8rem;'>アイムジャグラーEX 機械割信頼区間（適当打ち）</p>", unsafe_allow_html=True)

# 入力エリア
st.write("### ⚙️ 設定を入力")
n = st.number_input("💡 累計ゲーム数 (G)", min_value=100, value=8000, step=100)

setting_options = {
    "設定1 (97.0%)": 0.970,
    "設定2 (98.0%)": 0.980,
    "設定3 (98.9%)": 0.989,
    "設定4 (101.1%)": 1.011,
    "設定5 (103.3%)": 1.033,
    "設定6 (105.5%)": 1.055
}
selected_setting = st.selectbox("🎰 推定・狙い設定", list(setting_options.keys()), index=5)
target_payout = setting_options[selected_setting]

if st.button("信頼区間を計算する", use_container_width=True):
    # パチスロの標準偏差（適当打ち時）
    SIGMA = 1.385
    z_score = 1.96 # 95%信頼区間
    
    # 標準エラーの計算
    standard_error = SIGMA / np.sqrt(n)
    
    # 機械割の範囲
    min_rate = target_payout - (z_score * standard_error)
    max_rate = target_payout + (z_score * standard_error)
    
    # 差枚数の計算 (枚数 = G数 * 3枚 * (機械割 - 1))
    min_coins = int(np.round(n * 3 * (min_rate - 1)))
    max_coins = int(np.round(n * 3 * (max_rate - 1)))
    expected_coins = int(np.round(n * 3 * (target_payout - 1)))
    
    # 結果表示
    st.write("---")
    st.write("### 📊 95%信頼区間（現実的なブレの範囲）")
    
    st.info(f"**差枚数の範囲：**\n\n ## {min_coins:+}枚 〜 {max_coins:+}枚")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("機械割 下限", f"{min_rate*100:.1f}%")
    with col2:
        st.metric("機械割 上限", f"{max_rate*100:.1f}%")
        
    # グラフ描画（Matplotlib）
    fig, ax = plt.subplots(figsize=(6, 2.5))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    labels = ['Worst', 'Expected', 'Best']
    values = [min_coins, expected_coins, max_coins]
    colors = ['#f87171', '#a855f7', '#4ade80']
    
    bars = ax.barh(labels, values, color=colors, height=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#444')
    ax.spines['left'].set_color('#444')
    ax.tick_params(colors='white')
    ax.xaxis.grid(True, linestyle='--', alpha=0.3, color='#444')
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, f' {width:+}枚', 
                va='center', ha='left' if width >= 0 else 'right', color='white', fontweight='bold')

    st.pyplot(fig)
    
    st.caption(f"⚠️ **解説：** 設定を据え置いていると仮定した場合、{n:,}G回した時の差枚数は、20回中19回（確率95%）で上記の範囲に収まります。もしこれより大幅に下回っている場合、低設定への「下げ」を疑う強い根拠になります。")
