from flask import Flask, render_template, jsonify, make_response
from sng_demo.database import Memgraph
from sng_demo import db_operations

app = Flask(__name__)


# @app.route('/')
@app.route('/index')
def index():
    db = Memgraph()
    # db_operations.clear(db)
    # db_operations.populate_database(db, "resources/data_grappling.txt")
    return render_template('index.html')

@app.route('/reseed')
def reseed():
    db = Memgraph()
    print("in reseed")
    db_operations.clear(db)
    db_operations.populate_database(db, "resources/data_grappling.txt")
    return render_template('distances.html')

@app.route('/gojs')
def gojs():
    return render_template('gojs.html')

@app.route('/minimal')
def minimal():
    return render_template('minimal.html')

@app.route('/')
@app.route('/distances')
def distances():
    return render_template('distances.html')

@app.route('/inspector')
def inspector():
    return render_template('DataInspector.html')

@app.route('/animation')
def animation():
    return render_template('pathAnimation.html')

@app.route('/concept')
def concept():
    return render_template('conceptMap.html')

@app.route('/query')
def query():
    return render_template('query.html')

@app.route("/get-graph", methods=["POST"])
def get_graph():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_graph(db)), 200)
    return response

@app.route('/get-users', methods=["POST"])
def get_users():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_users(db)), 200)
    return response

@app.route('/get-user/<string:user_id>', methods=["GET"])
def get_user(user_id):
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_user(db, user_id)), 200)
    return response

@app.route('/get-relationships', methods=["POST"])
def get_relationships():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_relationships(db)), 200)
    return response

@app.route('/get-frame/<string:frame_id>', methods=["GET"])
def get_frame(frame_id):
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_frame(db, frame_id)), 200)
    return response

@app.route('/get-frames', methods=["GET"])
def get_frames():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_frames(db)), 200)
    return response

@app.route('/get-transitions', methods=["GET"])
def get_transitions():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_transitions(db)), 200)
    return response

@app.route("/get-ggraph", methods=["GET"])
def get_ggraph():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_ggraph(db)), 200)
    return response