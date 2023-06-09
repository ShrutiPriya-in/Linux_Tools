from flask import Flask, request
import requests
import blacklisted_countries # a separate file containing list of blacklisted countries



def filter_by_country(ip_addr):
    
    # Using ipapi.co, get the country of the ip address
    ip_details = requests.get(f'https://ipapi.co/{ip_addr}/json/').json()
    if 'country_name' not in ip_details:
        return True

    ip_country = ip_details['country_name']
    if ip_country.tolower() in (country.lower() for country in blacklisted_countries.countries):
        return False
    return True




app = Flask(__name__)

@app.route('/')
def ip_filter():
    ip_addr = request.remote_addr # get ip address of the incoming request 
    
    if filter_by_country(ip_addr):
        return "Welcome!"
    else:
        return "Sorry! You cannot access this page"
        


app.run(port=5500, debug =True)