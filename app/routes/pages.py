from flask import Blueprint, render_template


pages = Blueprint("pages", __name__)


@pages.route("/")
def home():
    return render_template("home.html")


@pages.route("/asr")
def asr_dashboard():
    return render_template("asr.html")


@pages.route("/tts")
def tts_dashboard():
    return render_template("tts.html")


@pages.route("/about")
def about_project():
    return render_template("about.html")
