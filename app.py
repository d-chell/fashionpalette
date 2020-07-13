import flask
import flask_login
from urllib.parse import urlparse, urljoin
import db
import os
import color
import bcrypt
import base64
from werkzeug.utils import secure_filename
app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.urandom(24)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(uid):
    return db.find_user(uid)

@login_manager.unauthorized_handler
def unauthorized():
    return flask.redirect(flask.url_for('login'))

def is_safe_url(target):
    ref_url = urlparse(flask.request.host_url)
    test_url = urlparse(urljoin(flask.request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route('/')
def home():
    return flask.render_template("home.html")

@app.route('/wiki')
def wiki():
    return flask.render_template("wiki.html")

@app.route('/profile', methods=['GET', 'POST'])
@flask_login.login_required
def myprofile():
    if flask.request.method == 'POST':
        if 'file' in flask.request.files:
            file = flask.request.files['file']
            if file.filename == '':
                flask.flash('No selected file')
                return flask.redirect(flask.request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                base64file = base64.b64encode(file.read())
                base64file = base64file.decode("ascii")
                db.store_profile(flask_login.current_user.id, base64file)
                print(filename, file.read())
        else:
            try:
                skintone = float(flask.request.form["skintone"])
                skincolor = float(flask.request.form["skincolor"])
                eyetone = float(flask.request.form["eyetone"])
                eyecolor = float(flask.request.form["eyecolor"])
                hairtone = float(flask.request.form["hairtone"])
                hairshade = float(flask.request.form["hairshade"])
                haircolor = float(flask.request.form["haircolor"])
            except:
                return("Invalid data.")
            print("skintone", skintone, "skincolor", skincolor, "eyetone", eyetone, "eyecolor", eyecolor, "hairtone", hairtone, "hairshade", hairshade, "haircolor", haircolor)
            if skintone < 0:
                skincolor = 6 - skincolor
            skin = skintone * skincolor
            if eyetone < 0:
                eyecolor = 7 - eyecolor
            eyes = eyetone * eyecolor
            hair = hairtone * haircolor * hairshade
            db.store_palette(flask_login.current_user.id, skin, eyes, hair)
    palette = db.get_palette(flask_login.current_user.id)
    if palette:
        skin, eyes, hair = palette
        print("skin", skin, "eyes", eyes, "hair", hair)
        y = color.get_y(skin, eyes, hair)
        print("y", y)
        try:
            modifier, season = color.get_season(abs(hair)-6, y)
            result = modifier + " " + season
        except Exception as e:
            print(e)
            result = "unknown, please try again."
    else:
        result = "unknown, as you have not submitted your information yet!"
    profilepic = db.get_profile(flask_login.current_user.id)
    return flask.render_template("myprofile.html", result=result, profilepic=profilepic)

@app.route('/history', methods=['GET', 'POST'])
@flask_login.login_required
def history():
    if flask.request.method == 'POST':
        date = flask.request.form["date"]
        color = flask.request.form["color"]
        opinion = flask.request.form["opinion"]
        comments = flask.request.form["comments"]
        db.create_log(flask_login.current_user.id, date, color, opinion, comments)
    else:
        try:
            hid = flask.request.args.get("delete")
            db.delete_log(hid)
        except Exception as e:
            print(e)
    history_list = db.get_history(flask_login.current_user.id)
    graph_list = []
    if history_list[0]:
        history_list.sort(reverse=True, key=lambda tup: tup[2])
        graph_list = history_list.copy()
        graph_list.sort(key=lambda tup: tup[2])
    return flask.render_template("history.html", history_list=history_list, graph_list=graph_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        user = flask.request.form["username"]
        passw = flask.request.form["passwordname"].encode('utf-8')
        if not passw:
            return("Please enter a password.")
        try:
            uid = db.get_uid(user)
        except:
            passwhash = bcrypt.hashpw(passw, bcrypt.gensalt())
            db.create_user(user, passwhash)
            uid = db.get_uid(user)
        user_object = load_user(uid)
        if not db.login_auth(uid, passw):
            return("Invalid password.")
        flask_login.login_user(user_object)
        flask.flash('Logged in successfully!')
        next = flask.request.args.get('next')
        # Open redirect protection
        if not is_safe_url(next):
            return flask.abort(400)
        return flask.redirect(next or flask.url_for("home"))
    else:
        error = "Invalid username or password."
    return flask.render_template('login.html', error=error)

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('home'))

# db.reset()
app.run(debug=True)
