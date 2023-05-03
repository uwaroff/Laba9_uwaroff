from flask import Flask, render_template, url_for, redirect, request
import sqlalchemy as db




def searchdd(serchText):

    select_query = db.select(accessories).where(accessories.columns.hardware_part == serchText)
    select_result = connection.execute((select_query))
    searchGemas =select_result.fetchall()
    if len(searchGemas) ==0:
        select_query = db.select(accessories).where(accessories.columns.price == serchText)
        select_result = connection.execute((select_query))
        searchGemas = select_result.fetchall()
    return searchGemas


app = Flask(__name__)


try:
    engine = db.create_engine('mysql+pymysql://root:ason121245@localhost:3306/my_database')
    connection = engine.connect()
    print("Connect DB")
except Exception as ex:
    print("ERROR Connect DB")
    print(ex)

metadata = db.MetaData()
accessories = db.Table('accessories', metadata,
                 db.Column('accessories_id', db.Integer, primary_key=True),
                 db.Column('hardware_part', db.Text),
                 db.Column('price', db.Integer))

metadata.create_all(engine)

insertion_query = accessories.insert().values([
    {"hardware_part":"motherboard", "price":7000},
    {"hardware_part":"Central Processing Unit", "price":16000},
    {"hardware_part":"Graphics Processing Unit", "price":4500},
    {"hardware_part":"Random Access Memory", "price":7600},
    {"hardware_part":"Hard Drive/SSD", "price":5200},
    {"hardware_part":"Power Supply Unit", "price":2300},
    {"hardware_part":"Cooling System", "price":5000},
    {"hardware_part":"Case", "price":10000},
    {"hardware_part":"Display", "price":25000},
    {"hardware_part":"Keyboard", "price":3500},
    {"hardware_part":"Mouse", "price":2000}

])
#connection.execute(insertion_query)

selall = db.select(accessories)
selres = connection.execute(selall)
allAccessories = selres.fetchall()

@app.route('/', methods =["GET", "POST"])
def index():
    sum = 0
    for i in range(len(allAccessories)):
        sum  = sum + allAccessories[i][2]
    if request.method == "POST":
        if request.form.get('clear') =='Clear':
            d = searchdd("s")
            return render_template('index.html', allGames=d, len=len(d))
        elif request.form.get('all') =='All List':
            render_template('index.html' , allGames = allAccessories, len = len(allAccessories))
        elif request.form.get('searchBtn') == 'Search':
            a = request.form.get("search")
            d = searchdd(a)
            return render_template('index.html' , allGames = d, len = len(d))
    return render_template('index.html' , allGames = allAccessories, len = len(allAccessories),sum = sum)

if __name__ == '__main__':
    app.run(debug=True, port=5001 )




