from flask import render_template
from app import app

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_views/dashboard.html")

@app.route("/admin/profile")
def admin_profile():
    return "Admin profile"