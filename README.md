# ✈️ Flight Data Analytics Dashboard

A web-based dashboard built with **Flask** that collects and analyzes flight data.
The system retrieves flight information, stores it locally, and visualizes key analytics through an interactive dashboard.

---

# 🌐 Live Demo

The system has been deployed on **Render** and can be accessed online.

🔗 **Live Dashboard Link:**

```
https://iot-jan-26.onrender.com
```

Users can access the dashboard directly without installing any software.

---

# 📌 Project Overview

This project demonstrates a simple **IoT-style data pipeline**:

1. Flight data is collected from an external API.
2. The data is stored locally using SQLite.
3. The Flask dashboard performs analysis using Pandas.
4. Results are visualized through charts and tables.

---

# 🧰 Technology Stack

* Python
* Flask
* Pandas
* Requests
* SQLite
* HTML / CSS / JavaScript
* Render (Cloud Deployment)

SQLite is built into Python, so no additional database installation is required.

---

# 🚀 Local Setup (For Developers)

If you want to run the project locally instead of using the deployed version:

## 1️⃣ Install Python

Download from:
https://www.python.org/downloads/

Ensure **"Add Python to PATH"** is selected.

Verify installation:

```
python --version
```

---

## 2️⃣ Install Git

Download from:
https://git-scm.com/downloads

---

## 3️⃣ Clone Repository

```
git clone https://github.com/Tanycy/IoT_Jan_26.git
cd IoT_Jan_26
```

---

## 4️⃣ Install Dependencies

```
pip install flask pandas requests
```

---

## 5️⃣ Run The Server

```
python app.py
```

Open the dashboard:

```
http://127.0.0.1:5000
```

---

# 📂 Project Structure

```
IoT_Jan_26/
│
├── app.py
├── collect_data.py
├── perak_flights.db
├── requirements.txt
│
├── templates/
│   └── dashboard.html
│
└── README.md
```

---
## 📊 Dashboard Features

The dashboard performs descriptive analytics on recorded flight data, including:

* **Flights per Hour Analysis** – Visualizes hourly air traffic patterns to identify peak flight periods.
* **Flights per Day Trend** – Shows daily flight activity to observe short-term traffic trends.
* **Total Flight Statistics** – Displays total recorded flights along with average altitude and velocity.
* **Aircraft Registration Country Distribution** – Shows the distribution of flights based on the aircraft registration country.
* **Flights by Departure Country** – Lists detected flights grouped by their departure country.
* **Altitude Distribution Analysis** – Displays aircraft altitude ranges using histogram visualization.
* **Velocity Distribution Analysis** – Shows aircraft speed distribution to analyze flight behavior.
* **Flight Path Visualization** – Maps recorded aircraft positions over the Perak region using geographic visualization.

---

# ⚠️ Development Rules

Before starting work:

```
git pull
```

After making changes:

```
git add .
git commit -m "Describe your change"
git push
```

---

# 🚫 Important Notes

* Do NOT modify `perak_flights.db`
* Do NOT upload large database files
* Only **Python and Git** are required to run locally

SQLite is already included with Python.
