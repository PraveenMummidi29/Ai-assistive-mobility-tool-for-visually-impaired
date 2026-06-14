# -*- coding: utf-8 -*-


from google.colab import drive
drive.mount('/content/drive')

# -*- coding: utf-8 -*-


!pip install flask pyngrok werkzeug sqlite3

import os
import sqlite3
import time # Import for optimization timing (optional, but helpful)

# Folders for templates and uploads
os.makedirs("/content/templates", exist_ok=True)
os.makedirs("/content/uploads", exist_ok=True)
os.makedirs("/content/processed", exist_ok=True)

# SQLite DB path
DB_PATH = "/content/users.db"

# Create table if not exists
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()
conn.close()

# Helper function for DB connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- HELPER FOR PROFILE DROPDOWN ---
def get_user_info(email):
    conn = get_db_connection()
    user = conn.execute("SELECT first_name, last_name, email FROM users WHERE email=?", (email,)).fetchone()
    conn.close()
    return dict(user) if user else None

# ----------------- MODIFIED LOGIN PAGE (vh -> %) -----------------
login_html = """
<!DOCTYPE html>
<html>
<head>
<style>
html, body {
  height: 100%; /* FIX: Ensures 100% height works */
  margin: 0;
  padding: 0;
}
body {
  background: url('https://images.unsplash.com/photo-1761335044629-611c11976356?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHx0b3BpYy1mZWVkfDc3fGJvOGpRS1RhRTBZfHxlbnwwfHx8fHw%3D') no-repeat center center fixed;
  background-size: cover;
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%; /* FIX: 100vh changed to 100% */
  margin: 0;
}
.project-title {
  font-size: 2.0em;
  font-weight: bold;
  color: #333;
  background: rgba(255,255,255,0.60);
  border-radius: 16px;
  padding: 16px 32px;
  margin-bottom: 22px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  letter-spacing: 1px;
}
.card {
  backdrop-filter: blur(12px);
  background: rgba(255,255,255,0.30);
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  padding: 40px 30px;
  text-align: center;
  width: 350px;
}
input {
  margin: 10px 0;
  padding: 12px;
  width: 100%;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 16px;
  box-sizing: border-box;
}
button {
  padding: 12px 22px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(45deg,#6e8efb,#a777e3);
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: opacity 0.2s;
}
button:hover { opacity: 0.85; }
a { color: #333; text-decoration: none; font-weight: bold; }
p.error { color: red; font-weight: bold; }
</style>
</head>
<body>
<div class="project-title">AI Tool for Visually Impaired</div>
<div class="card">
<h2>Login</h2>
{% if error %}<p class="error">{{ error }}</p>{% endif %}
<form method="post">
<input type="email" name="email" placeholder="Email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Login</button>
</form>
<p>Don't have an account? <a href="/signup">Signup</a></p>
</div>
</body>
</html>
"""
with open("/content/templates/login.html","w") as f:
    f.write(login_html)

# ----------------- MODIFIED SIGNUP PAGE (vh -> %) -----------------
signup_html = """
<!DOCTYPE html>
<html>
<head>
<style>
html, body {
  height: 100%; /* FIX: Ensures 100% height works */
  margin: 0;
  padding: 0;
}
body {
  background: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1920&q=80') no-repeat center center fixed;
  background-size: cover;
  font-family: Arial, sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%; /* FIX: 100vh changed to 100% */
  margin: 0;
}
.card {
  backdrop-filter: blur(12px);
  background: rgba(255,255,255,0.30);
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  padding: 40px 30px;
  text-align: center;
  width: 350px;
}
input {
  margin: 10px 0;
  padding: 12px;
  width: 100%;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 16px;
  box-sizing: border-box;
}
button {
  padding: 12px 22px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(45deg,#6e8efb,#a777e3);
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: opacity 0.2s;
}
button:hover { opacity:0.85; }
a { color: #333; text-decoration: none; font-weight: bold; }
p.error { color:red; font-weight:bold; }
</style>
</head>
<body>
<div class="card">
<h2>Signup</h2>
{% if error %}<p class="error">{{ error }}</p>{% endif %}
<form method="post">
<input type="text" name="first_name" placeholder="First Name" required>
<input type="text" name="last_name" placeholder="Last Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="password" name="password" placeholder="Password" required>
<input type="password" name="confirm_password" placeholder="Confirm Password" required>
<button type="submit">Signup</button>
</form>
<p>Already have an account? <a href="/login">Login</a></p>
</div>
</body>
</html>
"""
with open("/content/templates/signup.html","w") as f:
    f.write(signup_html)

# ----------------- MODIFIED INFO PAGE (vh -> %) -----------------
info_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Project Information</title>
    <style>
        /* --- Global FIX --- */
        html, body {
            height: 100%; /* FIX: Ensures 100% height works as vh equivalent */
            margin: 0;
            padding: 0;
        }
        /* --- General Layout --- */
        body {
            background: url('https://plus.unsplash.com/premium_photo-1661962394624-ebba47063dbe?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            height: 100%; /* FIX: 100vh changed to 100% */
            margin: 0;
            color: #333;
            overflow: hidden;
        }

        /* --- Left Column: Title (One-Third) --- */
        .left-panel {
            width: 33.33%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(10px);
            box-shadow: 4px 0 15px rgba(0, 0, 0, 0.3);
        }
        .project-title-lg {
            font-size: 2.5em;
            font-weight: 700;
            color: #FFFFFF;
            text-shadow: 0 0 10px rgba(0, 0, 0, 0.9), 0 0 20px #007bff;
            text-align: center;
        }

        /* --- Right Column: Info Card (Two-Thirds) --- */
        .right-panel {
            width: 66.67%;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .card {
            backdrop-filter: blur(15px);
            background: rgba(255, 255, 255, 0.45);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            padding: 50px 40px;
            text-align: center;
            width: 80%;
            max-width: 600px;
            color: #333;
        }
        h2 {
            color: #004d99;
            margin-bottom: 30px;
            font-size: 1.8em;
        }
        ul {
            list-style: none;
            padding: 0;
            text-align: left;
            margin-top: 20px;
        }
        li {
            background: rgba(255, 255, 255, 0.9);
            margin: 10px 0;
            padding: 12px;
            border-left: 5px solid #007bff;
            border-radius: 5px;
            font-size: 1.0em;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        /* --- Navigation & Button Styling --- */
        .start-button {
            display: block;
            width: 80%;
            max-width: 300px;
            margin: 30px auto 10px;
            padding: 15px 30px;
            border: none;
            border-radius: 15px;
            background: linear-gradient(45deg, #28a745, #1e7e34); /* Green Gradient */
            color: white;
            font-size: 1.3em; /* Slightly smaller */
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        .start-button:hover {
            background: linear-gradient(45deg, #1e7e34, #28a745);
            box-shadow: 0 8px 20px rgba(40, 167, 69, 0.6);
        }

        /* --- Profile Dropdown (Copied from upload.html) --- */
        .profile-container {
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 10;
        }
        .profile-button {
            background: #fff;
            border: 1px solid #ccc;
            border-radius: 50%;
            padding: 10px;
            cursor: pointer;
            font-weight: bold;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: background 0.2s;
        }
        .profile-button:hover { background: #f0f0f0; }
        .dropdown-content {
            display: none;
            position: absolute;
            background-color: #fff;
            min-width: 200px;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            padding: 12px;
            border-radius: 8px;
            top: 55px;
            right: 0;
        }
        .dropdown-content p { margin: 5px 0; font-size: 0.9em; }
        .dropdown-content .name { font-size: 1.1em; font-weight: bold; color: #004d99; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 8px;}
        .dropdown-content a {
            padding: 8px 0;
            text-decoration: none;
            display: block;
            text-align: left;
            color: #cc0000;
            border-top: 1px solid #eee;
            margin-top: 8px;
        }
        .dropdown-content a:hover { color: #ff3333; }
        .show { display: block; }

    </style>
</head>
<body>

    <div class="profile-container">
        <button class="profile-button" onclick="toggleDropdown()">👤</button>
        <div id="profileDropdown" class="dropdown-content">
            <p class="name">{% if user_info %}{{ user_info['first_name'] }} {{ user_info['last_name'] }}{% else %}Guest{% endif %}</p>
            <p>Email: {% if user_info %}{{ user_info['email'] }}{% else %}N/A{% endif %}</p>
            <a href="{{ url_for('logout') }}">Logout</a>
        </div>
    </div>

    <div class="left-panel">
        <div class="project-title-lg">
            AI-Powered Assistive Mobility Tool for Visually Impaired
        </div>
    </div>

    <div class="right-panel">
        <div class="card">
            <h2>Project Overview & Features</h2>
            <p style="margin-bottom: 30px; font-size: 1.1em;">This system enhances mobility and safety for the visually impaired by processing video footage and providing synchronized audio guidance.</p>

            <ul>
                <li><strong>Dual-Model Object Detection:</strong> Uses custom-trained and general YOLO models to detect pedestrians, vehicles, traffic lights, and hazards.</li>
                <li><strong>Distance Estimation:</strong> Calculates approximate distances (in meters) to detected objects for clear guidance.</li>
                <li><strong>Intelligent Narration:</strong> Summarizes scene data and generates continuous, human-like voice descriptions** using OpenAI and gTTS.</li>
                <li><strong>Video Speed Synchronization:</strong> Adjusts video playback speed to match the length of the generated audio narration.</li>
            </ul>

            <a href="{{ url_for('upload_video') }}" class="start-button">Start Detection</a>
        </div>
    </div>

<script>
    // Profile Dropdown JS (Copied from upload.html)
    function toggleDropdown() {
        document.getElementById("profileDropdown").classList.toggle("show");
    }

    window.onclick = function(event) {
      if (!event.target.matches('.profile-button') && !event.target.matches('.profile-button *')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
          var openDropdown = dropdowns[i];
          if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
          }
        }
      }
    }
</script>
</body>
</html>
"""
with open("/content/templates/info.html","w") as f:
    f.write(info_html)

# ----------------- MODIFIED UPLOAD PAGE (vh -> %) -----------------
upload_html = """
<!DOCTYPE html>
<html>
<head>
<title>Upload Video - AI Tool</title>
<style>
/* --- Global FIX --- */
html, body {
  height: 100%; /* FIX: Ensures 100% height works as vh equivalent */
  margin: 0;
  padding: 0;
}
/* --- General Layout --- */
body {
  background: url('https://images.unsplash.com/photo-1758132123976-6730692335f7?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB4b3BpYy1mZWVkfDg5fGJvOGpRS1RhRTBZfHxlbnwwfHx8fHw%3D') no-repeat center center fixed;
  background-size: cover;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  display: flex;
  height: 100%; /* FIX: 100vh changed to 100% */
  margin: 0;
  color: #333;
  overflow: hidden;
}

/* --- Left Column: Title (One-Third) --- */
.left-panel {
  width: 33.33%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  box-shadow: 4px 0 15px rgba(0, 0, 0, 0.3);
}
.project-title-lg {
  font-size: 2.5em;
  font-weight: 700;
  color: #FFFFFF;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.9), 0 0 20px #007bff;
  text-align: center;
}

/* --- Right Column: Upload Card (Two-Thirds) --- */
.right-panel {
  width: 66.67%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  position: relative; /* Needed for absolute positioning of back button */
}
.card {
  backdrop-filter: blur(15px);
  background: rgba(255, 255, 255, 0.45);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  padding: 50px 40px;
  text-align: center;
  width: 80%;
  max-width: 600px;
}
h2 { color: #004d99; margin-bottom: 30px; }
input[type="file"] {
  margin: 20px 0;
  padding: 15px;
  width: 100%;
  border-radius: 12px;
  border: 1px solid #004d99;
  background: rgba(255,255,255,0.7);
  cursor: pointer;
  font-size: 16px;
  box-sizing: border-box;
}
button {
  padding: 12px 25px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(45deg, #007bff, #0056b3);
  color: white;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: all 0.3s ease;
}
button:hover {
  background: linear-gradient(45deg, #0056b3, #007bff);
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.4);
}
p.status { margin-top: 20px; font-weight: bold; color: #cc0000; }
a { color: #004d99; text-decoration: none; font-weight: bold; }

/* --- Download Button Specific Style --- */
.download-button {
    display: inline-block;
    padding: 12px 25px;
    margin-top: 20px;
    border: none;
    border-radius: 10px;
    background: linear-gradient(45deg, #28a745, #1e7e34); /* Green Gradient */
    color: white;
    font-size: 16px;
    font-weight: bold;
    text-decoration: none; /* Make it look like a button */
    cursor: pointer;
    transition: all 0.3s ease;
}
.download-button:hover {
    background: linear-gradient(45deg, #1e7e34, #28a745);
    box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
}

/* --- Profile Dropdown (Top Right) --- */
.profile-container {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10;
}
.profile-button {
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 50%;
  padding: 10px;
  cursor: pointer;
  font-weight: bold;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: background 0.2s;
}
.profile-button:hover { background: #f0f0f0; }
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #fff;
  min-width: 200px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  padding: 12px;
  border-radius: 8px;
  top: 55px;
  right: 0;
}
.dropdown-content p { margin: 5px 0; font-size: 0.9em; }
.dropdown-content .name { font-size: 1.1em; font-weight: bold; color: #004d99; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 8px;}
.dropdown-content a {
  padding: 8px 0;
  text-decoration: none;
  display: block;
  text-align: left;
  color: #cc0000;
  border-top: 1px solid #eee;
  margin-top: 8px;
}
.dropdown-content a:hover { color: #ff3333; }
.show { display: block; }

/* --- Back Link Button (FIXED) --- */
.back-link-button {
    position: absolute;
    top: 25px;
    left: 25px; /* Positioned relative to the whole body */
    z-index: 20;
    padding: 8px 15px;
    background: rgba(255, 255, 255, 0.9);
    color: #007bff;
    font-weight: bold;
    border-radius: 8px;
    text-decoration: none;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: background 0.2s;
}
.back-link-button:hover {
    background: #f0f0f0;
}

</style>
</head>
<body>

<a href="{{ url_for('info_page') }}" class="back-link-button" title="Back to Info Page">
    &#x2190; Back
</a>

<div class="profile-container">
    <button class="profile-button" onclick="toggleDropdown()">👤</button>
    <div id="profileDropdown" class="dropdown-content">
        <p class="name">{% if user_info %}{{ user_info['first_name'] }} {{ user_info['last_name'] }}{% else %}Guest{% endif %}</p>
        <p>Email: {% if user_info %}{{ user_info['email'] }}{% else %}N/A{% endif %}</p>
        <a href="{{ url_for('logout') }}">Logout</a>
    </div>
</div>

<div class="left-panel">
    <div class="project-title-lg">
        AI-Powered Assistive Mobility Tool for Visually Impaired
    </div>
</div>

<div class="right-panel">
    <div class="card">
        <h2>Upload Video for Processing</h2>
        <form method="post" enctype="multipart/form-data" id="uploadForm">
            <input type="file" name="video" accept="video/*" required>
            <br>
            <button type="submit">Upload & Process</button>
        </form>
        <p class="status" id="statusMsg" style="display:none;">Processing video... This might take a moment.</p>

        {% if output_video_url %}
            <h3 style="margin-top: 30px; color: #004d99;">Processed Output Video</h3>
            <video width="100%" controls style="border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <source src="{{ output_video_url }}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <a href="{{ output_video_url }}" download="processed_video.mp4" class="download-button">
                Download Video
            </a>
            {% endif %}
    </div>
</div>

<script>
    const form = document.getElementById("uploadForm");
    const statusMsg = document.getElementById("statusMsg");
    form.addEventListener("submit", function() {
        if(form.video.files.length > 0) {
            statusMsg.style.display = "block";
        }
    });

    function toggleDropdown() {
        document.getElementById("profileDropdown").classList.toggle("show");
    }

    window.onclick = function(event) {
      if (!event.target.matches('.profile-button') && !event.target.matches('.profile-button *')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
          var openDropdown = dropdowns[i];
          if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
          }
        }
      }
    }
</script>
</body>
</html>
"""
with open("/content/templates/upload.html", "w") as f:
    f.write(upload_html)


from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "/content/uploads"
PROCESSED_FOLDER = "/content/processed"

@app.route("/")
def index():
    return redirect(url_for("login"))

# Login
@app.route("/login", methods=["GET","POST"])
def login():
    error = None
    if request.method=="POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password"], password):
            session["user"] = email
            # Redirect to the new info page after successful login
            return redirect(url_for("info_page"))
        else:
            error = "No user found with these credentials!"
    return render_template("login.html", error=error)

# Signup
@app.route("/signup", methods=["GET","POST"])
def signup():
    error = None
    if request.method=="POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            error = "Passwords do not match!"
        else:
            hashed = generate_password_hash(password)
            conn = get_db_connection()
            try:
                conn.execute("INSERT INTO users (first_name,last_name,email,password) VALUES (?,?,?,?)",
                             (first_name,last_name,email,hashed))
                conn.commit()
                conn.close()
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                error = "Email already exists!"
            finally:
                conn.close()
    return render_template("signup.html", error=error)

# --- INFO PAGE ROUTE ---
@app.route("/info")
def info_page():
    if 'user' not in session:
        return redirect(url_for("login"))
    # Fetch user info for the profile dropdown
    user_info = get_user_info(session['user'])
    return render_template("info.html", user_info=user_info)


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Install ML dependencies
!pip install pyngrok ultralytics openai transformers pydub soundfile moviepy gtts


# ---------------- IMPORTS ----------------
from ultralytics import YOLO
import cv2
from openai import OpenAI
# The VitsModel and AutoTokenizer are not used in the current version of the code,
# but I'll keep the import in case you plan to use them later.
from transformers import VitsModel, AutoTokenizer
import torch
import soundfile as sf
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
from gtts import gTTS # Moved here for consistency

# --- Detect GPU ---
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Using device:", device)

# ---------------- USER CONFIG ----------------
# NOTE: Replace this with your actual key if needed outside of this execution
OPENAI_API_KEY = ""
PRETRAINED_YOLO = "yolov8n.pt"
CUSTOM_MODEL_PATH = "/content/drive/MyDrive/infosys/trained_model/v1/weights/best.pt"

OUT_W, OUT_H = 640, 384
VIDEO_FPS = 30.0
CONF_THRESH = 0.35

# --- OPTIMIZATION CONSTANT ---
FRAME_SAMPLE_RATE = 5 # Process one out of every 5 frames for logging/narration summary

# ---------------- INITIALIZE MODELS ----------------
openai_client = OpenAI(api_key=OPENAI_API_KEY)

print("Loading YOLO models...")
pretrained_model = YOLO(PRETRAINED_YOLO)
custom_model = YOLO(CUSTOM_MODEL_PATH)

print("Loading TTS model...")

# ---------------- SIZE TO DISTANCE TABLE ----------------
KNOWN_HEIGHTS = {
    "person": 170, # Changed to cm for consistency with focal length calculation
    "car": 150,
    "motorcycle": 110,
    "bus": 300,
    "truck": 320,
    "bicycle": 160,
    "traffic light": 120,
    "zebracrossing": 70,
}

focal_length_pixels = OUT_W * 1.2

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


if "upload_video" in app.view_functions:
    del app.view_functions["upload_video"]

# --- OPTIMIZED upload_video ROUTE ---
@app.route("/upload_video", methods=["GET", "POST"])
def upload_video():
    if 'user' not in session:
        return redirect(url_for("login"))

    # Fetch user info for the profile dropdown
    user_info = get_user_info(session['user'])
    if not user_info:
        # Should not happen, but a safe fallback
        session.clear()
        return redirect(url_for("login"))

    output_video_url = None
    if request.method == "POST":
        start_time = time.time() # Start timing

        # --- Save uploaded file ---
        file = request.files["video"]
        if not file:
            return render_template("upload.html", error="No file uploaded.", user_info=user_info)

        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        input_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(input_path)

        detected_video_filename = "detected_" + unique_filename
        narration_audio_filename = f"narration_{uuid.uuid4().hex}.mp3"
        final_video_filename = "final_" + unique_filename

        detected_video_path = os.path.join(PROCESSED_FOLDER, detected_video_filename)
        narration_audio_path = os.path.join(PROCESSED_FOLDER, narration_audio_filename)
        final_video_path = os.path.join(PROCESSED_FOLDER, final_video_filename)


        # --- Object Detection & Optimized Logging ---
        cap = cv2.VideoCapture(input_path)
        frame_count = 0
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(detected_video_path, fourcc, VIDEO_FPS, (OUT_W, OUT_H))
        frame_detections_lines = [] # Collects labels only for sampled frames

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_resized = cv2.resize(frame, (OUT_W, OUT_H))
            labels_with_distance = []

            # Combined YOLO Detection
            all_results = [
                (pretrained_model(frame_resized, conf=CONF_THRESH, device=device), pretrained_model.names, (0, 0, 255)), # Red BGR
                (custom_model(frame_resized, conf=CONF_THRESH, device=device), custom_model.names, (255, 0, 0)) # Blue BGR
            ]

            for results, names, color in all_results:
                for box in results[0].boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = int(box.cls[0])
                    label = names[cls]

                    pixel_height = abs(y2 - y1)

                    # Distance calculation (in meters for display)
                    distance_m = -1.0
                    if label in KNOWN_HEIGHTS and pixel_height > 0:
                        distance_cm = (KNOWN_HEIGHTS[label] * focal_length_pixels) / pixel_height
                        distance_m = distance_cm / 100.0
                        label_text = f"{label} {distance_m:.1f}m"
                    else:
                        label_text = label

                    # Draw bounding box and label
                    cv2.rectangle(frame_resized, (x1, y1), (x2, y2), color, 2)
                    (tw, th), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    cv2.rectangle(frame_resized, (x1, y1 - th - 6), (x1 + tw + 4, y1), (255, 255, 255), -1)
                    cv2.putText(frame_resized, label_text, (x1 + 2, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

                    # --- OPTIMIZATION: Only log for a sampled frame ---
                    if frame_count % FRAME_SAMPLE_RATE == 0:
                        labels_with_distance.append(label_text)

            # Write annotated frame to output video
            out.write(frame_resized)

            # Append sampled frame detections
            if labels_with_distance and (frame_count % FRAME_SAMPLE_RATE == 0):
                frame_detections_lines.append(f"Frame {frame_count}: {', '.join(labels_with_distance)}")

            frame_count += 1

        cap.release()
        out.release()
        os.remove(input_path) # Clean up original upload

        # --- Summarize detections (using sampled data) ---
        object_counts = {}
        for line in frame_detections_lines:
            if ":" not in line: continue
            items = line.split(":")[1].split(",")
            for it in items:
                it = it.strip()
                if it=="": continue
                # Extract object name (e.g., 'person' from 'person 3.5m')
                base = it.split()[0].lower()
                object_counts[base] = object_counts.get(base,0)+1

        # Filter objects seen too few times (e.g., less than once every 5 seconds)
        min_seen = max(1, frame_count // (VIDEO_FPS * 5))
        scene_summary = "\n".join([f"{k}: seen {v} times" for k,v in object_counts.items() if v >= min_seen]) or "No consistent or clear objects detected."

        # --- Generate narration with OpenAI (Reduced Max Tokens) ---
        prompt = f"""
        You are a real-world navigation guide assisting a blind person.
        The video was sampled at a rate of 1 frame per {FRAME_SAMPLE_RATE}.
        Scene data summary: {scene_summary}
        Based on the summary, generate a single, encouraging, and continuous narration of ~30-45 seconds for a visually impaired user. Do not mention frame numbers or object count. Focus on describing the surroundings and distances clearly.
        """
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}],
            temperature=0.9,
            max_tokens=250 # Reduced for faster response
        )
        narration_text = response.choices[0].message.content.strip()

        # --- Convert narration to audio (gTTS) ---
        tts = gTTS(text=narration_text, lang='en', slow=False)
        tts.save(narration_audio_path)

        # --- Merge video + audio ---
        video_clip = VideoFileClip(detected_video_path)
        audio_clip = AudioFileClip(narration_audio_path)

        # Calculate speed factor to match video duration to audio duration
        SLOW_FACTOR = audio_clip.duration / video_clip.duration

        # Apply speed change and set audio
        final_clip = video_clip.fx(vfx.speedx, factor=1/SLOW_FACTOR).set_audio(audio_clip)

        # Write final video
        final_clip.write_videofile(
            final_video_path,
            codec="libx264",
            audio_codec="aac",
            fps=VIDEO_FPS
        )

        # Clean up intermediate files
        os.remove(detected_video_path)
        os.remove(narration_audio_path)

        end_time = time.time()
        print(f"Total processing time: {end_time - start_time:.2f} seconds")

        # Set the final video URL to be served from /processed/
        output_video_url = f'/processed/{os.path.basename(final_video_path)}'

    return render_template("upload.html", output_video_url=output_video_url, user_info=user_info) # Pass user_info here

# --- FILE SERVING ROUTE ---
@app.route('/processed/<filename>')
def serve_processed_file(filename):
    # This route serves files from the PROCESSED_FOLDER
    return send_from_directory(PROCESSED_FOLDER, filename)


# ---------------- START FLASK & NGROK ----------------
from pyngrok import ngrok
import threading

# Re-set your ngrok token
!ngrok authtoken 35W2DYWYBFk6tw7kz6esodx6lFv_3skqsjmv7dGQqAz3YdSKG

public_url = ngrok.connect(5000, bind_tls=True)
print("🚀 NEW Public URL:", public_url)

# Function to run Flask app
def run_app():
    # Set use_reloader=False to prevent the app from trying to start twice
    app.run(port=5000, use_reloader=False)

thread = threading.Thread(target=run_app)
thread.start()

import sqlite3
import pandas as pd

DB_PATH = "/content/users.db"

# Connect to the database
conn = sqlite3.connect(DB_PATH)

# Query all users
df = pd.read_sql_query("SELECT * FROM users", conn)

# Display the table
df