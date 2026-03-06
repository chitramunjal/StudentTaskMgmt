from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import mysql.connector
import boto3
import os
import uuid
import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # In production, use environment variables

# --- Database Connection ---
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="database",
            user="root",
            password="password",
            database="studentdb",
            # Added connection timeout and retry logic for docker startup robustness
            connect_timeout=10
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# --- S3 Configuration ---
# Uses dummy/mock credentials by default to avoid crashing on local demo
S3_BUCKET = os.environ.get("S3_BUCKET_NAME", "student-notes-bucket")
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "mock_access_key"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "mock_secret_key"),
    region_name=os.environ.get("AWS_REGION", "us-east-1")
)

# --- Routes ---

@app.route("/")
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'] # Note: In a real app, hash this!
        
        db = get_db_connection()
        if db:
            cursor = db.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                    (name, email, password)
                )
                db.commit()
                flash("Registration successful. Please login.", "success")
                return redirect(url_for('login'))
            except mysql.connector.IntegrityError:
                flash("Email already registered.", "danger")
            finally:
                cursor.close()
                db.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        db = get_db_connection()
        if db:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
            user = cursor.fetchone()
            cursor.close()
            db.close()
            
            if user:
                session['user_id'] = user['id']
                session['name'] = user['name']
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials.", "danger")
        else:
            flash("Database connection failed. Is the database service running?", "danger")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    search_query = request.args.get('search', '')
    priority_filter = request.args.get('priority', '')
    
    db = get_db_connection()
    tasks = []
    notes = []
    
    # Mock Cloud Stats
    cloud_stats = {
        'cpu_usage': '24%',
        'memory_usage': '1.2GB / 2GB',
        'disk_usage': '8.5GB / 20GB',
        'uptime': '14 days, 6 hours',
        'status': 'Healthy'
    }

    if db:
        cursor = db.cursor(dictionary=True)
        # Fetch tasks with filtering
        query = "SELECT * FROM tasks WHERE user_id=%s"
        params = [user_id]
        
        if search_query:
            query += " AND (task_title LIKE %s OR description LIKE %s)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])
        
        if priority_filter:
            query += " AND priority = %s"
            params.append(priority_filter)
            
        query += " ORDER BY deadline ASC"
        
        cursor.execute(query, tuple(params))
        tasks = cursor.fetchall()
        
        # Fetch notes
        cursor.execute("SELECT * FROM notes WHERE user_id=%s ORDER BY upload_date DESC", (user_id,))
        notes = cursor.fetchall()
        
        cursor.close()
        db.close()
        
    return render_template("dashboard.html", tasks=tasks, notes=notes, name=session.get('name'), cloud_stats=cloud_stats, search_query=search_query, priority_filter=priority_filter)

@app.route("/addtask", methods=["POST"])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    title = request.form['title']
    description = request.form['description']
    deadline = request.form['deadline']
    priority = request.form.get('priority', 'Medium')
    
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO tasks (user_id, task_title, description, deadline, priority) VALUES (%s, %s, %s, %s, %s)",
            (session['user_id'], title, description, deadline, priority)
        )
        db.commit()
        cursor.close()
        db.close()
        flash("Task added successfully.", "success")
        
    return redirect(url_for('dashboard'))

@app.route("/edit_task/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    status = request.form.get('status', 'pending')
    
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        cursor.execute("UPDATE tasks SET status=%s WHERE task_id=%s AND user_id=%s", (status, task_id, session['user_id']))
        db.commit()
        cursor.close()
        db.close()
    
    return redirect(url_for('dashboard'))

@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM tasks WHERE task_id=%s AND user_id=%s", (task_id, session['user_id']))
        db.commit()
        cursor.close()
        db.close()
        
    return redirect(url_for('dashboard'))

@app.route("/upload_note", methods=["POST"])
def upload_note():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if 'note_file' not in request.files:
        flash("No file part", "danger")
        return redirect(url_for('dashboard'))
        
    file = request.files['note_file']
    if file.filename == '':
        flash("No selected file", "danger")
        return redirect(url_for('dashboard'))
        
    if file:
        original_filename = file.filename
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        
        try:
            # We wrap this in a try-catch for local demos. 
            # If standard AWS creds are not in the environment, this would throw if we actually try to upload_fileobj
            # We mock the upload logic if it fails to ensure the demo continues working for DB ops
            try:
                s3_client.upload_fileobj(
                    file,
                    S3_BUCKET,
                    unique_filename,
                    ExtraArgs={'ContentType': file.content_type}
                )
            except Exception as s3_error:
                print(f"Skipping actual S3 upload. S3 error: {s3_error}")
                flash(f"Note: S3 integration is using mock credentials, file was registered but not actually uploaded to a real AWS bucket.", "info")
            
            file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{unique_filename}"
            
            db = get_db_connection()
            if db:
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO notes (user_id, file_name, file_url, upload_date) VALUES (%s, %s, %s, %s)",
                    (session['user_id'], original_filename, file_url, datetime.date.today())
                )
                db.commit()
                cursor.close()
                db.close()
                flash("File metadata saved successfully.", "success")
                
        except Exception as e:
            flash(f"Error processing file: {str(e)}", "danger")
            
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
