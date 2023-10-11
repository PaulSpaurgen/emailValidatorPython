from flask import Flask, request, jsonify
import re
import dns.resolver
import socket
import smtplib



app = Flask(__name__)

@app.route('/api/validateEmail', methods=['GET'])
def get_items():
    email = request.args.get('email', 'Guest')
    print("email==>",email)
    addressToVerify =email
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

    if match == None:
        print('Bad Syntax')
        return jsonify({
          "error": True,
          "reason": "not valid email"
        })

    records =  dns.resolver.resolve('scottbrady91.com', 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)

    host = socket.gethostname()

    # SMTP lib setup (use debug level for full output)
    

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Enable TLS for security
    server.set_debuglevel(0)

    email = "gspaurgen@gmail.com"
    password = "pasj78tt5u@G"

    print( "server before login ====>",server)


    server.login(email, password)

    print( "server after login ====>",server)


    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(host)
    server.mail('gspaurgen@gmail.com')

    print( "server after login connect ====>",server)
    code, message = server.rcpt(str(addressToVerify))
    print("code===>",code,"message==>",message)
    server.quit()

    

# Assume 250 as Success
    isValid = False
    if code == 250:
        isValid = True
        print('Success')
    else:
        isValid = False
        print('Bad')
    return jsonify({
        "isEmail" : isValid 
    })

if __name__ == '__main__':
    app.run(debug=True)
