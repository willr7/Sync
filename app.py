from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import steam_game_id
import benchmark_fetch
from suggestion import suggestions
from make_build import build_pc

app = Flask(__name__)
CORS(app) 

# Initialize a counter
counter = 0

@app.route('/')
def index():
    return render_template('pretty.html')


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
        gpu_score = score_dict["gpu_score"]
        cpu_score = score_dict["cpu_score"]
        build = build_pc(cpu_score, gpu_score)
        total_sum = sum(elem[1] for elem in build.values())
        
        return jsonify(specs | score_dict | build | {"sum": total_sum})
    except KeyError:
        return jsonify({"response": "Couldn't Find Game!"})

@app.route('/get_game_suggestions', methods=['GET'])
def get_game_suggestions():
    query = request.args.get('query')
    return jsonify(suggestions(query))

if __name__ == '__main__':
    app.run(debug=True)
