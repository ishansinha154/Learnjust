[4:30 PM] Siddhanth Mutha
from flask import Flask, request, render_template, make_response, jsonify

from flask_cors import CORS

from flask_mysqldb import MySQL

import MySQLdb.cursors

from datetime import datetime

import bcrypt

import logging

import uuid

import os
 
app = Flask(__name__)

CORS(app)
 
# Initialize MySQL

app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = 'Parkar@123'

app.config['MYSQL_DB'] = 'login'

app.config['MYSQL_PORT'] =   3306

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Set the cursor class to DictCursor
 
mysql = MySQL(app)
 
@app.route('/add_listing', methods=['GET', 'POST'])

def add_listing():

    if request.method == 'POST':

        # Get form data using request.form.get()

        prop_name = request.form.get('property_name', '')

        prop_loc = request.form.get('property_location', '')

        prop_size = int(request.form.get('property_size',   0))

        prop_amen = request.form.get('property_amentities', '')

        prop_stat = request.form.get('property_status', '')

        image = request.files.get('image')
 
        # Check if image was uploaded

        if image:

            # Generate unique filename for the image

            filename = str(uuid.uuid4()) + '_' + image.filename

            image_path = os.path.join('static/images', filename)

            image.save(image_path)

        else:

            image_path = ''
 
        # Convert prop_stat to the appropriate enum value

        prop_stat = 'for_rent' if prop_stat == 'rent' else ('for_sale' if prop_stat == 'sell' else 'both')
 
        # Connect to the database

        conn = mysql.connection

        cursor = conn.cursor()
 
        # Insert property listing into the database

        query = """

            INSERT INTO property (prop_name, prop_loc, prop_size, prop_amen, prop_stat, image_path, user_id, flag)

            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

        """

        cursor.execute(query, (prop_name, prop_loc, prop_size, prop_amen, prop_stat, image_path, int(request.form.get('user_id',   0)),   0))

        conn.commit()
 
        # Close the cursor and connection

        cursor.close()

        conn.close()
 
        return make_response(jsonify({'message': 'Listing added successfully!'}),   200)
 
    return render_template('add_listing.html')
 
if __name__ == '__main__':

    app.run(debug=True)