# 🚀 AI-Driven CRM Sales Dashboard

An interactive **Customer Relationship Management (CRM) Dashboard** built using **Streamlit, Machine Learning, and Data Visualization**.
This project helps sales teams analyze leads, track performance, and predict lead conversion using AI.

---

## 📌 Features

* 📊 **Interactive Dashboard**

  * Real-time KPIs (Total Leads, Revenue, Avg Deal Size)
  * Dynamic filtering (Status, Source)

* 📈 **Data Visualization**

  * Sales Pipeline (Bar Chart)
  * Lead Source Analysis (Pie Chart)
  * Engagement vs Deal Value (Scatter Plot)

* 🤖 **Machine Learning**

  * Lead Score Prediction (Hot / Warm / Cold)
  * Built using Random Forest Classifier

* 📧 **AI Email Generator**

  * Generates follow-up emails for clients

* ⬇️ **Data Export**

  * Download filtered data as CSV

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Data Handling:** Pandas
* **Visualization:** Plotly
* **Machine Learning:** Scikit-learn
* **Data Source:** Excel (.xlsx)

---

## 📂 Project Structure

```
crm_project/
│
├── app.py                     # Main Streamlit application
├── crm_ml_ready_data.xlsx     # Dataset
├── requirements.txt           # Dependencies
└── README.md                  # Project documentation
```

---

## ⚙️ Installation & Setup

1. Clone the repository:

'''
git clone https://github.com/your-username/crm-dashboard.git
cd crm-dashboard
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the application:

```
streamlit run app.py
```

---

## 📊 Machine Learning Model

* Algorithm: **Random Forest Classifier**

* Input Features:

  * Deal Value
  * Number of Interactions
  * Last Contact Days

* Output:

  * 🔥 Hot Lead
  * ⚡ Warm Lead
  * ❄️ Cold Lead

---

## 🎯 Use Case

This dashboard helps:

* Sales teams track performance
* Identify high-value leads
* Improve decision-making
* Automate follow-up communication

---

## 🧠 Future Enhancements

* 🔗 Integration with real CRM APIs
* 🤖 Advanced AI (Gemini/OpenAI integration)
* ☁️ Cloud deployment
* 📱 Mobile responsiveness

---

##  Author

PARIDHI CHAHAL
B.Tech CSE (AI/ML)

---

##  Acknowledgment

This project demonstrates the integration of **Data Analytics + Machine Learning + AI** in a real-world business scenario.
