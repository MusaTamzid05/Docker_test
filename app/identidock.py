from flask import Flask
from flask import Response
import requests



app = Flask(__name__)
default_name = "Musa"


@app.route("/" , methods = ["GET" , "POST"])
def mainpage():

    name = default_name
    header = "<html><head><title>Identidock</title></head><body>"
    body = '''<form method = "POST">
                  Hello <input type = "text" name = "name" value = "{}" >
                  <input type = "submit" value = "submit">
            </form>
            <p>You look like : <img src = "/monster/monster.png"/></p>
    '''.format(name)
    footer = "</body></html>"


    return header + body + footer

@app.route("/monster/<name>")
def get_identicon(name):

    r = requests.get("http://dnmonster:8080/monster/" + name + "?size=80")
    image = r.content

    return Response(image , mimetype = "image/png")


def main():
    app.run(debug = True , host = "0.0.0.0")


if __name__ == "__main__":
    main()


