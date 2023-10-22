import json

def reformat_json(json_file):
  """Reformats a JSON file from the format {model: [benchmark, price]} to the format {model: benchmark}.

  Args:
    json_file: The path to the JSON file to reformat.

  Returns:
    A dictionary containing the reformatted JSON data.
  """

  with open(json_file, "r") as f:
    json_data = json.load(f)

  reformatted_json_data = {}
  for model, benchmark_and_price in json_data.items():
    benchmark = benchmark_and_price[0]
    reformatted_json_data[model] = benchmark

  return reformatted_json_data

reformatted_json_data = reformat_json("cpu_benchmarks.json")

with open("formatted_cpu_benchmarks.json", "w") as f:
  json.dump(reformatted_json_data, f, indent=4)

