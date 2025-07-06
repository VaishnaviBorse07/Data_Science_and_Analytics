🦠 COVID-19 Data Analysis Dashboard
This project analyzes the global impact of COVID-19 using real-world data from WHO. It uses interactive visualizations and metrics to help understand the spread, recovery, and mortality trends globally.

📁 Project Structure
4_COVID_19_Data_Analysis/
│
├── screenshots/                  # Visuals of dashboard and results
├── working video/               # Demo video showcasing the dashboard
├── WHO-COVID-19-global-data.csv # Dataset containing COVID-19 global data
└── covid_dashboard.py           # Python script for dashboard and analysis
🔍 Features
Loads real-time WHO COVID-19 global data

Displays total confirmed, recovered, and death cases

Visualizes data via line plots, bar graphs, and maps

User-friendly dashboard built with Streamlit

Supports country-level filtering and analysis

📂 Files Description
WHO-COVID-19-global-data.csv: Contains WHO-provided daily COVID-19 data per country.

covid_dashboard.py: 
 Python Streamlit app that
  Parses and processes the CSV data
  Visualizes metrics (confirmed, deaths, recovered)
  Enables users to explore trends over time

screenshots/: Sample output images

working video/: Demo video of dashboard in action

🛠️ Technologies Used
Python

Pandas

Streamlit

Plotly / Matplotlib

WHO COVID-19 Data

🚀 How to Run
Clone/download the repository.

Install required packages:
pip install pandas streamlit plotly

Run the dashboard:
streamlit run covid_dashboard.py

📷 Screenshots
Go to the screenshots/ folder to view the dashboard visuals.

🎥 Demo
The full demonstration is available in the working video/ folder.
