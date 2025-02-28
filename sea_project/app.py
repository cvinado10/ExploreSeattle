from dash import Dash
from layout import create_layout
import Seattle

external_style = "assets/custom.css"

app = Dash (__name__, external_stylesheets = [external_style])
app.layout = create_layout(app)
app.run_server(debug= True)