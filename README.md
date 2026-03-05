# ✈️ Flight Data Analytics Dashboard

A web-based dashboard built with **Flask** that collects and analyzes flight data.

The system retrieves flight information, stores it locally, and visualizes key analytics such as flight distribution and statistics through an interactive dashboard.

---

# 📌 Project Overview

This project demonstrates a simple **IoT-style data pipeline**:

1. Flight data is collected from an external API.
   
2. The data is stored locally using **SQLite**.
   
4. A **Flask web dashboard** performs analysis using **Pandas**.
   
5. Results are visualized through charts and tables.

The goal is to provide a clear view of flight activity and perform basic analytics on the collected data.

---

# 🧰 Technology Stack

* **Python** – Main programming language
  
* **Flask** – Web framework for dashboard
  
* **Pandas** – Data analysis and processing
  
* **Requests** – API communication
  
* **SQLite** – Local database (built into Python)
  
* **HTML / CSS / JavaScript** – Dashboard interface

⚠️ **Note:** SQLite is included with Python, so no separate installation is required.

---

# 📂 Project Structure

```
IoT_Jan_26/
│
├── app.py                # Flask dashboard server
├── collect_data.py       # Script for collecting flight data
├── requirements.txt      # Python dependencies
├── perak_flights.db      # Local SQLite database
│
├── templates/
│   └── dashboard.html    # Dashboard user interface
│
└── README.md             # Project documentation
```

---

# 🚀 Setup and Installation

Follow these steps to run the project locally.

---

## 1️⃣ Install Python

Download Python from:

https://www.python.org/downloads/

During installation:

✔ Select **“Add Python to PATH”**

Verify installation:

```
> python --version
```

## 2️⃣ Install Git (if not installed)

Download Git:

https://git-scm.com/downloads

Verify installation:

```
> git --version
```

---

## 3️⃣ Clone the Repository

Open **Command Prompt / PowerShell** and run:

```
> git clone https://github.com/Tanycy/IoT_Jan_26.git
cd IoT_Jan_26
```

---

## 4️⃣ Install Required Python Packages

Inside the project folder, run:

```
> pip install flask pandas requests
```

These libraries are required for:

| Library  | Purpose              |
| -------- | -------------------- |
| Flask    | Web dashboard server |
| Pandas   | Data analysis        |
| Requests | API communication    |

---

## 5️⃣ Run the Dashboard Server

Start the Flask server:

```
> python app.py
```

If successful, you should see:

```
Running on http://127.0.0.1:5000
```

---

## 6️⃣ Open the Dashboard

Open your browser and go to:

```
http://127.0.0.1:5000
```

The flight analytics dashboard should now load.

---

# 🎨 Development Guide

Different parts of the project are handled in different files.

---

## Dashboard UI Design

File to edit:

```
templates/dashboard.html
```

You can modify:

* Dashboard layout
* CSS styling
* Chart colors
* Chart types
* Table design

No Python modification is required for UI changes.

---

## Backend Logic

File to edit:

```
app.py
```

Responsibilities:

* API routes
* Database queries
* Data analysis using Pandas
* Sending results to the dashboard

---

## Data Collection

File to edit:

```
collect_data.py
```

Responsibilities:

* Fetch flight data from external API
* Process returned data
* Store records in SQLite database

---

# 📊 Dashboard Analytics

The dashboard performs several types of analysis:

* Total number of detected flights
* Flight distribution by country
* Speed statistics
* Altitude statistics
* Flight activity summaries

All analysis is performed using **Pandas** before being visualized on the dashboard.

---

# ⚠️ Contribution Rules

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

* Do **NOT modify** `perak_flights.db`
* Do **NOT upload large database files**
* The project only requires **Python and Git** to run locally.

SQLite is already included with Python.

---

# 👨‍💻 Author

Developed as part of an **IoT/Data Analytics project** for educational purposes.

---
