import dash
from dash import Dash
from landing import create_layout
import Seattle

external_style = "assets/custom.css"

app = Dash (__name__, external_stylesheets = [external_style], use_pages=True, suppress_callback_exceptions=True)
app.layout = create_layout(app)
app.run_server(debug= True)