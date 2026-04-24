import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI CRM Dashboard", layout="wide")

st.markdown("## 🚀 AI-Driven CRM Sales Dashboard")
st.markdown("---")

# ---------------- LOAD DATA ----------------
df = pd.read_excel("crm_ml_ready_data.xlsx")
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 Filters")

status_filter = st.sidebar.multiselect(
    "Select Status", df["Status"].unique(), default=df["Status"].unique()
)

source_filter = st.sidebar.multiselect(
    "Select Source", df["Source"].unique(), default=df["Source"].unique()
)

search = st.sidebar.text_input("🔎 Search Client Name")

filtered_df = df[
    (df["Status"].isin(status_filter)) &
    (df["Source"].isin(source_filter))
]

if search:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(search, case=False)]

# ---------------- KPIs ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Leads", len(filtered_df))
col2.metric("Total Revenue", f"${int(filtered_df['Value'].sum())}")
col3.metric("Avg Deal Size", f"${int(filtered_df['Value'].mean()) if len(filtered_df)>0 else 0}")

# ---------------- INSIGHTS ----------------
st.subheader("📌 Key Insights")

if len(filtered_df) > 0:
    top_company = filtered_df.groupby("Company")["Value"].sum().idxmax()
    top_source = filtered_df.groupby("Source")["Value"].sum().idxmax()

    st.info(f"🏆 Top Revenue Company: {top_company}")
    st.info(f"📈 Best Lead Source: {top_source}")

# ---------------- TABLE ----------------
st.subheader("📋 Lead Data")
st.dataframe(filtered_df, use_container_width=True)

# ---------------- CHARTS ----------------
col4, col5 = st.columns(2)

with col4:
    fig1 = px.bar(filtered_df, x="Status", y="Value", color="Status", title="Sales Pipeline")
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    fig2 = px.pie(filtered_df, names="Source", values="Value", title="Lead Sources")
    st.plotly_chart(fig2, use_container_width=True)

# Scatter
fig3 = px.scatter(filtered_df,
                  x="Interactions",
                  y="Value",
                  size="Value",
                  color="Status",
                  title="Engagement vs Deal Value")
st.plotly_chart(fig3, use_container_width=True)

# Funnel Chart
funnel = filtered_df.groupby("Status")["Value"].sum().reset_index()
fig_funnel = px.funnel(funnel, x="Value", y="Status", title="Sales Funnel")
st.plotly_chart(fig_funnel, use_container_width=True)

# ---------------- ML MODEL ----------------
df['Lead_Score_Num'] = df['Lead_Score'].map({'Cold':0, 'Warm':1, 'Hot':2})

X = df[['Value', 'Interactions', 'Last_Contact_Days']]
y = df['Lead_Score_Num']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

st.metric("🤖 Model Accuracy", f"{acc*100:.2f}%")

# ---------------- HIGH PRIORITY ----------------
st.subheader("🔥 High Priority Leads")
hot_leads = filtered_df[filtered_df["Lead_Score"] == "Hot"]
st.dataframe(hot_leads)

# ---------------- PREDICTION ----------------
st.markdown("---")
st.subheader("🤖 Lead Score Prediction")

col6, col7, col8 = st.columns(3)

with col6:
    value = st.number_input("Deal Value", 10000, 200000, step=5000)

with col7:
    interactions = st.slider("Interactions", 1, 15, 5)

with col8:
    days = st.slider("Last Contact Days", 1, 10, 3)

if st.button("Predict Lead Score"):
    pred = model.predict([[value, interactions, days]])[0]

    if pred == 2:
        st.success("🔥 Hot Lead")
    elif pred == 1:
        st.warning("⚡ Warm Lead")
    else:
        st.error("❄️ Cold Lead")

# ---------------- AI EMAIL ----------------
st.markdown("---")
st.subheader("📧 AI Email Generator")

client_name = st.text_input("Client Name")

if st.button("Generate Email"):
    st.success(f"✅ Email Generated for {client_name}")
    st.code(f"""
Subject: Follow-up Opportunity

Dear {client_name},

We noticed your interest in our services and would love to take this forward.
Please let us know a convenient time to connect.

Looking forward to your response.

Best Regards,
Sales Team
""")

# ---------------- DOWNLOAD ----------------
st.markdown("---")

st.download_button(
    "⬇️ Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_leads.csv"
)

# ---------------- REFRESH ----------------
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()
