from flask import Flask, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>研究室現在地共有</title>

<style>
body { text-align:center; font-family: Arial; }
button { font-size:20px; margin:10px; padding:15px; }
</style>

</head>

<body>

<h2>今どこにいますか？</h2>

<button onclick="setLocation('実験室')">実験室</button>
<button onclick="setLocation('居室')">居室</button>
<button onclick="setLocation('大学')">大学</button>

<p id="status">未選択</p>

<script>
function setLocation(place){
    document.getElementById("status").innerText = "現在地: " + place;
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html)

if __name__ == "__main__":
    app.run()

