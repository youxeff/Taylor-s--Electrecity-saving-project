import os
from flask import Flask, render_template, request, redirect, Response
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import csv
from google.cloud.firestore_v1 import Query


app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))

json_file_path = os.path.join(base_dir, 'License', 'rptu-d4ff1-firebase-adminsdk-ssssf-38d8d0cfdc.json')

cred = credentials.Certificate(json_file_path)
firebase_admin.initialize_app(cred)

db = firestore.client()


@app.route('/')
def index():
    error = request.args.get('error')
    return render_template('index.html', error=error)


@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    if username == '1@admin' and password == 'admin2023':
        
        return redirect('/dashboard?username=' + username)
    else:
        error = 'Invalid username and/or password'
        return redirect('/?error=' + error)


@app.route('/searchbar', methods=['GET'])
def search():
    search_term = request.args.get('q')

    if not search_term:
        return redirect('/?error=Invalid search term')

    # Perform a search query
    users_ref = db.collection('users', 'billing', 'users')
    query = users_ref.where('name', '>=', search_term).where('name', '<=', search_term + u'\uf8ff')
    results = query.stream()

    # Prepare the search results
    search_results = []
    for result in results:
        search_results.append(result.to_dict())

    return render_template('searchbar.html', search_results=search_results, search_term=search_term)

@app.route('/dashboard')
def dashboard():
    # Retrieve the username from the query parameter
    username = request.args.get('username')
    if username:
        username = username.capitalize()  # Capitalize the first letter of the username

    # Fetch the total number of users from Firestore
    users_ref = db.collection('users')
    total_users = users_ref.get()
    total_users_count = len(total_users)
    billing_ref = db.collection('billing')
    total_billing = billing_ref.get()
    total_billing_count = len(total_billing)
    # Pass the username and total_users_count to the template
    return render_template('dashboard.html', total_users_count=total_users_count, total_billing_count=total_billing_count)


@app.route('/userlist')
def userlist():
    # Retrieve the username from the query parameter
    username = request.args.get('username')
    if username:
        username = username.capitalize()  # Capitalize the first letter of the username

    # Fetch the user data from Firestore
    users_ref = db.collection('users')
    user_data = users_ref.get()
    users = []
    for user in user_data:
        user_dict = user.to_dict()
        if all(field in user_dict for field in ['active', 'address', 'email', 'fullName', 'id', 'phoneNumber']):
            users.append(user_dict)

    return render_template('userlist.html', users=users)

@app.route('/export_users', methods=['GET'])
def export_users():
     # Fetch the user data from Firestore
        users_ref = db.collection('users')
        user_data = users_ref.get()
        users = []
        for user in user_data:
            user_dict = user.to_dict()
            if all(field in user_dict for field in ['active', 'address', 'email', 'fullName', 'id', 'phoneNumber']):
                users.append(user_dict)

        # Create a CSV string from the user data
        csv_data = ""
        if users:
            keys = users[0].keys()
            csv_data += ','.join(keys) + '\n'
            for user in users:
                row = [str(user[key]).replace(',', '') for key in keys]
                csv_data += ','.join(row) + '\n'

        # Set the appropriate headers for the CSV file download
        headers = {
            "Content-Disposition": "attachment; filename=userlist.csv",
            "Content-Type": "text/csv",
            "Active": "active",
            "Address": "address",
            "Email": "email",
            "Full name ": "fullName",
            "ID": "id",
            "Phone No.": "Phone Number",
         }



        # Create a response object with the CSV data and headers
        response = Response(csv_data, headers=headers)
        return response



@app.route('/billinglist')
def billinglist():
    page_size = int(request.args.get('page_size', 6))
    start_after = request.args.get('start_after')

    billing_ref = db.collection('billing')

    query = billing_ref.order_by('id')

    if start_after:
        start_after_doc = billing_ref.document(start_after).get()
        start_after_snapshot = billing_ref.order_by('id').start_after(start_after_doc).limit(1).get()
        start_after_snapshot = start_after_snapshot[0] if start_after_snapshot else None

        if start_after_snapshot:
            query = query.start_after(start_after_snapshot)

    billing_data = query.limit(page_size).get()
    billing_list = [bill.to_dict() for bill in billing_data]

    last_doc = billing_data[-1] if billing_data else None
    last_doc_id = last_doc.get('id') if last_doc else None

    has_previous_page = start_after is not None
    has_next_page = last_doc is not None

    return render_template(
        'billing.html',
        bills=billing_list,
        page_size=page_size,
        start_after=last_doc_id,
        has_previous_page=has_previous_page,
        has_next_page=has_next_page
    )


@app.route('/export_data', methods=['GET'])
def export_data():
    option = request.args.get('option')

    if option == 'userlist':
        # Fetch the user data from Firestore
        users_ref = db.collection('users')
        user_data = users_ref.get()
        users = []
        for user in user_data:
            user_dict = user.to_dict()
            if all(field in user_dict for field in ['active', 'address', 'email', 'fullName', 'id', 'phoneNumber']):
                users.append(user_dict)

        # Create a CSV string from the user data
        csv_data = ""
        if users:
            keys = users[0].keys()
            csv_data += ','.join(keys) + '\n'
            for user in users:
                row = [str(user[key]).replace(',', '') for key in keys]
                csv_data += ','.join(row) + '\n'

        # Set the appropriate headers for the CSV file download
        headers = {
            "Content-Disposition": "attachment; filename=userlist.csv",
            "Content-Type": "text/csv",
        }

        # Create a response object with the CSV data and headers
        response = Response(csv_data, headers=headers)
        return response

    elif option == 'billinglist':
        # Fetch the billing data from Firestore
        billing_ref = db.collection('billing')
        billing_data = billing_ref.get()
        billing_list = [bill.to_dict() for bill in billing_data]

        # Create a CSV string from the billing data
        csv_data = ""
        if billing_list:
            keys = billing_list[0].keys()
            csv_data += ','.join(keys) + '\n'
            for bill in billing_list:
                row = [str(bill[key]).replace(',', '') for key in keys]
                csv_data += ','.join(row) + '\n'

        # Set the appropriate headers for the CSV file download
        headers = {
            "Content-Disposition": "attachment; filename=billinglist.csv",
            "Content-Type": "text/csv",
        }

        # Create a response object with the CSV data and headers
        response = Response(csv_data, headers=headers)
        return response

    else:
        error = 'Invalid option'
        return redirect('/?error=' + error)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
