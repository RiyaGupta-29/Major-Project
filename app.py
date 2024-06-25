from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_mail import Mail, Message
import os
import videoTester
from flask_bootstrap import Bootstrap
import mysql.connector
from mysql.connector import errorcode
import pyaudio
import wave
import voiceAnalyzer
import random
from string import ascii_uppercase
import time 

app = Flask(__name__)
app.secret_key = os.urandom(24)
mail = Mail(app) 
Bootstrap(app)
socketio = SocketIO(app)
messages = []

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

def read_db_credentials(file_path):
    credentials = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    credentials[key.strip()] = value.strip()
                else:
                    print(f"Error: Invalid format in line: {line}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"Error: {e}")
    return credentials

# Establish connection
credentials = read_db_credentials('connection_details.txt')
connection = mysql.connector.connect(
    host=credentials.get('host'),
    user=credentials.get('user'),
    password=credentials.get('password'),
    database=credentials.get('database')
)

@app.route('/',methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            cursor = connection.cursor(dictionary=True)
            try:
                query = "SELECT * FROM users WHERE email = %s AND password = %s"
                values = (email, password)
                cursor.execute(query, values)
                user = cursor.fetchone() 
                
                if user:
                    session['loggedin'] = True
                    session['id'] = user['id']
                    session['email'] = user['email']
                    return redirect(url_for('index'))
                else:
                    error = 'Invalid email or password. Please try again.'
                    return render_template('login.html', error=error)
            finally:
                cursor.close()
        
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            re_password = request.form['repassword']

            if password == re_password:
                # Connect to the database
                cursor = connection.cursor()
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                values = (name, email, password)
                cursor.execute(query, values)

                # Commit the changes and close the connection
                connection.commit()
                cursor.close()

                return render_template('signup.html', data="Saved successfully. Now login")

            else:
                error = 'Password and re-password do not match. Please try again.'
                return render_template('signup.html', error=error)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            # Handle the duplicate entry error (account already exists)
            flash('Account already exists.', 'error')
        else:
            # Handle other database errors
            flash('Database error occurred.', 'error')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect to the homepage or login page
    return redirect(url_for('login'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = connection.cursor(dictionary=True)
        user_id = session.get('id')  # Use .get() method to avoid KeyError
        if user_id is None:
            return redirect(url_for('login'))
        cursor.execute('SELECT name,email FROM users WHERE id = %s', (user_id,))
        account = cursor.fetchone()
        name = account['name']
        email=account['email']
        return render_template('profile.html',name=name,email=email)

@app.route('/thoughts')
def thoughts():
    return render_template('thoughts.html')

@app.route('/puzzle')
def puzzle():
    return render_template('puzzle.html')


@app.route('/qstn')
def phq():
    return render_template("phq9.html",data="Anxiety and Depression Detection")

@app.route('/expression') 
def expression():
    if 'loggedin' in session:
        
        p=videoTester.exp()
        cursor = connection.cursor()
        user_id = session.get('id')
        cursor.execute("INSERT INTO candidate_results (user_id, result_face) VALUES (%s,%s)", (user_id,p))
        connection.commit()
        cursor.close()
        return render_template("face.html",data=p)

@app.route('/face') 
def face():
    return render_template("face.html",data = "Anxiety and Depression Detection")

@app.route('/voice')
def voice():
    return render_template("voice.html",data = "Click on the Mic to Record")


@app.route('/voice_recording')
def voice_recording():
    CHUNK = 1024 
    FORMAT = pyaudio.paInt16 #paInt8
    CHANNELS = 2 
    RATE = 44100 #sample rate
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output10.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK) #buffer

    #return render_template("voice.html", data = "Recording ....")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data) # 2 bytes(16 bits) per channel

    

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return render_template("voice.html", data = "Done recording.")

@app.route('/voice_analyzer')
def voice_analyzeer():
    if 'loggedin' in session:
        res = voiceAnalyzer.alalyzer()
        res2 = os.system('python test.py -f output10.wav > output.txt')
        file =  open("output.txt","r")
        #gender = ["male","female"]
        for line in file:
            if "Result:" in line:
                sound = line.split()
                res2 = sound[1]
        cursor = connection.cursor()
        user_id = session.get('id')
        cursor.execute("UPDATE candidate_results SET result_voice=%s WHERE user_id=%s", (res,user_id))
        connection.commit()
        cursor.close()
        return render_template("voice.html",data = res)

@app.route('/info', methods=["POST", "GET"])
def info():
    # Check if the user is logged in
    if 'loggedin' in session:
        cursor = connection.cursor(dictionary=True)
        try:
            user_id = session.get('id')  # Use .get() method to avoid KeyError
            if user_id is None:
                return redirect(url_for('login'))

            cursor.execute('SELECT name FROM users WHERE id = %s', (user_id,))
            account = cursor.fetchone()

            if account:
                name = account['name']
                if request.method == "POST":
                    code = request.form.get("code")
                    join = request.form.get("join", False)
                    create = request.form.get("create", False)

                    if join != False and not code:
                        return render_template("base.html", error="Please enter a room code.", code=code, name=name)
                    
                    room = code
                    if create != False:
                            room = generate_unique_code(4)
                            rooms[room] = {"members": 0, "messages": []}
                    elif code not in rooms:
                        return render_template("base.html", error="Room does not exist.", code=code, name=name)

                    session["room"] = room
                    session["name"] = name
                    return redirect(url_for("room"))
            
            return render_template('base.html', name=name)
        finally:
            cursor.close()

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("/index"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])
    
@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

    if rooms[room]["members"] == 2:
        socketio.emit("startTimer", to=room)

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

@app.route('/payment')
def payment():
    return render_template('payment.html') 

@app.route('/index2')
def index2():
    return render_template('index2.html') 

@app.route('/asanas')
def asanas():
    return render_template('Asanas.html') 

@app.route('/mood-ease-hub')
def mood_ease_hub():
    return render_template('index1.html') 

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/end')
def process_scores():
    if 'loggedin' in session:
        depression_score = request.args.get('depressionScore')
        anxiety_score = request.args.get('AnxietyScore')
        stress_score = request.args.get('StressScore')

        cursor = connection.cursor()
        user_id = session.get('id') 
        cursor.execute("""
            UPDATE candidate_results
            SET dass_depressionscore = %s,
                dass_anxietyscore = %s,
                dass_stressscore = %s
            WHERE user_id = %s
        """, (depression_score, anxiety_score, stress_score, user_id))

        connection.commit()
        cursor.close()
        return render_template('end.html', depression_score=depression_score, anxiety_score=anxiety_score, stress_score=stress_score)

@app.route('/mood-check-hub')
def mood_check_hub():
    return render_template('K10_edit.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        msg = Message(subject=subject,
                      sender=email,
                      recipients=['riya20csu269@ncuindia.edu'])  # Replace with the recipient email
        msg.body = f"From: {name}\nEmail: {email}\n\n{message}"

        try:
            mail.send(msg)
            flash('Email sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send email. Error: {str(e)}', 'danger')
        
        return redirect(url_for('index'))
    return 'Form submission error', 400

@app.route('/friend')
def friend():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    cursor.execute("SELECT user_id FROM friend_requests")
    friend_requests_data = cursor.fetchall()
    friend_requests = [req['user_id'] for req in friend_requests_data]
    
    return render_template('friend.html', users=users, friend_requests=friend_requests)

@app.route('/send_friend_request', methods=['POST'])
def send_friend_request():
    user_id = int(request.form['user_id'])
    cursor = connection.cursor()
    cursor.execute("INSERT INTO friend_requests (user_id) VALUES (%s)", (user_id,))
    connection.commit()
    return jsonify({"status": "success", "user_id": user_id})

if __name__ == '__main__':
    app.run(debug=True)
