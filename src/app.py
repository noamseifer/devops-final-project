from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main_page():
    result = None
    if request.method == "POST":
        try:
            a = float(request.form["firstNumber"])
            b = float(request.form["secondNumber"])
            result = a + b
        except ValueError:
            result = "Invalid input"            
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5051)