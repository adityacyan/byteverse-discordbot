from flask import Flask
from threading import Thread
import time

app = Flask('')
last_ping_time = None

def update_last_ping_time():
    global last_ping_time
    last_ping_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

@app.route('/')
def home():
    status_message = f"Last ping time: {last_ping_time}" if last_ping_time else "No pings received yet."
    return f'''
    <html>
      <head>
        <title>Webserver Status</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            text-align: center;
            padding: 50px;
          }}
          .container {{
            background-color: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: inline-block;
          }}
          h1 {{
            color: #007acc;
          }}
          p {{
            color: #333;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h1>✅ Webserver OK</h1>
          <h1>✅ Discord Bot OK</h1>
          <p>{status_message}</p>
          <p>Made by <strong>adityacyan</strong></p>
        </div>
      </body>
    </html>
    '''

def run():
    print("🌐 Webserver is running on http://0.0.0.0:8080")
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
