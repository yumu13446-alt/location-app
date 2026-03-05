from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

location_data = {}

html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>研究室現在地共有</title>
</head>

<body style="text-align:center;font-family:Arial">

<h2>研究室現在地共有</h2>

<input id="name" placeholder="名前">

<br><br>

<button onclick="setLocation('実験室')">実験室</button>
<button onclick="setLocation('居室')">居室</button>
<button onclick="setLocation('大学')">大学</button>

<h3>みんなの現在地</h3>

<div id="list"></div>

<script>

function setLocation(place){

    const name = document.getElementById("name").value;

    fetch("/update",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({name:name,location:place})
    });
}

function load(){

    fetch("/data")
    .then(r=>r.json())
    .then(data=>{

        let html="";

        for(let n in data){
            html += "<p>" + n + " : " + data[n].location + " (" + data[n].time + ")</p>";
        }

        document.getElementById("list").innerHTML = html;

    });
}

setInterval(load,2000);

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html)

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    now = datetime.now().strftime("%H:%M:%S")

    location_data[data["name"]] = {
        "location": data["location"],
        "time": now
    }

    return "ok"

@app.route("/data")
def data():
    return jsonify(location_data)

if __name__ == "__main__":
    app.run()
