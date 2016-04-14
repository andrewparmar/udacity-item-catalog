from flask import Flask, render_template, url_for, request, redirect, jsonify
# import jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# #Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# # restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

# #Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurants/new', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['newRest'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    return render_template('newRestaurants.html')

@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
        restaurant.name = request.form['editRest']
        session.commit()
        return redirect(url_for('showRestaurants'))
    return render_template('editRestaurants.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        try:
            restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
            session.delete(restaurant)
            session.commit()
            return redirect(url_for('showRestaurants'))
        except:
            return redirect(url_for('showRestaurants'))
    name = session.query(Restaurant.name).filter(Restaurant.id == restaurant_id).one()
    return render_template('deleteRestaurants.html', restaurant_id = restaurant_id, name = name)

@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    menu = session.query(MenuItem).join(MenuItem.restaurant).filter(Restaurant.id==restaurant_id)
    return render_template('menu.html', restaurant_id = restaurant_id, menu = menu)

@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newMenu = MenuItem(name = request.form['newItem'], restaurant_id = restaurant_id, description = request.form['newDescription'], price=request.form['newPrice'], course = request.form['course'])
        # newMenu = MenuItem(name = request.form['newItem'], restaurant_id = restaurant_id)
        session.add(newMenu)
        session.commit()
        return redirect(url_for('showRestaurants'))
    name = session.query(Restaurant.name).filter(Restaurant.id == restaurant_id).one()
    return render_template('newMenuItem.html', restaurant_id = restaurant_id, name = name)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        menuItem = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id,MenuItem.id == menu_id).one()
        menuItem.name = request.form['editMenu']
        menuItem.description = request.form['editDescription'] 
        menuItem.price = request.form['editPrice'] 
        menuItem.course = request.form['editCourse'] 
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    jam = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id,MenuItem.id == menu_id).one()
    return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, jam = jam)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        try:
            menuItem = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id,MenuItem.id == menu_id).one()
            session.delete(menuItem)
            session.commit()
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
        except:
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    jam = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id,MenuItem.id == menu_id).one()
    return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, jam = jam)

@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    # session.query
    # jam = session.query(MenuItem).filter(MenuItem.restaurant_id == 1,MenuItem.id == 1).one()
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])
    # return jsonify(restaurants=[1,2,3,4,5,6])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def showRestaurantMenuJSON(restaurant_id):
    menu = session.query(MenuItem).join(MenuItem.restaurant).filter(Restaurant.id==restaurant_id)
    print menu
    return jsonify(menu=[m.serialize for m in menu])

# @app.route('/restaurants/restaurant_id/menu/menu_id/JSON')


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port=5000 )
