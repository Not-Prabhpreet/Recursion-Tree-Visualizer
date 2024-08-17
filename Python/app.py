from flask import Flask, render_template, send_file
from main import save_svg
import os

app = Flask(__name__, template_folder='../templates')

# Route to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Route to generate and serve the SVG
@app.route('/rendered/recursion_tree.svg')
def serve_svg():
    # Ensure the SVG is generated
    save_svg()  # Adjust this line to call your existing visualization logic
    return send_file('../rendered/recursion_tree.svg', mimetype='image/svg+xml')  # Updated path

if __name__ == '__main__':
    # Ensure the rendered folder exists
    os.makedirs('../rendered', exist_ok=True)  # Updated path
    app.run(debug=True)





