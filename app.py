from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

#database connection details (change as needed)
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

queryInputs = []
@app.route('/')
def index():
    return render_template('index.html')
#Configure db


@app.route('/query1', methods = ['GET', 'POST'])
def query1():
        return render_template('query1.html')

@app.route('/query2', methods = ['GET', 'POST'])
def query2():
        return render_template('query2.html')

@app.route('/query3', methods = ['GET', 'POST'])
def query3():
        return render_template('query3.html')

@app.route('/query4', methods = ['GET', 'POST'])
def query4():
        return render_template('query4.html')

@app.route('/query5', methods = ['GET', 'POST'])
def query5():
        return render_template('query5.html')

@app.route('/query6', methods = ['GET', 'POST'])
def query6():
        return render_template('query6.html')

@app.route('/query7', methods = ['GET', 'POST'])
def query7():
        return render_template('query7.html')

@app.route('/query8', methods = ['GET', 'POST'])
def query8():
        if request.method == 'POST':
                year = request.form.get("season")
                squad = request.form.get('squad')
                numPlayers = request.form.get('numplayers')
                age = request.form.get('age')
                poss = request.form.get('poss')
                min = request.form.get('min')
                ninety = request.form.get('ninety')
                Gls = request.form.get('Gls')
                Ast = request.form.get('Ast')
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO all_squad_standard_stats(Year, Squad, NumPlayers, Age, Poss, Min, 90s, Gls, Ast) VALUES(" + year + ", %s, " + numPlayers + ", " + age + ", " + poss + ", " + min + ", " + ninety + ", " + Gls + ", " + Ast + ")", (squad,))
        return render_template('query8.html')

@app.route('/query9', methods = ['GET', 'POST'])
def query9():
        return render_template('query9.html')

@app.route('/query10', methods = ['GET', 'POST'])
def query10():
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM teams")
        if resultValue > 0:
            userDetails = cur.fetchall()
            return render_template('query10.html', userDetails=userDetails)


@app.route('/query9answer', methods = ["POST"])
def query9answer():
    team = request.form.get("team")
    season = request.form.get("season")
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT all_squad_standard_stats.year, all_squad_standard_stats.squad, all_squad_standard_stats.NumPlayers, all_squad_standard_stats.MP, all_squad_standard_stats.Gls, all_squad_standard_stats.Ast, all_squad_standard_stats.GToPK, all_squad_standard_stats.PK, all_squad_shooting_stats.Sh, all_squad_shooting_stats.SoT, all_squad_shooting_stats.SoTPerc, all_squad_shooting_stats.Dist FROM all_squad_standard_stats JOIN all_squad_shooting_stats ON all_squad_shooting_stats.squad = all_squad_standard_stats.Squad WHERE all_squad_standard_stats.squad= %s AND all_squad_shooting_stats.squad= %s  AND all_squad_standard_stats.year=" + season + " AND all_squad_shooting_stats.year=" + season + "", (team, team))
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('query9answer.html', userDetails=userDetails)

#Stored Procedure
@app.route('/query7answer', methods = ["POST"])
def query7answer():
    player = request.form.get("player")
    season = request.form.get("season")
    cur = mysql.connection.cursor()
    cur.callproc('getTeamRecordFromPlayerSeason', [player, int(season)])
    userDetails = cur.fetchall()
    return render_template('query7answer.html', userDetails=userDetails)

#Stored Procedure
@app.route('/query6answer', methods = ["POST"])
def query6answer():
    player = request.form.get("player")
    season = request.form.get("season")
    cur = mysql.connection.cursor()
    cur.callproc('getPlayerStatsForYear', [int(season), player])
    userDetails = cur.fetchall()
    return render_template('query6answer.html', userDetails=userDetails)

#Stored Procedure
@app.route('/query5answer', methods = ["POST"])
def query5answer():
    player = request.form.get("player")
    cur = mysql.connection.cursor()
    cur.callproc('getAllIndividualPlayerStats', [player])
    userDetails = cur.fetchall()
    return render_template('query5answer.html', userDetails=userDetails)
        

@app.route('/query4answer', methods = ["POST"])
def query4answer():
    season = request.form.get("season")
    playercount = request.form.get("playercount")
    statistic = request.form.get("statistic")
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT Player, " + statistic + " FROM all_player_standard_stats WHERE Year=" + season + " ORDER BY " + statistic + " DESC LIMIT " + playercount)
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('query4answer.html', userDetails=userDetails)

@app.route('/query3answer', methods = ["POST"])
def query3answer():
    season = request.form.get("season")
    cur = mysql.connection.cursor()
    userDetails = 0
    userDetails2 = 0
    resultValue = cur.execute("SELECT Player, Gls FROM all_player_standard_stats WHERE Year=" + season + " ORDER BY Gls DESC LIMIT 1")
    if resultValue > 0:
        userDetails = cur.fetchall()
    resultValue2 = cur.execute("SELECT Player, Ast FROM all_player_standard_stats WHERE Year=" + season + " ORDER BY Ast DESC LIMIT 1")
    if resultValue2 > 0:
        userDetails2 = cur.fetchall()
        return render_template('query3answer.html', userDetails=userDetails, userDetails2 = userDetails2)


@app.route('/query2answer', methods = ["POST"])
def query2answer():
    team = request.form.get("team")
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM all_league_tables WHERE Squad= %s", (team,))
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('query2answer.html', userDetails=userDetails)

@app.route('/query1answer', methods = ["POST"])
def query1answer():
    season = request.form.get("season")
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM all_league_tables WHERE Year=" + season)
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('query1answer.html', userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)
