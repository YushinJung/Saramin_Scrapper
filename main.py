from getting_jobs_from_saramin_url import crolling, save_list_dict_job_to_csv

from flask import Flask, render_template, request, redirect, send_file

app = Flask("Saramin Scrapper")
db = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/report")
def report():
    word_input = request.args.get('word_input').lower()
    display_number = int(request.args.get('number'))

    if db.get(word_input):
        list_dict_job = db[word_input]
    else:
        list_dict_job = crolling(word_input)
        db[word_input] = list_dict_job
    
    total_job = len(list_dict_job)
    if display_number < 0 :
        display_number = total_job
    elif display_number > total_job:
        display_number = total_job
        
    return render_template('report.html', word_input=word_input, total_job=total_job, display_number=display_number, jobs=list_dict_job[:display_number])

@app.route("/export")
def export():
    word_input = request.args.get('word_input').lower()
    list_dict_job = db[word_input]
    d_csv = save_list_dict_job_to_csv(list_dict_job, word_input)
    return send_file(d_csv)

app.run(host="0.0.0.0")