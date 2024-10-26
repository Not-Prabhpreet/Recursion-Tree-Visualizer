from flask import Flask, render_template, send_file, request, jsonify, abort
import os
from .main import visualize  # Add the dot to indicate relative import
import traceback
import pydot

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_file(os.path.join(app.static_folder, filename))

@app.route('/visualize', methods=['POST'])
def visualize_route():
    data = request.json
    function_definition = data.get('definition', '').strip()
    function_call = data.get('call', '').strip()

    # Basic validation
    if not function_definition:
        return jsonify({"error": "Function definition is required"}), 400
    if not function_call:
        return jsonify({"error": "Function call is required"}), 400

    try:
        dot_content = visualize(function_definition, function_call)
        try:
            graph, = pydot.graph_from_dot_data(dot_content)
            svg_content = graph.create_svg().decode('utf-8')
            return jsonify({"svg": svg_content})
        except (ValueError, IndexError) as e:
            return jsonify({"error": "Error generating visualization. Please check your input."}), 400
    except ValueError as e:
        # Handle specific validation errors
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle unexpected errors
        error_message = str(e)
        print(f"Error in visualize_route: {error_message}\n{traceback.format_exc()}")
        return jsonify({"error": "An unexpected error occurred. Please check your inputs and try again."}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)  # Added debug=True