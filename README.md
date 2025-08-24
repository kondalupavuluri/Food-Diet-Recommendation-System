# 🍴 Food Diet Recommendation System  

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)  
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)  
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)  
![License](https://img.shields.io/badge/License-MIT-yellow)  

A **Machine Learning–based web application** that provides **personalized diet recommendations** based on user health details and goals.  
This project helps users generate meal plans tailored to their **age, height, weight, dietary preferences, and fitness goals**.  

---

**Features  **

- 📊 **BMI Calculation** – Computes Body Mass Index & health condition.  
- 🥗 **Personalized Meal Plans** – Suggestions for **weight loss, gain, or maintenance**.  
- 🥬 **Diet Preferences** – Choose between **Veg, Non-Veg, or Mixed** diets.  
- 🍛 **Meal Customization** – Select number of meals per day & customize based on available ingredients.  
- 🍽 **Default Indian Meal Plan** – Pre-designed option for general users.  
- 📖 **Recipes & Instructions** – Each food item includes detailed preparation steps.  
- ⚡ **Interactive Frontend** – Simple and user-friendly **Streamlit UI**.  
- 🔗 **FastAPI Backend** – Manages ML model predictions and APIs.  

---

##  Tech Stack  

- **Programming Language:** Python  
- **Frontend:** [Streamlit](https://streamlit.io/)  
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)  
- **Machine Learning:** Scikit-learn (KNN Algorithm)  
- **Database:** CSV/SQLite (food dataset & nutritional values)  
- **Libraries:** Pandas, Numpy, Matplotlib, Seaborn  

---

## 📂 Project Structure  

```bash
Food-Diet-Recommendation-System/
│
├── FastAPI_Backend/        # Backend with FastAPI + ML model
│   ├── main.py             # API routes
│   ├── model.pkl           # Trained ML model (KNN)
│   └── requirements.txt
│
├── Streamlit_Frontend/     # Streamlit UI
│   ├── app.py              # Main Streamlit app
│   └── pages/              # Additional UI pages
│
├── dataset/                # Food & nutrition dataset
│   └── food_data.csv
│
├── README.md               # Project documentation
└── LICENSE                 # License file
