from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
from zoneinfo import ZoneInfo
import threading
import time
import requests

def keep_alive():
    while True:
        try:
            requests.get("https://location-app-6.onrender.com")
            print("keep alive")
        except:
            pass
        time.sleep(300)  # 300秒 = 5分

app = Flask(__name__)

location_data = {}

html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>研究室現在地共有</title>

<style>
body { text-align:center; font-family: Arial; }
button { font-size:20px; margin:10px; padding:15px; }
input { font-size:18px; padding:5px; }
</style>

</head>

<body>

<h2>研究室 現在地共有</h2>

<input id="name" placeholder="名前を入力">

<br><br>

<button onclick="setLocation('KEK')">KEK</button>
<button onclick="setLocation('プレハブ')">プレハブ</button>
<button onclick="setLocation('筑波大学')">筑波大学</button>
<button onclick="setLocation('NIMS')">NIMS</button>
<button onclick="setLocation('帰宅')">帰宅</button>
<button onclick="setLocation('出張')">出張</button>
<button onclick="setLocation('その他')">その他</button>

<h3>みんなの現在地</h3>

<div id="list"></div>

<script>

function setLocation(place){

    const name = document.getElementById("name").value;

    fetch("/update",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            name:name,
            location:place
        })
    });

}

function timeAgo(time){

    const now = new Date();
    const past = new Date(time);

    const diff = Math.floor((now - past)/1000);

    const min = Math.floor(diff/60);
    const hour = Math.floor(diff/3600);

    if(diff < 60){
        return "たった今";
    }
    else if(min < 60){
        return min + "分前";
    }
    else if(hour < 24){
        return hour + "時間前";
    }
    else{
        const day = Math.floor(hour/24);
        return day + "日前";
    }
}

function load(){

    fetch("/data")
    .then(r=>r.json())
    .then(data=>{

        let html="";

        for(let n in data){

            html += "<p>"
                 + n
                 + " : "
                 + data[n].location
                 + " ("
                 + timeAgo(data[n].time)
                 + ")</p>";

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

    now = datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()

    location_data[data["name"]] = {
        "location": data["location"],
        "time": now
    }

    return "ok"


@app.route("/data")
def data():
    return jsonify(location_data)


if __name__ == "__main__":

    t = threading.Thread(target=keep_alive)
    t.start()

    app.run()
