import streamlit as st
import plotly.express as px
import pandas as pd

st.title("💰 我的記帳 APP")

# 初始化資料
if "records" not in st.session_state:
    st.session_state.records = []

# 輸入區
st.subheader("新增記帳")

category = st.text_input("分類")

amount = st.number_input(
    "金額",
    min_value=0.0,
    step=1.0
)

record_type = st.selectbox(
    "類型",
    ["收入", "支出"]
)

note = st.text_input("備註")

# 新增按鈕
if st.button("新增記帳"):

    st.session_state.records.append({
        "類型": record_type,
        "分類": category,
        "金額": amount,
        "備註": note
    })

    st.success("新增成功")

# 顯示資料
st.subheader("記帳紀錄")

if st.session_state.records:

    df = pd.DataFrame(st.session_state.records)

    st.dataframe(
        df,
        use_container_width=True
    )

    income = df[df["類型"] == "收入"]["金額"].sum()
    expense = df[df["類型"] == "支出"]["金額"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("總收入", f"${income:,.0f}")
    col2.metric("總支出", f"${expense:,.0f}")
    col3.metric("餘額", f"${income-expense:,.0f}")

    expense_df = df[df["類型"] == "支出"]

    category_sum = (
        expense_df
        .groupby("分類")["金額"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        category_sum,
        names="分類",
        values="金額",
        title="支出分類分析"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("目前尚無資料")