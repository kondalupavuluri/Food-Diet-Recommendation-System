import streamlit as st
import pandas as pd
from Generate_Recommendations import Generator
from random import uniform as rnd
from ImageFinder.ImageFinder import get_images_links as find_image
from streamlit_echarts import st_echarts

st.set_page_config(page_title="Automatic Diet Recommendation", page_icon="💪", layout="wide")

nutritions_values = [
    'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent',
    'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent'
]

# Streamlit states initialization
if "person" not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations = []
    st.session_state.person = None
    st.session_state.weight_loss_option = None


class Person:
    def __init__(self, age, height, weight, gender, activity, meals_calories_perc, weight_loss):
        self.age = age
        self.height = height
        self.weight = weight
        self.gender = gender
        self.activity = activity
        self.meals_calories_perc = meals_calories_perc
        self.weight_loss = weight_loss

    def calculate_bmi(self):
        return round(self.weight / ((self.height / 100) ** 2), 2)

    def display_result(self):
        bmi = self.calculate_bmi()
        bmi_string = f"{bmi} kg/m²"
        if bmi < 18.5:
            category, color = "Underweight", "Red"
        elif 18.5 <= bmi < 25:
            category, color = "Normal", "Green"
        elif 25 <= bmi < 30:
            category, color = "Overweight", "Yellow"
        else:
            category, color = "Obesity", "Red"
        return bmi_string, category, color

    def calculate_bmr(self):
        if self.gender == "Male":
            return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        return 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

    def calories_calculator(self):
        activites = [
            "Little/no exercise", "Light exercise",
            "Moderate exercise (3-5 days/wk)", "Very active (6-7 days/wk)",
            "Extra active (very active & physical job)"
        ]
        weights = [1.2, 1.375, 1.55, 1.725, 1.9]
        weight_factor = weights[activites.index(self.activity)]
        return self.calculate_bmr() * weight_factor

    def generate_recommendations(self):
        try:
            total_calories = self.weight_loss * self.calories_calculator()
            recommendations = []

            for meal in self.meals_calories_perc:
                meal_calories = self.meals_calories_perc[meal] * total_calories

                if meal == "breakfast":
                    recommended_nutrition = [
                        meal_calories, rnd(10, 30), rnd(0, 4), rnd(0, 30),
                        rnd(0, 400), rnd(40, 75), rnd(4, 10), rnd(0, 10), rnd(30, 100)
                    ]
                elif meal == "lunch":  # fixed spelling: 'launch' → 'lunch'
                    recommended_nutrition = [
                        meal_calories, rnd(20, 40), rnd(0, 4), rnd(0, 30),
                        rnd(0, 400), rnd(40, 75), rnd(4, 20), rnd(0, 10), rnd(50, 175)
                    ]
                elif meal == "dinner":
                    recommended_nutrition = [
                        meal_calories, rnd(20, 40), rnd(0, 4), rnd(0, 30),
                        rnd(0, 400), rnd(40, 75), rnd(4, 20), rnd(0, 10), rnd(50, 175)
                    ]
                else:
                    recommended_nutrition = [
                        meal_calories, rnd(10, 30), rnd(0, 4), rnd(0, 30),
                        rnd(0, 400), rnd(40, 75), rnd(4, 10), rnd(0, 10), rnd(30, 100)
                    ]

                generator = Generator(recommended_nutrition)
                response = generator.generate()

                if response and response.json().get("output"):
                    recommended_recipes = response.json()["output"]
                    for recipe in recommended_recipes:
                        recipe["image_link"] = find_image(recipe["Name"])
                    recommendations.append(recommended_recipes)

            return recommendations or []

        except Exception as e:
            st.error(f"Error generating recommendations: {e}")
            return []


class Display:
    def __init__(self):
        self.plans = [
            "Extreme weight gain", "weight gain", "Mild weight gain",
            "Maintain weight", "Mild weight loss", "Weight loss", "Extreme weight loss"
        ]
        self.weights = [1.3, 1.2, 1.1, 1, 0.9, 0.8, 0.6]
        self.losses = ["+1 kg/week", "+0.5 kg/week", "+0.25 kg/week",
                       "-0 kg/week", "-0.25 kg/week", "-0.5 kg/week", "-1 kg/week"]

    def display_bmi(self, person):
        st.header("BMI CALCULATOR")
        bmi_string, category, color = person.display_result()
        st.metric(label="Body Mass Index (BMI)", value=bmi_string)
        st.markdown(f"<p style='color:{color}; font-size: 25px;'>{category}</p>", unsafe_allow_html=True)
        st.markdown("Healthy BMI range: 18.5 kg/m² - 25 kg/m².")

    def display_calories(self, person):
        st.header("CALORIES CALCULATOR")
        maintain_calories = person.calories_calculator()
        st.write("Guideline for daily calorie intake:")
        for plan, weight, loss, col in zip(self.plans, self.weights, self.losses, st.columns(7)):
            with col:
                st.metric(
                    label=plan,
                    value=f"{round(maintain_calories * weight)} Cal/day",
                    delta=loss,
                    delta_color="inverse"
                )

    def display_recommendation(self, person, recommendations):
        if not recommendations:
            st.warning("No recommendations available. Please generate a plan first.")
            return

        st.header("DIET RECOMMENDATOR")
        meals = person.meals_calories_perc
        st.subheader("Recommended recipes:")

        for meal_name, column, recommendation in zip(meals, st.columns(len(meals)), recommendations):
            with column:
                st.markdown(f"##### {meal_name.upper()}")
                for recipe in recommendation:
                    if isinstance(recipe, dict):
                        recipe_name = recipe["Name"]
                        expander = st.expander(recipe_name)
                        recipe_img = f'<div><center><img src={recipe["image_link"]} alt={recipe_name}></center></div>'
                        nutritions_df = pd.DataFrame({value: [recipe[value]] for value in nutritions_values})

                        expander.markdown(recipe_img, unsafe_allow_html=True)
                        expander.markdown("### Nutritional Values (g):")
                        expander.dataframe(nutritions_df)
                        expander.markdown("### Ingredients:")
                        for ingredient in recipe["RecipeIngredientParts"]:
                            expander.markdown(f"- {ingredient}")
                        expander.markdown("### Recipe Instructions:")
                        for instruction in recipe["RecipeInstructions"]:
                            expander.markdown(f"- {instruction}")
                        expander.markdown("### Cooking and Preparation Time:")
                        expander.markdown(
                            f"- Cook Time       : {recipe['CookTime']} min\n"
                            f"- Preparation Time: {recipe['PrepTime']} min\n"
                            f"- Total Time      : {recipe['TotalTime']} min"
                        )

    def display_meal_choices(self, person, recommendations):
        if not recommendations:
            return
        st.subheader("Choose your meal composition:")

        # Simplified for 3 meals
        if len(recommendations) >= 3:
            breakfast_column, lunch_column, dinner_column = st.columns(3)
            with breakfast_column:
                breakfast_choice = st.selectbox(
                    "Choose your breakfast:", [recipe["Name"] for recipe in recommendations[0]]
                )
            with lunch_column:
                lunch_choice = st.selectbox(
                    "Choose your lunch:", [recipe["Name"] for recipe in recommendations[1]]
                )
            with dinner_column:
                dinner_choice = st.selectbox(
                    "Choose your dinner:", [recipe["Name"] for recipe in recommendations[2]]
                )
            choices = [breakfast_choice, lunch_choice, dinner_choice]

            # Calculate nutrition totals
            total_nutrition_values = {nv: 0 for nv in nutritions_values}
            for choice, meals_ in zip(choices, recommendations):
                for meal in meals_:
                    if meal["Name"] == choice:
                        for nv in nutritions_values:
                            total_nutrition_values[nv] += meal[nv]

            total_calories_chose = total_nutrition_values["Calories"]
            loss_calories_chose = round(person.calories_calculator() * person.weight_loss)

            # Graphs
            total_calories_graph_options = {
                "xAxis": {"type": "category", "data": ["Total Calories you chose", f"{st.session_state.weight_loss_option} Calories"]},
                "yAxis": {"type": "value"},
                "series": [
                    {
                        "data": [
                            {"value": total_calories_chose,
                             "itemStyle": {"color": ["#33FF8D", "#FF3333"][total_calories_chose > loss_calories_chose]}},
                            {"value": loss_calories_chose, "itemStyle": {"color": "#3339FF"}},
                        ],
                        "type": "bar",
                    }
                ],
            }
            st_echarts(options=total_calories_graph_options, height="400px")

            nutritions_graph_options = {
                "tooltip": {"trigger": "item"},
                "legend": {"top": "5%", "left": "center"},
                "series": [
                    {
                        "name": "Nutritional Values",
                        "type": "pie",
                        "radius": ["40%", "70%"],
                        "data": [
                            {"value": round(total_nutrition_values[nv]), "name": nv} for nv in total_nutrition_values
                        ],
                    }
                ],
            }
            st_echarts(options=nutritions_graph_options, height="500px")


# ---- Main page ----
display = Display()
title = "<h1 style='text-align: center;'>Automatic Diet Recommendation</h1>"
st.markdown(title, unsafe_allow_html=True)

with st.form("recommendation_form"):
    st.write("Modify the values and click the Generate button for recommendations")
    age = st.number_input("Age", min_value=2, max_value=120, step=1)
    height = st.number_input("Height(cm)", min_value=50, max_value=300, step=1)
    weight = st.number_input("Weight(kg)", min_value=10, max_value=300, step=1)
    gender = st.radio("Gender", ("Male", "Female"))
    activity = st.select_slider(
        "Activity",
        options=[
            "Little/no exercise", "Light exercise",
            "Moderate exercise (3-5 days/wk)", "Very active (6-7 days/wk)",
            "Extra active (very active & physical job)"
        ]
    )
    option = st.selectbox("Choose your weight loss plan:", display.plans)
    st.session_state.weight_loss_option = option
    weight_loss = display.weights[display.plans.index(option)]
    number_of_meals = st.slider("Meals per day", min_value=3, max_value=5, step=1, value=3)

    if number_of_meals == 3:
        meals_calories_perc = {"breakfast": 0.35, "lunch": 0.40, "dinner": 0.25}
    elif number_of_meals == 4:
        meals_calories_perc = {"breakfast": 0.30, "morning snack": 0.05, "lunch": 0.40, "dinner": 0.25}
    else:
        meals_calories_perc = {
            "breakfast": 0.30, "morning snack": 0.05, "lunch": 0.40,
            "afternoon snack": 0.05, "dinner": 0.20
        }

    generated = st.form_submit_button("Generate")

if generated:
    st.session_state.generated = True
    person = Person(age, height, weight, gender, activity, meals_calories_perc, weight_loss)

    with st.container():
        display.display_bmi(person)
    with st.container():
        display.display_calories(person)

    with st.spinner("Generating recommendations..."):
        recommendations = person.generate_recommendations()
        st.session_state.recommendations = recommendations
        st.session_state.person = person

if st.session_state.generated and st.session_state.recommendations:
    with st.container():
        display.display_recommendation(st.session_state.person, st.session_state.recommendations)
        st.success("Recommendation Generated Successfully !", icon="✅")
    with st.container():
        display.display_meal_choices(st.session_state.person, st.session_state.recommendations)
