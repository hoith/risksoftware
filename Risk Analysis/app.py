from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
app.secret_key = "your_secret_key"  # REPLACE with a strong, randomly generated key!
# Enable CORS for all routes and all origins (for development - be more restrictive in production)
CORS(app, resources={r"/*": {"origins": "*"}}) #Allow requests from all origins

# Placeholder user data - REPLACE WITH A REAL DATABASE!
users = {"user1": "password", "user2": "password2"}


@app.route('/', methods=['GET', 'POST'])  # Route for both GET (initial page load) and POST (login submit)
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:  # Replace this with actual database authentication
            session['username'] = username  # Set the session
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401  # 401 Unauthorized

    return render_template('login.html') # Only for GET



@app.route('/dashboard')
def dashboard():
    if "username" in session:  # User must be logged in to access dashboard
        return render_template('dashboard.html', username=session['username'])  # Render dashboard template
    else:
        return redirect('/') # If not logged in, go to the login page

@app.route('/api/market_risk', methods=['POST'])
def market_risk_api():
    try:
        data = request.get_json()

        asset_prices = data.get('asset_prices')
        confidence_level = data.get('confidence_level')
        method = data.get('method')
        distribution = data.get('distribution')

        risk_software = RiskManagementSoftware()

        if method == "historical":
            var = risk_software.calculate_market_risk_historical(asset_prices, confidence_level)
        else:  # Parametric
            var = risk_software.calculate_market_risk_parametric(asset_prices, confidence_level, method=distribution)

        return jsonify({'var': var})
    except (TypeError, ValueError) as e:
        return jsonify({'error': str(e)}), 400 #Bad request
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500 #Internal server error



@app.route('/api/credit_risk', methods=['POST'])
def credit_risk_api():
    try:
        data = request.get_json()
        pd = data.get('pd')
        lgd = data.get('lgd')
        ead = data.get('ead')

        risk_software = RiskManagementSoftware()
        el = risk_software.calculate_credit_risk(pd, lgd, ead)

        return jsonify({'el': el})

    except (TypeError, ValueError) as e:

        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500



@app.route('/api/operational_risk', methods=['POST'])
def operational_risk_api():
    try:
        data = request.get_json()

        losses = data.get('losses')
        percentile = data.get('percentile')

        risk_software = RiskManagementSoftware()
        op_risk = risk_software.calculate_operational_risk(losses, percentile)

        return jsonify({'op_risk': op_risk})

    except (TypeError, ValueError) as e:
        return jsonify({'error': str(e)}), 400  # Bad Request
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500  # Internal Server Error





@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear the session
    return redirect('/')


if __name__ == "__main__":

    app.run(debug=True)