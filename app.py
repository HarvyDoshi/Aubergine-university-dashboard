
import time
import requests
import json
import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func  # Added for counting/grouping

app = Flask(__name__)

# --- CONFIGURATION ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'university.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    country = db.Column(db.String, index=True)
    state_province = db.Column(db.String)
    domains = db.Column(db.JSON)
    web_pages = db.Column(db.JSON)

# Create tables on startup
with app.app_context():
    db.create_all()

UPDATE_WAIT_TIME = 86400
last_updated = 0

# --- DATA INGESTION ---
def ingest_data_to_db():
    global last_updated
    url = "https://raw.githubusercontent.com/Hipo/university-domains-list/master/world_universities_and_domains.json"
    
    try:
        response = requests.get(url)
        data = response.json()
        db.session.query(University).delete()
        
        universities = []
        for item in data:
            uni = University(
                name=item.get('name'),
                country=item.get('country'),
                state_province=item.get('state-province'),
                domains=item.get('domains', []),
                web_pages=item.get('web_pages', [])
            )
            universities.append(uni)
        
        db.session.add_all(universities)
        db.session.commit()
        last_updated = time.time()
        return True
    except Exception as e:
        print(f"Error ingesting data: {e}")
        db.session.rollback()
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    if University.query.count() == 0:
        ingest_data_to_db()

    country = request.args.get('country')
    state_province = request.args.get('state-province')
    name = request.args.get('name')
    limit = request.args.get('limit', 100, type=int)

    query = University.query

    if country:
        query = query.filter(University.country.ilike(f'{country}'))
    if state_province:
        query = query.filter(University.state_province.ilike(f'{state_province}'))
    if name:
        query = query.filter(University.name.ilike(f'%{name}%'))

    results = query.limit(limit).all()

    return jsonify([{
        'name': u.name,
        'country': u.country,
        'state-province': u.state_province,
        'web_pages': u.web_pages
    } for u in results])

@app.route("/provinces")
def provinces():
    country = request.args.get('country')
    if not country: return jsonify([])

    results = db.session.query(University.state_province).filter(
        University.country.ilike(country),
        University.state_province.isnot(None)
    ).distinct().order_by(University.state_province).all()

    return jsonify([r[0] for r in results])

# --- NEW STATS ENDPOINT ---
@app.route("/stats")
def stats():
    if University.query.count() == 0:
        ingest_data_to_db()

    # Total Universities
    total_unis = University.query.count()
    
    # Total Countries (Distinct)
    total_countries = db.session.query(University.country).distinct().count()

    # Top 5 Countries by number of universities
    top_countries_query = db.session.query(
        University.country, 
        func.count(University.id).label('count')
    ).group_by(University.country).order_by(func.count(University.id).desc()).limit(5).all()

    return jsonify({
        'total_universities': total_unis,
        'total_countries': total_countries,
        'top_countries': [{'country': c, 'count': n} for c, n in top_countries_query]
    })

@app.route('/update')
def update():
    if (time.time() >= last_updated + UPDATE_WAIT_TIME):
        if ingest_data_to_db(): return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})

if __name__ == "__main__":
    app.run(debug=True, port=9090)