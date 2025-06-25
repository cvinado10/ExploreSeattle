import dash
from dash import html, Input, Output, dcc, callback
import dash_bootstrap_components as dbc

from itertools import cycle


# --LOGIC FOR THE LANDING LAYOUT--

dash.register_page(__name__, path='/', name='Home', title='Carolina Vinado')



categories = {
    "Engineering": ["eng_1.jpg", "eng_2.jpg", "eng_3.jpg"],
    "Asimov": ["dog_1.jpg", "dog_2.jpg", "dog_3.jpg"],
    "Travel": ["travel_1.jpg", "travel_2.jpg"],
    "Fostering": ["foster_1.jpg", "foster_2.jpg", "foster_3.jpg"],
    "Food": ["food_1.jpg", "food_2.jpg", "food_3.jpg"],
    "Sports": ["sport_1.jpg", "sport_2.jpg", "sport_3.jpg"]
    }


layout = html.Div([
    html.Div([
        html.Div("Explore a Slice of My Interests", className="banner-text"),

        dcc.Interval(id="image-interval", interval=3000, n_intervals=0),

        html.Div([
        html.Div([
            html.Div(cat, className="img-label"),
            html.Img(id=f"img-{cat.lower()}", className="collage-img")
        ], className=f"collage-slot img{i+1}")
        for i, cat in enumerate(categories)
            ], className="collage-container")
        ], className="intro-section")

    ], className="p-4")


image_cycles = {cat: cycle(imgs) for cat, imgs in categories.items()}

# Callback factory to avoid closure issue
def create_image_callback(cat_name):
    def update_image(n):
        return f"/assets/{next(image_cycles[cat_name])}"
    return update_image

# Register callbacks
for cat in categories:
    callback(
        Output(f"img-{cat.lower()}", "src"),
        Input("image-interval", "n_intervals"),
        prevent_initial_call=False
    )(create_image_callback(cat))