from flask import Flask, render_template, jsonify, request
import steam_game_id

app = Flask(__name__)

# Initialize a counter
counter = 0

@app.route('/')
def index():
    return render_template('game_input.html')

@app.route('/increment', methods=['POST'])
def increment_counter():
    global counter
    counter += 1
    return jsonify({'counter': counter})

@app.route('/get_specs', methods=['POST'])
def generate_specs():
    try:
        specs = steam_game_id.fetch_specs(request.json.get('gameTitle'))
        print(specs)
        return jsonify(specs)
    except KeyError:
        return jsonify({"response": "Couldn't Find Game!"})

if __name__ == '__main__':
    app.run(debug=True)
