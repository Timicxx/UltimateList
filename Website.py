from flask import Flask, redirect, jsonify, render_template, session, escape, request, url_for
import uuid
import ujson
from urllib import parse

from modules.Manager import WebsiteManager
from modules.Helper import *

app = Flask("UltimateList")
app.secret_key = str(uuid.uuid4())
websiteManager = WebsiteManager()


@app.route("/")
def main():
    return redirect(url_for("main_page"), code=302)


@app.route("/home")
def main_page():
    if 'username' in session:
        return render_template("index.html")
    return render_template("index.html")


@app.route("/me", methods=['GET', 'POST'])
def session_user_page():
    if 'username' in session:
        if request.method == 'POST':
            print(request.form)
        return render_template(
            "session_user_page.html",
            extensions=websiteManager.extensionManager.extensions
        )
    elif request.method == 'POST':
        username = request.form['username']
        if username is not '':
            session['username'] = username
            if username == "Tymec":
                session['isAdmin'] = True
            return redirect(url_for("session_user_page"))
    return render_template("login.html")


@app.route('/movie/<int:entry_id>')
def movie_page(entry_id):
    response = websiteManager.displayEntry(MediaType.MOVIE.value, entry_id)
    if response is -1:
        return redirect(url_for("not_found_404"), code=302)
    return str(response)


@app.route('/comic/<int:entry_id>')
def comic_page(entry_id):
    response = websiteManager.displayEntry(MediaType.COMIC.value, entry_id)
    if response is -1:
        return redirect(url_for("not_found_404"), code=302)
    return str(response)


@app.route('/music/<int:entry_id>')
def music_page(entry_id):
    response = websiteManager.displayEntry(MediaType.MUSIC.value, entry_id)
    if response is -1:
        return redirect(url_for("not_found_404"), code=302)
    return str(response)


@app.route('/game/<int:entry_id>')
def game_page(entry_id):
    response = websiteManager.displayEntry(MediaType.GAME.value, entry_id)
    if response is -1:
        return redirect(url_for("not_found_404"), code=302)
    return str(response)


@app.route('/book/<int:entry_id>')
def book_page(entry_id):
    response = websiteManager.displayEntry(MediaType.BOOK.value, entry_id)
    if response is -1:
        return redirect(url_for("not_found_404"), code=302)
    return str(response)


@app.route('/entry/<string:media_type>/<int:entry_id>')
def entry_page(media_type, entry_id):
    parameters = dict(parse.parse_qsl(request.query_string.decode("utf-8")))
    response = websiteManager.displayEntry(media_type, entry_id, parameters)
    if response is -1:
        return redirect(url_for("not_found_404"), code=302)
    elif type(response) is dict:
        return jsonify(response)
    return render_template("entry.html", entry=response)


@app.route("/user/", methods=['GET', 'POST'])
def social():
    if request.method == 'POST':
        return redirect(
            url_for(
                "user_page",
                username=request.form['username'],
                format='json'
            ),
            code=302
        )
    return render_template("search_user.html")


@app.route("/user/<string:username>/")
def user_page(username):
    parameters = dict(parse.parse_qsl(request.query_string.decode("utf-8")))
    response = websiteManager.displayUserList(parameters, username)
    if response is -1:
        return redirect(url_for("not_found_404"), code=302)
    return jsonify(response) if parameters.get('format') == 'json' else "<h1>NOT IMPLEMENTED YET</h1>"


@app.route("/browse", methods=["GET", "POST"])
def browse():
    parameters = dict(parse.parse_qsl(request.query_string.decode("utf-8")))
    if parameters == {}:
        if request.method == 'POST':
            return redirect(
                url_for(
                    "browse",
                    q=request.form["media"],
                    page=1,
                    media=request.form["media_type"]
                ),
                code=302
            )
        return render_template("browse.html", media_types=websiteManager.listManager.media_types.keys())
    response = websiteManager.searchEntry(parameters)
    if response is -1:
        return redirect(url_for("not_found_404"), code=302)
    elif type(response) is not list and response.get('response') is not None:
        return ujson.dumps(response)
    return render_template("search_result.html", response=response)


@app.route("/404")
def not_found_404():
    return "404 Not Found"
