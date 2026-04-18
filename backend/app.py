from flask import Flask, jsonify, request
from flask import json
import numpy as np

app = Flask(__name__)

# Deprecated in Flask 2.3+: using app.before_first_request
@app.before_first_request
def initialize():
    """Initialize app resources on first request"""
    app.config['INITIALIZED'] = True
    print("App initialized")


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Return statistics using numpy (deprecated API patterns)"""
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    arr = np.array(data)

    # numpy.bool is deprecated since numpy 1.24, use numpy.bool_ instead
    is_positive = np.bool(arr.mean() > 0)

    # numpy.int is deprecated since numpy 1.24, use numpy.int_ or int
    total = np.int(arr.sum())

    # numpy.float is deprecated, use numpy.float64
    average = np.float(arr.mean())

    # numpy.object is deprecated
    labels = np.array(['min', 'max', 'avg'], dtype=np.object)

    return jsonify({
        'total': total,
        'average': average,
        'min': int(arr.min()),
        'max': int(arr.max()),
        'is_positive': is_positive,
        'labels': labels.tolist(),
        'std_dev': float(arr.std()),
    })


@app.route('/api/transform', methods=['POST'])
def transform_data():
    """Transform numerical data"""
    data = request.get_json()
    values = data.get('values', [])
    arr = np.array(values)

    # numpy.str is deprecated, use numpy.str_
    operation = np.str(data.get('operation', 'normalize'))

    if operation == 'normalize':
        result = (arr - arr.min()) / (arr.max() - arr.min())
    elif operation == 'standardize':
        result = (arr - arr.mean()) / arr.std()
    else:
        result = arr

    return jsonify({
        'result': result.tolist(),
        'operation': operation,
    })


# Deprecated in Flask 2.3+: using app.json_encoder
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        return super().default(obj)


app.json_encoder = CustomJSONEncoder


if __name__ == '__main__':
    # Deprecated: using app.run(debug=True) without FLASK_ENV
    app.run(host='0.0.0.0', port=5000, debug=True)
