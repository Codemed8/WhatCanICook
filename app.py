from flask import Flask,Blueprint, render_template, request,session,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'AiIyqBin1F1i'
db = SQLAlchemy(app)

class recipes(db.Model):
    id = db.Column("id",db.Integer,primary_key=True)
    site = db.Column(db.String(100))
    recipe_id = db.relationship('lookuptable', backref = 'lookuptable.recipes_site', primaryjoin='recipes.id==lookuptable.recipes_site')
    
    def __init__(self,site):
        self.site = site 

class ingredients(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)
    item = db.Column(db.String(100))
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    image_id = db.relationship('images', backref = 'imagesite')
    categories = db.relationship('categories', foreign_keys='ingredients.category')

    
    def __init__(self,item):
        self.site = item 

class categories(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)
    category = db.Column(db.String(100))
    def __init__(self,category):
        self.category = category 

class images(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)
    image = db.Column(db.String(100))
    image_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    def __init__(self,image):
        self.image = image 

class lookuptable(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)
    recipes_site = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    ingredients_item = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    
    recipe = db.relationship('recipes', foreign_keys='lookuptable.recipes_site')
    ingredients = db.relationship('ingredients', foreign_keys='lookuptable.ingredients_item')


    def __init__(self,recipes_site,ingredients_item):
        self.recipes_site = recipes_site
        self.ingredients_item = ingredients_item


def getAllIngred():
    rows = ingredients.query.all()
    ingredAndImage = {}
    for row in rows:
        lst = []
        lst.append(row.image_id[0].image)
        lst.append(row.categories.category)
        ingredAndImage[row.item] = lst 
    return ingredAndImage

def locatesites(lstofsubmittedingredients,row):
    hist ={}
    for usritem in lstofsubmittedingredients:
        for site in row:
            if usritem == site.ingredients.item :
                hist[site.recipe.site] = hist.get(site.recipe.site, 0) + 1

    hist = dict(sorted(hist.items(), key=lambda x: x[1],reverse=True))
    return (hist)





@app.route("/",methods=["POST","GET"])
def view():
    if request.method == "POST":
        lstofsubmittedingredients = (request.form.getlist('item'))
        row=lookuptable.query.all()
        hist = locatesites(lstofsubmittedingredients,row)
        return render_template("view.html", values=hist)

    else:
        ingredAndImage = getAllIngred()
        return render_template("index.html", ingredAndImage=ingredAndImage)


if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
