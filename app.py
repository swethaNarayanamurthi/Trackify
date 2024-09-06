from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from twilio.rest import Client

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    name = request.form['name']
    destination = request.form['destination']
    phone_number = request.form['phone_number']

    # Convert destination to latitude and longitude
    geolocator = Nominatim(user_agent="track_app")
    location = geolocator.geocode(destination)
    destination_coordinates = (location.latitude, location.longitude)
    print(destination_coordinates)

    # Current location (Assuming for example)
    current_coordinates = (11.74269375, 79.75030644171935)  # Latitude and Longitude of New York City

    # Calculate distance
    distance = geodesic(current_coordinates, destination_coordinates).kilometers

    # Check if the destination is matched or not
    if distance < 1:  # Assuming within 1 kilometer is considered matched
        messages="Destination matched "
        account_sid='AC80150745059978094571827aace4823b'
        auth_token='a2ae7d69f1970f17c3da46a10bd1db67'
        client=Client(account_sid,auth_token)

        call=client.calls.create(twiml='<Response><Say>Your Destination has been reached please Be Prepared</Say></Response>',
                         to='+918825881457',
                         from_='+15128656397'
                         )
        print(call.sid)
        message_body = 'Your Destination has been reached please Be Prepared'
        from_phone_number='+15128656397'
        to_phone_number='+918825881457'

        try:
    # Send the message
            message = client.messages.create(
            body=message_body,
            from_=from_phone_number,
            to=to_phone_number
            )
            print(f'Message sent successfully! SID: {message.sid}')
        except Exception as e:
            print(f'Failed to send message: {str(e)}')

    else:
        messages = "Destination not matched."

    return render_template('result.html', name=name, destination=destination, phone_number=phone_number, message=messages)

if __name__ == '__main__':
    app.run(debug=True)
