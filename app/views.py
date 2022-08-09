import base64, io
from functools import wraps
from urllib.request import HTTPBasicAuthHandler
from flask import render_template, request, url_for, redirect, flash, session, send_file
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from app import app
from app.models import Users, db
from app.dict import img_dict
from app import service

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            return redirect('/login', code=302)

        email_list = [t for t in db.session.query(Users.email).all() if session["email"] in t]

        if session["email"] != email_list[0][0]:
            return redirect('/login', code=302)
        
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login")
@app.route("/")
def showLoginPage():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def addLoginUser():
    email = request.form.get("email")
    password = request.form.get("password")

    session["email"] = email

    if (db.session.query(Users).filter(Users.email == email).all()):
        user = db.session.query(Users).filter(Users.email==email).first()
        return render_template("list-project.html", filename=user.filename)

    new_user = Users(email=email, password=password, img=None, mimetype=None)

    db.session.add(new_user)
    db.session.commit()

    return render_template("list-project.html")

@app.route("/ongoing-project")
@login_required
def ongoingProject():
    img_dict["pic"] = db.session.query(Users).filter(Users.email==session["email"]).first().img
    img_dict["filename"] = db.session.query(Users).filter(Users.email==session["email"]).first().filename
    img_dict["mimetype"] = db.session.query(Users).filter(Users.email==session["email"]).first().mimetype

    return editorPage()

@app.route("/file-upload")
@login_required
def showFileUploadPage():
    return render_template("file-upload.html")

@app.route("/file-upload", methods=["POST"])
def fileUploadPage():
    pic = request.files["pic"]
    if not pic:
            flash("No file selected.")
            return redirect(url_for("showFileUploadPage"))
    
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype

    img_dict["pic"] = pic.read()
    img_dict["filename"] = filename
    img_dict["mimetype"] = mimetype
    
    return redirect(url_for("editorPage"))

@app.route("/editor", methods=["GET", "POST"])
@login_required
def editorPage():

    try:
        pic = img_dict["pic"]
    except:
        return redirect("/login")

    if "rotate_slider" in request.form:
        angle = request.form.get("rotate_slider")
        img = service.rotate_img(pic, angle)
        img_dict["pic"] = base64.b64decode(img)
        return render_template("editor.html", img=img)

    if "black_and_white_btn" in request.form:
        img = service.black_and_white_img(pic)
        img_dict["pic"] = base64.b64decode(img)
        return render_template("editor.html", img=img)
    
    if "flip_btn" in request.form:
        img = service.flip_img(pic)
        img_dict["pic"] = base64.b64decode(img)
        return render_template("editor.html", img=img)
    
    if "blur_slider" in request.form:
        amt = request.form.get("blur_slider")
        img = service.blur_img(pic, amt)
        img_dict["pic"] = base64.b64decode(img)
        return render_template("editor.html", img=img)
    
    if "smooth_btn" in request.form:
        img = service.smooth_img(pic)
        img_dict["pic"] = base64.b64decode(img)
        return render_template("editor.html", img=img)
    
    if "sharp_btn" in request.form:
        img = service.sharp_img(pic)
        img_dict["pic"] = base64.b64decode(img)
        return render_template("editor.html", img=img)
    
    if "edge_detec_btn" in request.form:
        img = service.edge_detection(pic)
        img_dict["pic"] = base64.b64decode(img)
        return render_template("editor.html", img=img)
    
    if "emboss_btn" in request.form:
        img = service.emboss_img(pic)
        img_dict["pic"] = base64.b64decode(img)
        return render_template("editor.html", img=img)
    
    if "contrast_slider" in request.form:
        amt = request.form.get("contrast_slider")
        img = service.contrast_img(pic, amt)
        img_dict["pic"] = base64.b64decode(img)
        return render_template("editor.html", img=img)
    
    if "bright_slider" in request.form:
        amt = request.form.get("bright_slider")
        img = service.bright_img(pic, amt)
        img_dict["pic"] = base64.b64decode(img)
        return render_template("editor.html", img=img)
    
    if "color_picker" in request.form:
        color = request.form.get("color_picker")
        border_width = int(request.form.get("border_width"))
        img = service.add_border(pic, color, border_width)
        img_dict["pic"] = base64.b64decode(img)
        return render_template("editor.html", img=img)
    
    if "text_picker" in request.form:
        color = request.form.get("color_picker_2")
        text = request.form.get("text_picker")
        img = service.add_caption(pic, color, text)
        img_dict["pic"] = base64.b64decode(img)
        return render_template("editor.html", img=img)

    return render_template("editor.html", img=base64.b64encode(pic).decode("utf-8"))

@app.route("/save")
@login_required
def save_img():
    Users.query.filter_by(email=session["email"]).update({Users.img: img_dict["pic"]}, synchronize_session = False)
    Users.query.filter_by(email=session["email"]).update({Users.filename: img_dict["filename"]}, synchronize_session = False)
    Users.query.filter_by(email=session["email"]).update({Users.mimetype: img_dict["mimetype"]}, synchronize_session = False)

    db.session.commit()

    flash("Project saved.")
    return editorPage()

@app.route("/donwload-img")
@login_required
def download_img():
    return send_file(io.BytesIO(img_dict["pic"]), download_name=img_dict["filename"], as_attachment=True)

@app.route("/logout")
def logoutPage():
    if "email" in session:
        session.clear()

    img_dict.clear()
    
    flash("You have been successfully logged out. Cookies Cleared.")
    return redirect(url_for("showLoginPage"))