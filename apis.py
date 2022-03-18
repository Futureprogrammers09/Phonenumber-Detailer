from flask import Flask , jsonify , render_template
import phonenumbers
from phonenumbers import carrier , timezone , geocoder
import json


app = Flask(__name__ , template_folder='template')

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/apis/<string:n>")
def send(n):
    value= n

    #Getting the contry code ==============
    pepnumber = phonenumbers.parse(value)
    location = geocoder.description_for_number(pepnumber , "en")

    #Getting the Service Provider ===========
    service_pro = carrier.name_for_number(pepnumber , "en")
    is_valid = phonenumbers.is_valid_number(pepnumber)
    name_user = carrier.safe_display_name(pepnumber , "en")
    timeZone = timezone.time_zones_for_number(pepnumber)
    code = phonenumbers.can_be_internationally_dialled(pepnumber)
    
    token = phonenumbers.country_mobile_token(location)

    json_num = json.dumps(pepnumber.__dict__)

    send = {
        "number_details" : json.loads(json_num),
        "location" : location,
        "service_provider" : service_pro,
        "is_valid" : is_valid,
        "name_user" : name_user,
        "timezone" : timeZone ,
        "is_dialled_internationaly" : code,
        "indexed_number" : n,
    }

    return jsonify(send)


if __name__ == "__main__":
    app.run(debug=True , port=8000)