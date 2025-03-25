from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return '''
    <html>
      <head>
        <title>Webserver Status</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            text-align: center;
            padding: 50px;
          }
          .container {
            background-color: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: inline-block;
          }
          h1 {
            color: #007acc;
          }
          p {
            color: #333;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>✅ Webserver OK</h1>
          <h1>✅ Discord Bot OK</h1>
          <p>Made by <strong>adityacyan</strong></p>
        </div>
      </body>
    </html>
    '''

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
