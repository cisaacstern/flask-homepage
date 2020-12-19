from threading import Thread

from flask import Flask, render_template
from tornado.ioloop import IOLoop

from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.server.server import Server
from bokeh.themes import Theme

from bokeh.settings import settings

import albedo._albedo.dashlayout as dashlayout
import panel as pn
from bokeh.io import curdoc

app = Flask(__name__)
settings.resources = 'cdn'
settings.resources = 'inline'

@app.route('/about/')
def about_page():
    return render_template("about.html")

def bkapp(doc):

    dash = dashlayout.DashLayout()
    board = dash.dashboard()
    model = board.get_root()
    doc.add_root(model)

    doc.theme = Theme(filename="theme.yaml")

@app.route('/terrain-correction/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("terrain-correction.html", script=script, template="Flask")

def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': bkapp}, io_loop=IOLoop(), allow_websocket_origin=["127.0.0.1:8000"])
    server.start()
    server.io_loop.start()

Thread(target=bk_worker).start()

@app.route('/snow-surface-pde/')
def pde_page():
    return render_template("snow-surface-pde.html")

@app.route('/topo-gallery/')
def topo_page():
    return render_template("topo-gallery.html")


if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8000)