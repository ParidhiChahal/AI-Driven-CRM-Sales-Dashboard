import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI CRM Dashboard", layout="wide")

st.markdown("## 🚀 AI-Driven CRM Sales Dashboard")
st.markdown("---")

# ---------------- LOAD DATA ----------------
df = pd.read_excel("crm_ml_ready_data.xlsx")

# Safety conversion
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

# ---------------- KPIs ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Leads", len(df))
col2.metric("Total Revenue", f"${int(df['Value'].sum())}")
col3.metric("Avg Deal Size", f"${int(df['Value'].mean())}")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("🔍 Filters")

status_filter = st.sidebar.selectbox("Select Status", df["Status"].unique())
source_filter = st.sidebar.selectbox("Select Source", df["Source"].unique())

filtered_df = df[
    (df["Status"] == status_filter) &
    (df["Source"] == source_filter)
]

# ---------------- TABLE ----------------
st.subheader("📋 Lead Data")
st.dataframe(filtered_df, use_container_width=True)

# ---------------- CHARTS ----------------
col4, col5 = st.columns(2)

with col4:
    fig1 = px.bar(filtered_df, x="Status", y="Value", title="Sales Pipeline")
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    fig2 = px.pie(filtered_df, names="Source", values="Value", title="Lead Sources")
    st.plotly_chart(fig2, use_container_width=True)

fig3 = px.scatter(filtered_df,
                  x="Interactions",
                  y="Value",
                  size="Value",
                  color="Status",
                  title="Engagement vs Deal Value")

st.plotly_chart(fig3, use_container_width=True)

# ---------------- ML MODEL ----------------
df['Lead_Score_Num'] = df['Lead_Score'].map({'Cold':0, 'Warm':1, 'Hot':2})

X = df[['Value', 'Interactions', 'Last_Contact_Days']]
y = df['Lead_Score_Num']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# ---------------- PREDICTION UI ----------------
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

# ---------------- AI EMAIL GENERATOR ----------------
st.markdown("---")
st.subheader("📧 AI Email Generator")

client_name = st.text_input("Client Name")

if st.button("Generate Email"):
    st.write(f"""
    Dear {client_name},

    I hope you are doing well.

    We wanted to follow up regarding your interest in our services. 
    Based on our recent discussion, we believe there is a great opportunity to collaborate.

    Please let us know a convenient time to proceed further.

    Looking forward to your response.

    Best Regards,  
    Sales Team
    """)

# ---------------- DOWNLOAD BUTTON ----------------
st.markdown("---")
st.download_button("⬇️ Download Filtered Data",
                   filtered_df.to_csv(index=False),
                   "filtered_leads.csv")
