from flask import Flask, request, render_template_string
import os
from google import genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

template = '''
<!doctype html>
<html>
<head>
    <title>Rose Agent Chat (Gemini)</title>
    <style>
        body { font-family: Arial, sans-serif; background:#f6f6fa; margin:0; }
        .chatbox { max-width:600px; margin:40px auto; background:#fff; border-radius:8px;
            box-shadow:0 2px 12px rgba(0,0,0,0.08); padding:30px 30px 10px; }
        h2 { font-weight:500; color:#333; }
        form { margin-bottom:12px; }
        input[name=prompt] { width:75%; padding:10px; border-radius:5px;
            border:1px solid #ccc; font-size:1em;}
        input[type=submit] { padding:10px 18px; background:#7e3fff; color:#fff;
            border:none; font-size:1em; border-radius:5px; margin-left:10px;}
        .msg { margin:15px 0; }
        .user { color:#333; background:#e8e6ff; border-radius:7px; padding:9px; }
        .agent { color:#212; background:#f9e7fa; border-radius:7px; padding:9px; }
    </style>
</head>
<body>
    <div class="chatbox">
        <h2>Rose Agent Chat (Gemini)</h2>
        <form method="post">
            <input name="prompt" placeholder="Ask me anything..." autofocus>
            <input type="submit" value="Send">
        </form>
        {% if user %}
        <div class="msg user"><b>You:</b> {{ user }}</div>
        {% endif %}
        {% if response %}
        <div class="msg agent"><b>Rose Agent:</b> {{ response }}</div>
        {% endif %}
    </div>
</body>
</html>
'''


def run_rose_agent(user_prompt):
    client = genai.Client()
    return client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt
    ).text

@app.route("/", methods=["GET", "POST"])
def chat():
    response = None
    user = None
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        user = prompt
        if prompt.strip():
            try:
                response = run_rose_agent(prompt)
            except Exception as e:
                response = f"Error: {e}"
    return render_template_string(template, response=response, user=user)


if __name__ == "__main__":
    app.run(debug=True)
