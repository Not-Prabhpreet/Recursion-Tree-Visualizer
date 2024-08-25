from flask import Flask, render_template, send_file, request, jsonify
import os
from main import visualize
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
    function_definition = data.get('definition', '')
    function_call = data.get('call', '')

    print(f"Received function definition: {function_definition}")
    print(f"Received function call: {function_call}")

    try:
        dot_content = visualize(function_definition, function_call)
        try:
            graph, = pydot.graph_from_dot_data(dot_content)
            svg_content = graph.create_svg().decode('utf-8')
            return jsonify({"svg": svg_content})
        except (ValueError, IndexError):
            return jsonify({"error": "Error generating visualization. Please check your input."}), 400
    except Exception as e:
        error_message = f"Error in visualize_route: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return jsonify({"error": error_message}), 400

#if __name__ == '__main__':
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host='0.0.0.0', port=port)