from flask import Flask, render_template, request, jsonify
from supabase import create_client
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

AUTO_FIELDS = ['id', 'created_at']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    try:
        response = supabase.table("cad").select("*").order("id", desc=False).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        response = supabase.table("cad").insert(data).execute()
        return jsonify({"success": True, "data": response.data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
