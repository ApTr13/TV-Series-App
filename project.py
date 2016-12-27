from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Series, Episode, User
from flask import session as login_session
import random
import string
import os
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
app = Flask(__name__)

# Flask Project file
# for the TV Series Application
# built by aptr13 <http://aptr13.me>

engine = create_engine('sqlite:///series.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Login page with state
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits)for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Routing to connect with FB Page
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in login_session in order to properly logout,
    # let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


# Logout from Session
@app.route('/logout')
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['facebook_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['provider']
    print "User got logged out"
    flash("You have successfully been logged out.")
    return redirect(url_for('showSerieses'))
    # return "you have been logged out"


# User Helper Functions
# Function to create a user in database if the user logs in for first time
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Function to get User data when user_id is given
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Function to get uder_id when email is given
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON APIs to view all Epiaodes in a given Series
@app.route('/series/<int:series_id>/episodes/JSON')
def seriesEpisodesJSON(series_id):
    series = session.query(Series).filter_by(id=series_id).one()
    episodes = session.query(Episode).filter_by(series_id=series_id).all()
    return jsonify(Episode=[i.serialize for i in episodes])


# JSON APIs to view given Epiaode
@app.route('/series/<int:series_id>/episodes/<int:episode_id>/JSON')
def episodeJSON(series_id, episode_id):
    episode = session.query(Episode).filter_by(id=episode_id).one()
    return jsonify(Episode=episode.serialize)


# JSON APIs to view all series
@app.route('/series/JSON')
def seriesesJSON():
    serieses = session.query(Series).all()
    return jsonify(serieses=[r.serialize for r in serieses])


# Show all serieses
@app.route('/')
@app.route('/series/')
def showSerieses():
    serieses = session.query(Series).order_by(asc(Series.name))
    if 'username' not in login_session:
        return render_template('publicserieses.html', serieses=serieses)
    else:
        print "User logged in -"+login_session['username']
        return render_template(
            'serieses.html', serieses=serieses, user=login_session['username'])


# Create a new series
@app.route('/series/new/', methods=['GET', 'POST'])
def newSeries():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newSeries = Series(name=request.form[
            'name'], rating=request.form[
                'rating'], actors=request.form[
                    'actors'], user_id=login_session['user_id'])
        session.add(newSeries)
        flash('New Series %s Successfully Added' % newSeries.name)
        session.commit()
        print "Series add Success"
        return redirect(url_for('showSerieses'))
    else:
        return render_template('newseries.html')


# Edit a series
@app.route('/series/<int:series_id>/edit/', methods=['GET', 'POST'])
def editSeries(series_id):
    editedSeries = session.query(Series).filter_by(id=series_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedSeries.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this series. Please create your own series in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedSeries.name = request.form['name']
            editedSeries.rating = request.form['rating']
            editedSeries.actors = request.form['actors']
            session.add(editedSeries)
            session.commit()
            print "Series edit Success"
            flash('Series Successfully Edited %s' % editedSeries.name)
            return redirect(url_for('showSerieses', series_id=series_id))
    else:
        return render_template('editseries.html', series=editedSeries)


# Delete a series
@app.route('/series/<int:series_id>/delete/', methods=['GET', 'POST'])
def deleteSeries(series_id):
    seriesToDelete = session.query(Series).filter_by(id=series_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if seriesToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this series. Please create your own series in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(seriesToDelete)
        flash('%s Successfully Deleted' % seriesToDelete.name)
        session.commit()
        print "Series delete Success"
        return redirect(url_for('showSerieses', series_id=series_id))
    else:
        return render_template('delseries.html', series=seriesToDelete)


# Show all Episodes in a given Series
@app.route('/series/<int:series_id>/')
@app.route('/series/<int:series_id>/episodes/')
def showEpisodes(series_id):
    series = session.query(Series).filter_by(id=series_id).one()
    creator = getUserInfo(series.user_id)
    episodes = session.query(Episode).filter_by(series_id=series_id).all()
    if'username'not in login_session or creator.id != login_session['user_id']:
        return render_template(
            'publicepisodes.html', episodes=episodes, series=series, creator=creator)
    else:
        return render_template(
            'episodes.html', episodes=episodes, series=series, creator=creator)


# Create a new episode
@app.route('/series/<int:series_id>/episodes/new/', methods=['GET', 'POST'])
def newEpisode(series_id):
    if 'username' not in login_session:
        return redirect('/login')
    series = session.query(Series).filter_by(id=series_id).one()
    if login_session['user_id'] != series.user_id:
        return """<script>function myFunction() {alert(
            'You are not authorized to edit this series.
            Please create your own series in order to edit.');}
            </script><body onload='myFunction()''>"""
    if request.method == 'POST':
        newEpisode = Episode(name=request.form[
            'name'], description=request.form[
                'description'], air_date=request.form[
                    'air_date'], series_id=series_id, user_id=series.user_id)
        session.add(newEpisode)
        session.commit()
        print "Episode add Success"
        flash('New Episode %s Successfully Created' % (newEpisode.name))
        return redirect(url_for('showEpisodes', series_id=series_id))
    else:
        return render_template('newepisode.html', series=series)


# Edit an episode
@app.route('/series/<int:series_id>/episode/<int:episode_id>/edit', methods=[
    'GET', 'POST'])
def editEpisode(series_id, episode_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Episode).filter_by(id=episode_id).one()
    series = session.query(Series).filter_by(id=series_id).one()
    if login_session['user_id'] != series.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this series.Please create your own series in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        editedItem.name = request.form['name']
        editedItem.description = request.form['description']
        editedItem.air_date = request.form['air_date']
        session.add(editedItem)
        session.commit()
        print "Episode edit Success"
        flash('Episode Successfully Edited')
        return redirect(url_for('showEpisodes', series_id=series_id))
    else:
        return render_template(
            'editepisode.html', series=series, episode_id=episode_id, episode=editedItem)


# Delete an episode
@app.route('/series/<int:series_id>/episode/<int:episode_id>/delete', methods=[
    'GET', 'POST'])
def deleteEpisode(series_id, episode_id):
    if 'username' not in login_session:
        return redirect('/login')
    series = session.query(Series).filter_by(id=series_id).one()
    itemToDelete = session.query(Episode).filter_by(id=episode_id).one()
    if login_session['user_id'] != series.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this series.Please create your own series in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        print "Episode delete Success"
        flash('Episode Successfully Deleted')
        return redirect(url_for('showEpisodes', series_id=series_id))
    else:
        return render_template(
            'delepisode.html', episode=itemToDelete, series=series)


# CSS wasnt getting updated due to cache saved in browser
# This routing generates a random hash so that every time page is refreshed,
# the url for static files gets an added random variable and does not get
# affected by cache
# CREDITS - Ostrovski "https://gist.github.com/Ostrovski/f16779933ceee3a9d181"
@app.url_defaults
def hashed_url_for_static_file(endpoint, values):
    if 'static' == endpoint or endpoint.endswith('.static'):
        filename = values.get('filename')
        if filename:
            if '.' in endpoint:  # has higher priority
                blueprint = endpoint.rsplit('.', 1)[0]
            else:
                blueprint = request.blueprint  # can be None too

            if blueprint:
                static_folder = app.blueprints[blueprint].static_folder
            else:
                static_folder = app.static_folder

            param_name = 'h'
            while param_name in values:
                param_name = '_' + param_name
            values[param_name] = static_file_hash(
                os.path.join(static_folder, filename))


def static_file_hash(filename):
    return int(os.stat(filename).st_mtime)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
