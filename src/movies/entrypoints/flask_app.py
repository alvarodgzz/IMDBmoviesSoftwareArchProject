from flask import Flask, request, render_template
from movies import models
import csv
import os


app = Flask(__name__)
models.start_mappers()

# This method is applying the Single Responsibility Principle, this method has only 
# one responsability/job, to get the list of movies with the parameters given by the user
def getRecommendations(pref1, pref2, pref3, size):
    nPref  = pref1 * pref2 * pref3
    nPref = (nPref % 5) + 1

    rows = []
    with open('movie_results.csv', 'r', newline="") as file:
    # create the object of csv.reader()
        csvReader = csv.reader(file, delimiter=',')
        headers = next(csvReader)

        i = 0
        for row in csvReader:
            if (len(rows) == size):
                break
            if (row[0] == nPref):
                rows.append(row)
            rows.append({'title':row[1], 'stars':row[2], 'rating':row[3]})
            i = i + 1

        # This statement is applying the Interface Segregation Principle, this is external
        # for the interface or user scope. This is for development and will always be 
        # segregated from the interface.
        print("THIS ARE YOUR RECOMMENDATIONS!!!")
    return rows


@app.route("/hello", methods=["GET"])
def hello_world():
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in %r: %s" % (cwd, files))
    return "Hello World!", 200

@app.route("/recommendations/<int:pref1>/<int:pref2>/<int:pref3>", methods=["GET"])
@app.route("/recommendations/<int:pref1>/<int:pref2>/<int:pref3>/<int:size>", methods=["GET"])
@app.route("/recommendations/<int:pref1>/<int:pref2>/<string:rating>", methods=["GET"])
@app.route("/recommendations/<int:pref1>/<int:pref2>/<int:pref3>/<int:size>/<string:rating>", methods=["GET"])
def get_movie_recommendations(pref1, pref2, pref3, size=10, rating=True):
        rows = getRecommendations(pref1, pref2, pref3, size)

        # This funciton call is applying the Open Close Principle, we are making use of it as new code
        # with new behaviour, instead of modifying the existing code.
        newlist = sorted(rows, key=lambda d: d['rating'], reverse=False)

        if (rating == 'True'):
            return render_template('movieList.html', data=rows)
        else:
            return render_template('movieList.html', data=newlist)
