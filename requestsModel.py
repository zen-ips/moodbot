from flask import Flask, request, jsonify, render_template_string
import requests as req
import re

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>💬 Mood Quote Generator</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #e6f2ff;
      padding: 2rem;
    }
    select, button {
      font-size: 1rem;
      padding: 0.5rem;
      margin-top: 1rem;
    }
    ul {
      background: #fff;
      padding: 1rem;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      list-style: disc inside;
      margin-top: 1rem;
    }
    li {
      margin: 0.5rem 0;
    }
  </style>
</head>
<body>
  <h2>🌤️ Mood-Based Quote Generator</h2>
  <label for="mood">Choose your mood:</label>
  <select id="mood">
    <option value="happy">Happy 😊</option>
    <option value="anxious">Anxious 😰</option>
    <option value="tired">Tired 😴</option>
    <option value="motivated">Motivated 💪</option>
    <option value="sad">Sad 😢</option>
    <option value="angry">Angry 😡</option>
    <option value="stressed">Stressed 😩</option>
    <option value="excited">Excited 🤩</option>
  </select>
  <br>
  <button onclick="generateQuotes()">Get Quotes</button>
  <ul id="quotesList"></ul>

  <script>
    async function generateQuotes() {
      const mood = document.getElementById("mood").value;
      const response = await fetch("/generate_quote", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mood })
      });

      const data = await response.json();
      const output = document.getElementById("quotesList");
      output.innerHTML = "";

      if (data.quotes) {
        try {
          const quotes = JSON.parse(data.quotes);
          quotes.forEach(q => {
            const li = document.createElement("li");
            li.textContent = q;
            output.appendChild(li);
          });
        } catch (e) {
          const li = document.createElement("li");
          li.textContent = data.quotes;
          output.appendChild(li);
        }
      } else {
        const li = document.createElement("li");
        li.textContent = data.error || "Something went wrong!";
        output.appendChild(li);
      }
    }
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate_quote', methods=['POST'])
def generate_quote():
    user_data = request.json
    mood = user_data.get('mood', '')
    print(f"✅ Mood received: {mood}")

    prompt = f'''I am creating an app that generates a quote to encourage the user based on their mood. The mood is "{mood}". Generate an encouraging and uplifting array of quotes based on this mood. Return only the array of quotes as JSON. No explanation.'''

    data = {
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = req.post("http://127.0.0.1:11434/api/generate", headers={"Content-Type": "application/json"}, json=data)
        if response.ok:
            raw = response.json()["response"].strip()
            print("🧠 Raw response:\n", raw)

            match = re.search(r"\[(.*?)\]", raw, re.DOTALL)
            if match:
                json_quotes = "[" + match.group(1) + "]"
                return jsonify({"quotes": json_quotes})
            else:
                return jsonify({"quotes": raw})
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
