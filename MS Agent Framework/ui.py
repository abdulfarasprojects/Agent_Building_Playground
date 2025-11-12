from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from cooking_agent import chat_with_agent

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_chat():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cooking AI Agent</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            #chat { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: scroll; margin-bottom: 10px; }
            input { width: 300px; padding: 5px; }
            button { padding: 5px 10px; }
        </style>
    </head>
    <body>
        <h1>Cooking AI Agent</h1>
        <p>You can ask me to find recipes or extract ingredients from recipes.</p>
        <div id="chat"></div>
        <input type="text" id="input" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">Send</button>
        <script>
            async function sendMessage() {
                const input = document.getElementById('input');
                const chat = document.getElementById('chat');
                const message = input.value.trim();
                if (!message) return;
                chat.innerHTML += '<p><strong>You:</strong> ' + message + '</p>';
                input.value = '';
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                });
                const data = await response.json();
                chat.innerHTML += '<p><strong>Agent:</strong> ' + data.response + '</p>';
                chat.scrollTop = chat.scrollHeight;
            }
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    response = await chat_with_agent(message)
    return {"response": response}