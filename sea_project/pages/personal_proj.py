import dash
from dash import html, Input, Output, dcc, callback
import dash_bootstrap_components as dbc
from itertools import cycle



# --LOGIC FOR THE LANDING LAYOUT--

dash.register_page(
    __name__,
    path='/PersonalProjects',
    title='Personal Projects',
    name='Personal Projects'
    )

def centered_img(path):
    return html.Div(
        html.Img(src=path, className="project-img"),
        style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "height": "100%"
        }
    )


def create_project_card(title, background, goal, challenges, implementation, img_prefix):
    return dbc.Card(
        dbc.CardBody([
            html.H4(title, className="card-title"),
            html.Div([
                html.H6("Background"),
                html.P(background),
                html.H6("Goal"),
                html.P(goal),
                html.H6("Challenges"),
                html.P(challenges),
                html.H6("Implementation"),
                html.P(implementation),
            ]),
            dbc.Row([
                dbc.Col(centered_img(f"/assets/{img_prefix}1.jpg"), width=4),
                dbc.Col(centered_img(f"/assets/{img_prefix}2.jpg"), width=4),
                dbc.Col(centered_img(f"/assets/{img_prefix}3.jpg"), width=4),
            ], className="mt-3")
        ]),
        className="mb-4 p-3 shadow-sm"
    )

layout = html.Div([
    html.H2("Personal Projects", className="text-center my-4"),
    
    create_project_card(
        "Grade Patio",
        "The patio had poor drainage and was sloped toward the house, causing water pooling and raising concerns about the foundation.",
        "Regrade the yard to slope away from the house, improving drainage and preparing the space for future outdoor projects.",
        "Maintaining a consistent slope without heavy equipment, working around retaining walls and storm drains, and preserving existing landscaping.",
        "Used a laser level and string lines to establish grade, compacted gravel and sand layers, then placed pavers and transplanted plants. Built tree boxes for trees above the new grade.",
        "patio"
    ),

    create_project_card(
        "Design and Build a Pergola",
        "The patio lacked shade, making it less inviting for daytime use.",
        "Construct a pergola that provides shade, defines the outdoor space, and complements the house's design.",
        "Anchoring posts securely without damaging underground utilities and navigating complex angled cuts for a clean aesthetic. Angle of the corner of interest was 110 degrees, outside of standard pergonal kits.",
        "Designed a simple yet elegant structure leveraging commercially available parts as much as possible, sourced cut and treated cedar wood, and sunk piers for durability.",
        "pergola"
    ),

    create_project_card(
        "Build a Gate",
        "A structurally unsound section of fence needed replacement for privacy and pet containment. Adding a gate would improve side yard access and usability.",
        "Build a secure, weather-resistant gate that matches the existing fence and enhances functionality.",
        "Keeping the gate square over time while accommodating grade variations. Designing a latch system that’s secure, low-profile, and easy to operate.",
        "Sourced cut and treated cedar wood to build the wooden frame, sunk posts, added slats, gate, and a latch system with padlock compatibility, and pavers for access.",
        "gate"
    ),

    create_project_card(
        "Build a Murphy Bed",
        "A guest room also served as an office, but needed a more flexible layout. With visiting family from overseas, a sofa bed wasn't comfortable for extended stays.",
        "Design a Murphy bed that folds away when not in use, with custom cabinetry that offers storage for both guests and everyday office use.",
        "Sourcing reliable hardware, aligning the frame and cabinetry precisely, and preserving room functionality—ensuring access to the closet, window, lighting, and outlets while maintaining walkability when open.",
        "Used a commercial Murphy bed kit for the folding frame, anchored the structure to wall studs, and sourced, cut and treated wood to built integrated cabinetry to house the bed and provide organized storage. Made jig to speed up and sta Added design elements such as veneer for a more finished look.",
        "murphy"
    ),

    create_project_card(
        "Dog Stairs with Storage",
        "Asimov, our small aging dog, struggled to access high furniture, and the bedroom area lacked sufficient storage.",
        "Create dog-friendly stairs that double as storage for pet supplies and household items.",
        "Balancing stair tread height for comfort and integrating hidden storage compartments without compromising usability. Adding illumination for nighttime use.",
        "Designed modular stairs using commercially available parts where possible. Built push-to-open drawers with thin plywood, added foam and fabric for non-slip treads, and installed remote-controlled LED lighting.",
        "dogstairs"
    ),

    create_project_card(
        "Main Closet Build & Organize",
        "The main bedroom closet had inefficient wire shelving and poor organization. The space outside the closet was underutilized, with a dresser partially blocking balcony access.",
        "Maximize storage space with a custom-built system tailored to specific clothing and storage needs.",
        "Navigating tight clearances, maintaining access to HVAC, outlets, and windows, and integrating both closet and external storage into a cohesive design.",
        "Measured and modeled the layout, modified a commercial corner unit to fit the adjacent space—including a custom folding door to clear dresser handles. Demoed the existing closet interior, installed custom wooden shelving, and added dressers and continuous hanging rods for optimized storage.",
        "closet"
    )
])
