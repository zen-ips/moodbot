Mood-Based Quote Generator
A simple AI-powered web app that generates motivational quotes based on the user's selected mood.
Built using Flask and Ollama's Gemma 3:1b model.

Features:

Select a mood from a dropdown (e.g., happy, tired, anxious)

Generates uplifting quotes using a local language model

Works entirely offline using Ollama

Clean, user-friendly web interface

Single-file Python + HTML app using Flask

How to Run:

Make sure you have Ollama installed and running.
Download from: https://ollama.com/download

Pull the Gemma model (only once):
ollama pull gemma3:1b

Run the Flask app:
python server.py

Open your browser and go to:
http://127.0.0.1:5000

Technologies Used:

Python + Flask

Ollama (Local LLM runner)

Gemma 3:1b (AI model)

HTML + CSS + JavaScript (for the frontend)
