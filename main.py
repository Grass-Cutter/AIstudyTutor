from flask import Flask, render_template, request
import google.generativeai as ai
import os

#API_Key from Secrets
API_KEY = os.getenv("GOOGLE_API_KEY")

#Configuration of API_Key
ai.configure(api_key = API_KEY)

#Chatbot Model created + chat session started
model = ai.GenerativeModel(model_name="gemini-1.5-flash")
chat = model.start_chat()

#Flask setup
app = Flask(__name__)

#Store History
chat_history = []

@app.route("/", methods = ["GET", "POST"])
def index():
  global chat_history

  subject = "general"
  if request.method == "POST":
    user_input = request.form.get("user_input", "")
    subject = request.form.get("subject", "general")

    #Prompt based on subject
    if subject == "math":
      prompt = f"You are a math study tutor. Assist the user with this: {user_input}"
    elif subject == "history":
      prompt = f"You are a history study tutor. Assist the user with this: {user_input}"
    elif subject == "science":
      prompt = f"You are a science study tutor. Assist the user with this: {user_input}"
    elif subject == "coding":
      prompt = f"You are a coding tutor. Assist the user with this: {user_input}"
    elif subject == "english":
      prompt = f"You are an english study tutor. Assist the user with this: {user_input}"
    else:
      prompt = f"You are a general study tutor. Assist the user    with this: {user_input}"

    #User message added to chat history
    chat_history.append(("You", user_input))
    #Bot response
    response = chat.send_message(prompt)
    bot_reply = response.text

    #Add bot response to chat history
    chat_history.append(("Study AI", bot_reply))
  
  return render_template("index.html", history = chat_history, selected_subject = subject)

app.run(host = "0.0.0.0", port = 81)
