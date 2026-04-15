import os
import subprocess

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
APP_DIR = os.path.join(ROOT_DIR, "FlaskDashboard")

os.chdir(APP_DIR)
subprocess.run(["python", "app.py"], check=True)
