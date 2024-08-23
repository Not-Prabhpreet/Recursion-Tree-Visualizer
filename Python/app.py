from flask import Flask, render_template, send_file, request
import os
from main import visualize
import traceback

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_file(os.path.join(app.static_folder, filename))

@app.route('/rendered/<filename>')
def serve_svg(filename):
    rendered_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'rendered')
    return send_file(os.path.join(rendered_folder, filename), mimetype='image/svg+xml')

@app.route('/visualize')
def visualize_route():
    function_definition = request.args.get('definition', '')
    function_call = request.args.get('call', '')

    print(f"Received function definition: {function_definition}")
    print(f"Received function call: {function_call}")

    try:
        dot_content = visualize(function_definition, function_call)
        print("Dot content (first 100 chars):", dot_content[:100])
        
        filename = 'recursion_tree.dot'
        
        rendered_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'rendered')
        os.makedirs(rendered_folder, exist_ok=True)
        file_path = os.path.join(rendered_folder, filename)
        with open(file_path, 'w') as f:
            f.write(dot_content)

        return filename
    except Exception as e:
        error_message = f"Error in visualize_route: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return f"Error: {error_message}", 400
if __name__ == '__main__':
    app.run(debug=True)