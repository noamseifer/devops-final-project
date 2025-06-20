from flask import Flask, request, render_template
import redis
import re
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)


app = Flask(__name__)


# # Prometheus metrics
emails_added_total = Counter(
    'emails_added_total',
    'Total number of emails added'
)


request_latency = Histogram(
    'email_submission_latency_seconds',
    'Latency of email submissions'
)


# Will need to add redis to our multi-container
# redis_client =
# redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
redis_client = redis.Redis(
    host='redis_host',
    port=6379,
    db=0,
    decode_responses=True
)


# Basic email validation:
# - Requires one or more non-whitespace characters before the @
# - Requires one or more non-whitespace characters after the @ and before the .
# - Requires one or more non-whitespace characters after the .
email_validate_pattern = r"^\S+@\S+\.\S+$"


@app.route("/", methods=["GET", "POST"])
def main_page():
    result = None
    if request.method == "POST":
        with request_latency.time():
            email = str(request.form["userEmail"])
            if check_is_email(email):
                if is_email_registered(email):
                    result = "Email already registered"
                else:
                    result = "Valid Email"
                    redis_client.sadd("emails-set", email)
                    emails_added_total.inc()
            else:
                result = "Invalid Email"
    return render_template("index.html", result=result)


@app.route("/emails")
def emails_page():
    emails = redis_client.smembers('emails-set')
    emails = sorted(emails)
    cardinality = redis_client.scard("emails-set")

    return render_template(
        "emails.html",
        emails=emails,
        cardinality=cardinality
    )


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


def check_is_email(i_InputString) -> bool:
    return re.fullmatch(email_validate_pattern, i_InputString) is not None


# returns true if email is already registered
def is_email_registered(i_InputString) -> bool:
    return redis_client.sismember("emails-set", i_InputString)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5051)
