# 🧊 WOS SVS Tracker

A lightweight tracking and visualization tool for **State vs State (SvS)** progress in *Whiteout Survival*.

This app allows alliances or players to log, monitor, and analyze score progression over time, helping optimize strategy and track performance during SvS events.

---

## 🚀 Features

- 📊 Real-time score tracking  
- 🧑‍🤝‍🧑 Player contribution logging  
- 📈 Automatic visualization of score progression  
- 🔄 Auto-refreshing dashboard  
- ☁️ Google Sheets integration for shared data storage  
- 🎯 Designed for alliance coordination and decision-making  

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend/Data:** Google Sheets (via `gspread`)  
- **Visualization:** Matplotlib / Streamlit charts  
- **Auth:** Google Service Account  

---

## 📦 Installation

### 1. Clone the repository

    git clone https://github.com/bklynchconnect/wos-svs-tracker.git
    cd wos-svs-tracker

### 2. Install dependencies

    pip install -r requirements.txt

*(If you don’t have a requirements file yet, you can generate one using `pip freeze > requirements.txt`.)*

---

## 🔐 Google Sheets Setup

1. Create a Google Sheet for storing data  
2. Create a **Google Service Account**  
3. Download the credentials JSON file  
4. Share your Google Sheet with the service account email  
5. Add credentials to your project (e.g. `credentials.json`)  

---

## ▶️ Running the App

    streamlit run app.py

---

## 📊 Data Structure

Typical sheet columns:

| Timestamp | Player | X | Y | Score / Tags |
|----------|--------|---|---|-------------|

You can customize this depending on your tracking needs.

---

## 🎮 Use Case

This tool is designed for:

- SvS prep tracking  
- Monitoring alliance contribution  
- Identifying performance trends  
- Coordinating strategy during events  

---

## ⚙️ Customization Ideas

- Add alliance vs alliance comparison  
- Heatmaps of player activity  
- Alerts for score thresholds  
- Multi-state tracking  
- Export reports  

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to improve.

---

## ⚠️ Disclaimer

This is a fan-made tool and is not affiliated with *Whiteout Survival*.

---

## 📄 License

MIT License (or update as needed)

---

## 💡 Future Improvements

- Mobile-friendly UI  
- Authentication / user roles  
- Historical SvS analytics  
- API-based data ingestion (instead of manual entry)  
