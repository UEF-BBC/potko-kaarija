import PCA9685
import time

from flask import Flask, request, jsonify
import wifi_Rpi as wifi
import asyncio
import threading


async def reply_to_device_queries_on_background():
    wifi.respond_to_device_query()

pwm = PCA9685.PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)



app = Flask(__name__)


@app.route('/echo', methods=['POST'])
def echo():
    # Get the posted data (JSON or form data)
    print("Got message")
    data = request.get_json() or request.form.to_dict()
    
    dataj = request.get_json()

    print("Received data:",dataj)

    xValue = dataj.get('xValue')
    yValue = dataj.get('yValue')

    print("xValue is ",xValue)
    print("yValue is ",yValue)

    #Scale to range the servo wants
    xScaled = xValue*2000 + 500
    yScaled = yValue*2000 + 500

    pwm.setServoPulseScaled(0,xScaled)   
    pwm.setServoPulseScaled(1,yScaled)   
#    pwm.setServoPulse200(0,xScaled)   
#    pwm.setServoPulse200(1,yScaled)   

    ## setServoPulse(2,2500)
    #for i in range(500,2500,10):  
    #    pwm.setServoPulse200(0,i)   
    #    time.sleep(0.02)     

    #for i in range(2500,500,-10):
    #    pwm.setServoPulse200(0,i) 
    #    time.sleep(0.02)  

    return jsonify(data)


# Function to run Flask in a separate thread
def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

# Main function to run both Flask and asyncio
def main():
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    # Run asyncio loop in the main thread
    asyncio.run(reply_to_device_queries_on_background())


if __name__ == '__main__':
    main()
    # Bind to all available IP addresses on the local network
    #app.run(host='0.0.0.0', port=5000)



 