
from flask import Flask, render_template, request
from openai import OpenAI

client = OpenAI(
    api_key="placeholder",
)

app = Flask(__name__)


@app.route("/answer", methods=["GET", "POST"])

    
def generate_advice(user_data):

    prompt = f"""
    You are an AI health coach. Provide a detailed diet and workout plan based on the following details:
    - Height: {user_data['height']} cm
    - Weight: {user_data['weight']} kg
    - Age: {user_data['age']} years
    - Gender: {user_data['gender']}
    - BMI: {user_data['bmi']}
    - Average hours exercised per week: {user_data['exercise_hours']}
    - Resting heart rate: {user_data['resting_heart_rate']} bpm

    Provide concise yet actionable advice. The diet and exercise advice should be structured in separate paragraphs.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    advice = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            advice += chunk.choices[0].delta.content
    
    return advice  # Return the full response
        

@app.route("/", methods=["GET", "POST"])

def index():
    if request.method == "POST":
        # Collect form data
        bmi = float(request.form["weight"]) / (float(request.form["height"])/ 100)**2
        
        user_data = {
            "height": request.form["height"],
            "weight": request.form["weight"],
            "age": request.form["age"],
            "gender": request.form["gender"],
            "bmi": bmi,
            "exercise_hours": request.form["exercise_hours"],
            "resting_heart_rate": request.form["resting_heart_rate"]
        }
        # Generate advice
        advice = generate_advice(user_data)
        return render_template("index.html", advice=advice, user_data=user_data)

    return render_template("index.html", advice=None)

if __name__ == "__main__":
    app.run(debug=True)

