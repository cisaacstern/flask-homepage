import albedo._albedo.dashlayout as dashlayout
#import _albedo.dashlayout
import panel as pn
from bokeh.io import curdoc
pn.extension()

dash = dashlayout.DashLayout()
#dash = _albedo.dashlayout.DashLayout()
board = dash.dashboard()
model = board.get_root()
curdoc().add_root(model)
curdoc().title = 'Albedo'
