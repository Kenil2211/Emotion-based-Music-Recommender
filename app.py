from flask import Flask, render_template, Response, jsonify, request
from pymongo import MongoClient
import io
import datetime
import gunicorn
from camera import *
from stress_graph import *

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client.club5
emotions_collection = db.emotions
users_collection = db.currentmusicusers

headings = ("Name","Album","Artist","url")
df1 = music_rec()
df1 = df1.head(15)
@app.route('/')
def index():
    print(df1.to_json(orient='records'))
    return render_template('index.html', headings=headings, data=df1)

def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    userid = request.args.get('userid')
    print('userrrrrr',userid)
    return Response(gen(VideoCamera(userid)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')

@app.route('/music/c/user', methods=['GET'])
def get_user():
    # Query the database to get user data
    user_data = users_collection.find_one({}, {'_id': 0, 'firstname': 1})

    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/plot/emotions', methods=['POST'])
def plot_emotions():
    
    # date = request.args.get('date')
    data = request.get_json()
    
    # Access the date from the JSON data
    date = data.get('date', None)
    userid = data.get('userid',None)
    print('apiiiiiiii',date,userid)
    # Assuming plot_emotions_by_time function takes a list of emotions and timestamps and returns a matplotlib figure
    fig = plot_emotions_by_time(userid,date)
    
    # Convert figure to PNG image and send it
    output = io.BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)
        
    return Response(output.getvalue(), mimetype='image/png')



if __name__ == '__main__':
    app.debug = True
    app.run()
