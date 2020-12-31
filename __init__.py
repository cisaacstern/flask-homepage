from threading import Thread

from flask import Flask, render_template, redirect
from tornado.ioloop import IOLoop

from bokeh.embed import server_document
from bokeh.server.server import Server
from bokeh.themes import Theme

from bokeh.settings import settings

import homepage.albedo._albedo.dashlayout as dashlayout
import panel as pn
from bokeh.io import curdoc

app = Flask(__name__)
settings.resources = 'cdn'
settings.resources = 'inline'

@app.route('/')
def hello():
    return redirect('/about/')

@app.route('/about/')
def about_page():
    return render_template("about.html")

@app.route('/projects/')
def projects_page():
    return render_template("projects.html")

def bkapp(doc):

    dash = dashlayout.DashLayout()
    board = dash.dashboard()
    model = board.get_root()
    doc.add_root(model)

    doc.theme = Theme(filename="homepage/theme.yaml")

@app.route('/projects/terrain-correction/', methods=['GET'])
def bkapp_page():
    script = server_document('http://192.168.99.103:5006/bkapp')
    return render_template("terrain-correction.html", script=script, template="Flask")

def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': bkapp}, io_loop=IOLoop(), allow_websocket_origin=["192.168.99.103:5000"])
    server.start()
    server.io_loop.start()

Thread(target=bk_worker).start()

@app.route('/projects/snow-surface-pde/')
def pde_page():
    return render_template("snow-surface-pde.html")

@app.route('/map/')
def map_page():
    return render_template("map.html")

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=5000)