from extensions import db, migrate
from flask import Flask, render_template
import os
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hospital.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hospital-management-secret-key'

db.init_app(app)
migrate.init_app(app, db)

# Import models to ensure they are registered with SQLAlchemy
from models import Patient, Doctor, Appointment

@app.route('/')
def index():
    patient_count = Patient.query.count()
    doctor_count = Doctor.query.count()
    appointment_count = Appointment.query.count()
    recent_appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).limit(5).all()
    return render_template('index.html', 
                         patient_count=patient_count, 
                         doctor_count=doctor_count, 
                         appointment_count=appointment_count,
                         recent_appointments=recent_appointments)

@app.route('/patients')
def patients():
    all_patients = Patient.query.all()
    return render_template('patients.html', patients=all_patients)

@app.route('/doctors')
def doctors():
    all_doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=all_doctors)

@app.route('/appointments')
def appointments():
    all_appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=all_appointments)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Seed initial data if empty
        if Doctor.query.count() == 0:
            doc1 = Doctor(name="Dr. Sarah Smith", specialty="Cardiology", email="sarah.smith@medi.com")
            doc2 = Doctor(name="Dr. James Wilson", specialty="Neurology", email="j.wilson@medi.com")
            doc3 = Doctor(name="Dr. Emily Chen", specialty="Pediatrics", email="e.chen@medi.com")
            db.session.add_all([doc1, doc2, doc3])
            
            p1 = Patient(name="John Doe", email="john@example.com", phone="123-456-7890")
            p2 = Patient(name="Jane Miller", email="jane@example.com", phone="098-765-4321")
            db.session.add_all([p1, p2])
            db.session.commit()
            
            a1 = Appointment(patient_id=p1.id, doctor_id=doc1.id, appointment_date=datetime.now(), reason="Heart checkup", status="Scheduled")
            a2 = Appointment(patient_id=p2.id, doctor_id=doc2.id, appointment_date=datetime.now(), reason="Headache", status="Completed")
            db.session.add_all([a1, a2])
            db.session.commit()
            print("Seeded database with sample data.")
            
    app.run(debug=True)
