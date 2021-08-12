from App.app import app
from os import environ
from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    port_number = environ.get('PORT', 9000)
    hostname = environ.get('HOST', "0.0.0.0")

    app.run(debug=True, port=port_number, host=hostname)
