from flask import Flask
from flask import Response
from flask import request

import requests
import hashlib
import redis




app = Flask(__name__)

cache = redis.StrictRedis(host = "redis" , port = 6379 , db = 0)

default_name = "Musa"
salt = "UNIQUE_SALT"


def get_name():


    if request.method == "POST":
        name = request.form["name"]
    else:
        name = default_name

    return name




@app.route("/" , methods = ["GET" , "POST"])
def mainpage():

    name = get_name()

    salted_name = salt + name
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

    header = "<html><head><title>Identidock</title></head><body>"
    body = '''<form method = "POST">
                  Hello <input type = "text" name = "name" value = "{0}" >
                  <input type = "submit" value = "submit">
            </form>
            <p>You look like : <img src = "/monster/{1}"/></p>
    '''.format(name , name_hash)
    footer = "</body></html>"


    return header + body + footer

@app.route("/monster/<name>")
def get_identicon(name):


    # requests a web app written in node to return image.

    image = cache.get(name)

    # if the name is new , that generate a new image for the name,
    # else use the fucking cache for to get the old image for the
    # name.


    if image is None:


        print("Cache miss " , flush = True)
        r = requests.get("http://dnmonster:8080/monster/" + name + "?size=80")
        image = r.content
        cache.set(name , image)


    return Response(image , mimetype = "image/png")


def main():
    app.run(debug = True , host = "0.0.0.0")


if __name__ == "__main__":
    main()


