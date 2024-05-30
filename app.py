import requests
from flask import Flask, jsonify, render_template, request, send_file, url_for, redirect

app = Flask(__name__)

information = {}

def get_forks(username):

    global information

    fork_url = f"https://api.github.com/users/{username}/repos"

    response = []

    try:

        response = requests.get(fork_url)

        if response.status_code != 200:
            # return jsonify({"error": "User not found"}), 404
            return redirect("/bad_results")
    
    except Exception as e:
        # return jsonify({"error": "User not found"}), 404
        return redirect("/bad_results")
    
    fork_info = response.json()

    count = 0

    for repo in fork_info:
        count += repo['forks']

    return count



@app.route('/')
def init():
    return render_template('index.html')



@app.route("/back_to_index", methods=["GET"])
def generate_get():
    return render_template("index.html"), 200


@app.route('/github-stats', methods=['POST', 'GET'])
def github_stats():

    global information

    username = request.form.get("username")

    if not username:
        return redirect("/bad_results")

    # print(username)

    api_url = f"https://api.github.com/users/{username}"

    response = []

    try:

        response = requests.get(api_url)

        if response.status_code != 200:
            # return jsonify({"error": "User not found"}), 404
            return redirect("/bad_results")
    
    except Exception as e:
        # return jsonify({"error": "User not found"}), 404
        return redirect("/bad_results")
    
    info = response.json()

    # print(info)

    information['user'] = info['login']
    information['num_repos'] = info['public_repos']

    if info['public_repos'] == 0:
        information['num_forks'] = 0
    else:
        information['num_forks'] = get_forks(username)

    return redirect('/good_results')

@app.route("/good_results", methods=["GET"])
def results_get():

    global information

    return render_template("good_results.html", information=information), 200


@app.route("/bad_results", methods=["GET"])
def result_status_get():

    # print(f"bad results status: {status}")

    return render_template("bad_results.html"), 200