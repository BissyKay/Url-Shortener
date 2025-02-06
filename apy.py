from flask import Flask, request, redirect, render_template
import hashlib

app = Flask(__name__)

# Dictionary to store shortened URLs
url_mapping = {}

def generate_secure_short_code(long_url):
    """Generate a SHA256-based short code for the URL."""
    hash_object = hashlib.sha256(long_url.encode())
    return hash_object.hexdigest()[:8]  # Use first 8 chars for uniqueness

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = generate_secure_short_code(long_url)
        url_mapping[short_code] = long_url
        short_url = request.host_url + short_code
        return render_template('index.html', short_url=short_url, long_url=long_url)
    return render_template('index.html', short_url=None)

@app.route('/<short_code>')
def redirect_to_long(short_code):
    """Redirect the user to the original long URL after verifying safety."""
    long_url = url_mapping.get(short_code)
    if long_url:
        return redirect(long_url)
    return "Invalid or expired short URL", 404

if __name__ == '__main__':
    app.run(debug=True)
