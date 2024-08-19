import PCA9685
import time

from flask import Flask, request, jsonify

pwm = PCA9685.PCA9685(0x40, debug=False)
pwm.setPWMFreq(200)


app = Flask(__name__)


@app.route('/echo', methods=['POST'])
def echo():
    # Get the posted data (JSON or form data)
    print("Got message")
    data = request.get_json() or request.form.to_dict()
    
    dataj = request.get_json()

    print("Received data:",dataj)

    xValue = dataj.get('xValue')

    print("xValue is ",xValue)

    #Scale to range the servo wants
    xScaled = xValue*2000 + 500

    pwm.setServoPulse200(0,xScaled)   

    ## setServoPulse(2,2500)
    #for i in range(500,2500,10):  
    #    pwm.setServoPulse200(0,i)   
    #    time.sleep(0.02)     

    #for i in range(2500,500,-10):
    #    pwm.setServoPulse200(0,i) 
    #    time.sleep(0.02)  

    return jsonify(data)


if __name__ == '__main__':
    # Bind to all available IP addresses on the local network
    app.run(host='0.0.0.0', port=5000)




 