import os

import sqlalchemy as db
from flask import Flask
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    engine = db.create_engine("postgresql://" + os.environ.get('AWS_POSTGRES_URL'))
    df = pd.read_sql_query('SELECT * FROM apps_by_matthew.applications', con=engine)
    return df.to_json()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)