from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/echo', methods=['POST'])
def echo():
    # Get the posted data (JSON or form data)
    print("Got message")
    data = request.get_json() or request.form.to_dict()
    
    # Return the same data as JSON
    return jsonify(data)

if __name__ == '__main__':
    # Bind to all available IP addresses on the local network
    app.run(host='0.0.0.0', port=5000)