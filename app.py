from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

# Dummy contact list
contacts = []

@app.route('/')
def home():
    city_filter = request.args.get('city')
    if city_filter:
        filtered_contacts = [c for c in contacts if c['city'].lower() == city_filter.lower()]
    else:
        filtered_contacts = contacts

    cities = sorted(set(c['city'] for c in contacts))
    return render_template('home.html', contacts=filtered_contacts, cities=cities, selected_city=city_filter)

@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    city = request.form['city']
    
    contact = {
        'id': str(uuid.uuid4()),
        'name': name,
        'email': email,
        'phone': phone,
        'city': city
    }
    contacts.append(contact)
    return redirect(url_for('home'))

@app.route('/contact/<contact_id>')
def contact_detail(contact_id):
    contact = next((c for c in contacts if c['id'] == contact_id), None)
    if not contact:
        return "Contact not found", 404
    return render_template('contact_detail.html', contact=contact)

if __name__ == '__main__':
    app.run(debug=True)
