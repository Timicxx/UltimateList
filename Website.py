from flask import Flask, redirect, jsonify, render_template, session, escape, request, url_for
import uuid
import ujson

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
        return render_template(
            "index.html",
            username=escape(session['username'])
        )
    return render_template("index.html")


@app.route("/me")
def me_page():
    if 'username' in session:
        return render_template(
            "me.html",
            username=escape(session['username'])
        )
    return redirect(url_for("login"), code=302)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for("me_page"))
    return '''
            <form method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Login>
            </form>
        '''


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


@app.route("/user/", methods=['GET', 'POST'])
def search_user():
    if request.method == 'POST':
        return redirect(
            url_for(
                "user_page",
                username=request.form["username"]
            ),
            code=302
        )
    return render_template("search_user.html")


@app.route("/user/<string:username>/")
def user_page(username):
    response = websiteManager.getAllUserLists(username)
    if response is -1:
        return redirect(url_for("not_found_404"), code=302)
    return jsonify(response)


@app.route("/user/<string:username>/<string:media_type>")
def user_page_media(media_type, username):
    response = websiteManager.displayUserList(media_type, username)
    if response is -1:
        return redirect(url_for("not_found_404"), code=302)
    return jsonify(response)


@app.route("/search/<string:media_type>/<string:search_input>/<int:page_number>")
def search_page(media_type, search_input, page_number):
    parameters = request.query_string
    response = websiteManager.searchEntry(media_type, search_input, page_number, parameters)
    if response is -1:
        return redirect(url_for("not_found_404"), code=302)
    elif type(response) is dict:
        return ujson.dumps(response)
    return render_template("media.html", response=response, media=media_type)


@app.route("/browse", methods=["GET", "POST"])
def browse():
    if request.method == 'POST':
        return redirect(
            url_for(
                "search_page",
                search_input=request.form["media"],
                page_number=1,
                media_type=request.form["media_type"]
            ),
            code=302
        )
    return render_template("search_media.html", code=302)


@app.route("/404")
def not_found_404():
    return "404 Not Found"
