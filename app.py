from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import steam_game_id
import benchmark_fetch

app = Flask(__name__)
CORS(app) 

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
        cpu_name, gpu_name = None, None
        
        if isinstance(specs['Processor'], list):
            cpu_name = specs['Processor'][0]
        else:
            cpu_name = specs['Processor']
            
        if isinstance(specs['Graphics'], list):
            gpu_name = specs['Graphics'][0]
        else:
            gpu_name = specs['Graphics']
            
        score_dict = benchmark_fetch.fetch_particular_score(cpu_name, gpu_name) #closest_cpu, score, closest_gpu, score
        return jsonify(specs | score_dict)
    except KeyError:
        return jsonify({"response": "Couldn't Find Game!"})

if __name__ == '__main__':
    app.run(debug=True)
