import requests
from flask import Flask, render_template, request
from twilio.rest import Client
import requests_cache
account_sid = "ACf34c4aea7c12f4f8f0699861cef0440a"
auth_token = "f79d0f78a8fb8e80d7cf6fbb8c9ddde8"
client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')
@app.route('/')
def registration_form():
    return render_template('form.html')

@app.route('/login_page', methods=['POST','GET'])
def login_reg_details():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source-state']
    source_dt = request.form['source-dt']
    dest_st = request.form['dest-st']
    dest_dt = request.form['dest-dt']
    pno = request.form['pno']
    date = request.form['trip']
    full_name = first_name+" "+last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[dest_st]['districts'][dest_dt]['total']['confirmed']
    pop = json_data[dest_st]['districts'][dest_dt]['meta']['population']
    travel_pass = ((cnt/pop)*100)
    if(travel_pass< 45) and request.method == 'POST':
        status = 'Confirmed'
        client.messages.create(to="whatsapp:+918555855643",
                               from_="whatsapp:+14155238886",
                               body="Hello "+full_name+" "+"Your Travel From "+source_dt+" To "+dest_dt+" dated "+date+" is "+status+".")
        return render_template('user_reg_details.html', var=full_name , var1=email_id,
                                var3=source_st,var4=source_dt,var5=dest_st,var6=dest_dt,
                               var7=pno,var8=date,var9=status) 
    else:
        status="Not Confirmed"
        client.messages.create(to="whatsapp:+918555855643",
                               from_="whatsapp:+14155238886",
                               body="Hello "+full_name+" "+"Your Travel From "+source_dt+" To "+dest_dt+" dated "+date+" is "+status+".")
        return render_template('user_reg_details.html', var=full_name, var1=email_id,
                                var3=source_st, var4=source_dt, var5=dest_st, var6=dest_dt,
                               var7=pno, var8=date, var9=status)

if __name__ == '__main__':
    app.run(port=3011,debug=True)