from flask import Flask, redirect, jsonify, render_template, session, request, url_for, send_from_directory
import uuid
import ujson
import os
from urllib import parse

from modules.Manager import WebsiteManager

app = Flask("UltimateList")
app.secret_key = str(uuid.uuid4())
websiteManager = WebsiteManager()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/")
def main():
    return redirect(url_for("main_page"), code=301)


@app.route("/home", methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST' and session['username']:
        session.pop('username')
    return render_template("index.html")


@app.route("/me", methods=['GET', 'POST'])
def session_user_page():
    if 'username' in session:
        if request.method == 'POST':
            websiteManager.toggleExtensions(request.form)
        return render_template(
            "session_user_page.html",
            extensions=websiteManager.extensionManager.extensions
        )
    elif request.method == 'POST':
        username = request.form['username']
        if username is not '':
            session['username'] = username
            if username in websiteManager.admin_list:
                session['isAdmin'] = True
            return redirect(url_for("session_user_page"))
    return render_template("login.html")


@app.route('/entry/<string:media_type>/<int:entry_id>')
def entry_page(media_type, entry_id):
    parameters = dict(parse.parse_qsl(request.query_string.decode("utf-8")))
    response = websiteManager.displayEntry(media_type, entry_id, parameters)
    if response is -1:
        return redirect(url_for("not_found_404"), code=301)
    elif type(response) is dict:
        return jsonify(response)
    return render_template("entry.html", entry=response)


@app.route("/user", methods=['GET', 'POST'])
def social():
    parameters = dict(parse.parse_qsl(request.query_string.decode("utf-8")))
    if parameters == {}:
        if request.method == 'POST':
            return redirect(
                url_for(
                    "social",
                    username=request.form['username'],
                    format='json'
                ),
                code=301
            )
        return render_template("search_user.html")
    response = websiteManager.displayUserList(parameters)
    if response is -1:
        return redirect(url_for("not_found_404"), code=301)
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
                code=301
            )
        return render_template("browse.html", media_types=websiteManager.listManager.media_types.keys())
    response = websiteManager.searchEntry(parameters)
    if response is -1:
        return redirect(url_for("not_found_404"), code=301)
    elif type(response) is not list and response.get('response') is not None:
        return ujson.dumps(response)
    return render_template("search_result.html", response=response)


@app.route("/404")
def not_found_404():
    return "404 Not Found"


if __name__ == "__main__":
    context = (
        'path/to/ssl/server.crt'
        'path/to/ssl/server.key'
    )
    app.run(
        ssl_context=context
    )
