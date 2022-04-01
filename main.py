from flask import render_template, Flask, request
from twilio.rest import Client
import requests

account_sid = 'AC4eacd966690d31ebac26bff35042c33e'
auth_token = '926800a997c6a37579ed668fb215af1b'

client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def registration_form():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login_registration_dtls():
    f_name = request.form['fname']
    l_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source_dt']
    des_st = request.form['desti_state']
    des_dt = request.form['desti_dt']
    phone = request.form['phoneNumber']
    id_proof = request.form['idcard']
    date = request.form['trip']
    full_name = f_name + " " + l_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[des_st]['districts'][des_dt]['total']['confirmed']
    pop = json_data[des_st]['districts'][des_dt]['meta']['population']
    travel_pass = ((cnt / pop) * 100)
    if travel_pass < 30 and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(from_='+12019891998',
                               to='+91'+phone,
                               body="Hello" + " " + full_name + ". " + "Your Travel from" + " " + source_dt + " " + "to" + " " + des_dt + " " + "has been" +
                                    " " + status + " on" + " " + date+".")

        return render_template('user_registration_dtls.html', var1=full_name, var2=email_id, var3=id_proof,
                               var4=source_st, var5=source_dt, var6=des_st, var7=des_dt, var8=phone, var9=status, var10=date)
    else:
        status = 'NOT CONFIRMED'
        client.messages.create(from_='+12019891998',
                               to='+91'+phone,
                               body="Hello" + " " + full_name + " " + " Your Travel from " + " " + source_dt + " " + "to" + " " + des_dt + " " + "has" +
                                    " " + status + " On" + " " + date + " " + ", Apply later")

        return render_template('user_registration_dtls.html', var1=full_name, var2=email_id, var3=id_proof,
                               var4=source_st, var5=source_dt, var6=des_st, var7=des_dt, var8=phone, var9=status, var10=date)


if __name__ == "__main__":
    app.run(debug=True)