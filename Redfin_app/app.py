from scraper import get_data,update_dat
from refre import refresh
from flask import Flask, render_template, request,jsonify,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
import threading
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scraped_data.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)  # Add this line

    scraped_data = db.relationship('ScrapedData', backref='location', lazy=True)

class ScrapedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_on_redfin = db.Column(db.String(255))
    property_type = db.Column(db.String(255))
    year_built = db.Column(db.String(255))
    style = db.Column(db.String(255))
    community = db.Column(db.String(255))
    lot_size = db.Column(db.String(255))
    street_address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(255))
    price = db.Column(db.String(255))
    offer_price = db.Column(db.String(255))
    beds = db.Column(db.String(255))
    baths = db.Column(db.String(255))
    size = db.Column(db.String(255))
    agent_name = db.Column(db.String(255))
    agent_last_name=db.Column(db.String(255))
    agent_phone = db.Column(db.String(255))
    agent_email = db.Column(db.String(255))

    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

@app.route('/')
def index():
    locations = Location.query.all()  # Assuming Location is the model for locations
    return render_template('index.html', locations=locations)
update_lock = threading.Lock()
updating_data = False

@app.route('/add_data', methods=['POST'])
def add_data():
    global updating_data
    with update_lock:
        updating_data = True
        location_name = request.form.get('location')
        print("Adding data for location:", location_name)  # Add this line
        scraped_data_list=get_data(location_name)
        data_from_update = update_dat(location_name)
        for item in data_from_update:
            if item not in scraped_data_list:
                scraped_data_list.append(item)
        for scraped_data in scraped_data_list:
            if location_name:
                existing_location = Location.query.filter_by(name=location_name).first()

                if not existing_location:
                    print("Creating new location:", location_name)  # Add this line
                    new_location = Location(name=location_name)
                    db.session.add(new_location)
                    db.session.commit()
                    existing_location = new_location
                
                scraped_data_instance = ScrapedData(
                        time_on_redfin=str(scraped_data.get('time_on_redfin')),
                        property_type=str(scraped_data.get('property_type')),
                        year_built=str(scraped_data.get('year_built')),
                        style=str(scraped_data.get('style')),
                        community=str(scraped_data.get('community')),
                        lot_size=str(scraped_data.get('lot_size')),
                        street_address=str(scraped_data.get('street_address')),
                        city=str(scraped_data.get('city')),
                        state=str(scraped_data.get('state')),
                        zip_code=str(scraped_data.get('zip_code')),
                        price=str(scraped_data.get('price')),
                        offer_price=str(scraped_data.get('offer price')),
                        beds=str(scraped_data.get('beds')),
                        baths=str(scraped_data.get('baths')),
                        size=str(scraped_data.get('size')),
                        agent_name=str(scraped_data.get('agent_name')),
                        agent_last_name=str(scraped_data.get('agent_last_name')),
                        agent_phone=str(scraped_data.get('agent_phone')),
                        agent_email=str(scraped_data.get('agent_email')),
                        location_id=existing_location.id
                    )
                db.session.add(scraped_data_instance)
                db.session.commit()
            updating_data = False
    refresh()
    return redirect(url_for('index'))
@app.route('/delete_location/<int:location_id>', methods=['POST'])
def delete_location(location_id):
    location = Location.query.get(location_id)
    if location:
        for scraped_data in location.scraped_data:
            db.session.delete(scraped_data)

        db.session.delete(location)
        db.session.commit()
        refresh()
    return redirect(url_for('index'))

@app.route('/delete_scraped_data/<int:scraped_data_id>', methods=['POST'])
def delete_scraped_data(scraped_data_id):
    scraped_data = ScrapedData.query.get(scraped_data_id)
    if scraped_data:
        db.session.delete(scraped_data)
        db.session.commit()
        refresh()
    return redirect(url_for('index'))
scheduler = BackgroundScheduler()
scheduler.start()
def update_data_job():
    global updating_data
    
    with app.app_context():
        if not updating_data:
            locations = Location.query.all()
            for location in locations:
                location_name = location.name
                print("Updating data for location:", location_name)
                scraped_data_list = update_dat(location_name)
                existing_location = Location.query.filter_by(name=location_name).first()

                if not existing_location:
                    print("Creating new location:", location_name)
                    new_location = Location(name=location_name)
                    db.session.add(new_location)
                    db.session.commit()
                    existing_location = new_location
            
                for scraped_data in scraped_data_list:
                    street_address = scraped_data.get('street_address')
                    existing_scraped_data = ScrapedData.query.filter_by(street_address=street_address).first()

                    if not existing_scraped_data:
                        print("Creating new scraped data for street address:", street_address)
                        scraped_data_instance = ScrapedData(
                                time_on_redfin=str(scraped_data.get('time_on_redfin')),
                                property_type=str(scraped_data.get('property_type')),
                                year_built=str(scraped_data.get('year_built')),
                                style=str(scraped_data.get('style')),
                                community=str(scraped_data.get('community')),
                                lot_size=str(scraped_data.get('lot_size')),
                                street_address=str(scraped_data.get('street_address')),
                                city=str(scraped_data.get('city')),
                                state=str(scraped_data.get('state')),
                                zip_code=str(scraped_data.get('zip_code')),
                                price=str(scraped_data.get('price')),
                                offer_price=str(scraped_data.get('offer price')),
                                beds=str(scraped_data.get('beds')),
                                baths=str(scraped_data.get('baths')),
                                size=str(scraped_data.get('size')),
                                agent_name=str(scraped_data.get('agent_name')),
                                agent_last_name=str(scraped_data.get('agent_last_name')),
                                agent_phone=str(scraped_data.get('agent_phone')),
                                agent_email=str(scraped_data.get('agent_email')),
                                location_id=existing_location.id
                            )
                        db.session.add(scraped_data_instance)
                        db.session.commit()
            refresh()
        else:
            print("add_data runing,update_data_job will run later")        
scheduler.add_job(update_data_job, 'interval', hours=24, next_run_time=datetime.now() + timedelta(hours=24))
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)