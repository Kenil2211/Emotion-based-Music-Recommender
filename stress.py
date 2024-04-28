import pymongo
import datetime
import matplotlib.pyplot as plt

def plot_emotions_by_time(userid, date):
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client.club5
    collection = db.emotions

    # Define numerical values for emotions
    emotion_values = {"Angry": 6, "Disgusted": 4, "Fearful": 7, "Happy": 3, "Neutral": 4, "Sad": 5, "Surprised": 4}

    # Query emotions for the given date
    start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = date.replace(hour=23, minute=59, second=59, microsecond=999999)
    query = {"userid": userid, "date_time": {"$gte": start_date, "$lte": end_date}}
    emotions_cursor = collection.find(query)

    # Prepare data for plotting
    emotions_by_time = {}
    for entry in emotions_cursor:
        time = entry["date_time"].time().strftime("%H:%M:%S")  # Convert time to string
        emotion = entry["emotion"]
        emotion_value = emotion_values[emotion]  # Get numerical value for the emotion
        if time not in emotions_by_time:
            emotions_by_time[time] = {emotion_value: 1}
        else:
            if emotion_value in emotions_by_time[time]:
                emotions_by_time[time][emotion_value] += 1
            else:
                emotions_by_time[time][emotion_value] = 1

    # Plot the graph
    if emotions_by_time:
        plt.figure(figsize=(10, 6))
        for time, emotions in sorted(emotions_by_time.items()):
            plt.plot([time] * len(emotions), list(emotions.keys()), 'ro')
        plt.xlabel('Time')
        plt.ylabel('Emotion (Numeric Value)')
        plt.title('Emotions Captured on {}'.format(date.strftime('%Y-%m-%d')))
        plt.grid(True)
        plt.xticks(rotation=90)  # Rotate x-ticks vertically
        plt.tight_layout()  # Adjust layout to make room for the rotated x-tick labels
        plt.show()
    else:
        print("No emotions captured on {}".format(date.strftime('%Y-%m-%d')))

# Example usage
date_to_plot = datetime.datetime(2024, 3, 15)
plot_emotions_by_time("65f201b71cdf9ff02b126ef1", date_to_plot)
