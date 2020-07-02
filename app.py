import flask
import flask_login
from urllib.parse import urlparse, urljoin
import db
import bcrypt
app = flask.Flask(__name__)
app.secret_key = 'ee00d0998aikwdpoka--2-2-eeoddkkd'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

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

@app.route('/profile')
@flask_login.login_required
def myprofile():
    return flask.render_template("myprofile.html")

@app.route('/history', methods=['GET', 'POST'])
@flask_login.login_required
def history():
    if flask.request.method == 'POST':
        date = flask.request.form["date"]
        color = flask.request.form["color"]
        opinion = flask.request.form["opinon"]
        comments = flask.request.form["comments"]
        db.create_log(flask_login.current_user.id, date, color, opinion, comments)
    else:
        try:
            hid = flask.request.args.get("delete")
            db.delete_log(hid)
        except Exception as e:
            print(e)
    return flask.render_template("history.html", history_list=db.get_history(flask_login.current_user.id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        user = flask.request.form["username"]
        passw = flask.request.form["passwordname"].encode('utf-8')
        try:
            uid = db.get_uid(user)
        except:
            passwhash = bcrypt.hashpw(passw, bcrypt.gensalt())
            db.create_user(user, passwhash)
            uid = db.get_uid(user)
        print(uid)
        user_object = load_user(uid)
        print(user_object)
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
