import dash
from dash import html, Input, Output, dcc, callback
import dash_bootstrap_components as dbc

from components.Links import linkedin, github, wftda_sources


# --LOGIC FOR THE LAYOUT--

dash.register_page(
    __name__,
    path='/Resume',
    title='Resume',
    name='Resume'
)

summary = html.Div([
    html.H5("Summary"),
    html.P("Creative problem solver, scientist, and engineer with 10+ years of experience in research, development, and analysis of complex systems. Proficient at optimizing processes, extracting insights, and driving decision-making through data science and engineering expertise.")])

education = html.Div([
    html.H2("Education"),
    html.Ul([
        html.Li([
            html.Div([
                html.Span([
                    html.B("Doctor of Philosophy (Ph.D.)"),
                    ", Materials Science and Engineering — ",
                    html.I("University of Washington")
                ], className="d-inline-block"),
                html.Span(html.B("2019"), className="ms-auto fw-bold")
            ], className="d-flex justify-content-between")]),
        html.Li([
            html.Div([
                html.Span([
                    html.B("Master of Science (M.S.)"),
                    ", Materials Science and Engineering — ",
                    html.I("University of Washington")]),
                html.Span(html.B("2015"), className="ms-auto fw-bold")
            ], className="d-flex justify-content-between")]),
        html.Li([
            html.Div([
                html.Span([
                    html.B("Bachelor of Science (B.S.)"),
                    ", Materials Science and Engineering — ",
                    html.I("University of North Texas")]),
                html.Span(html.B("2012"), className="ms-auto fw-bold")
            ], className="d-flex justify-content-between")]),
        html.Li([
            html.Div([
                html.Span([
                    html.B("Certificate"),
                    ", Data Science — ",
                    html.I("Noble Desktop")]),
                html.Span(html.B("2024"), className="ms-auto fw-bold")
            ], className="d-flex justify-content-between")]),
        html.Li([
            html.Div([
                html.Span([
                    html.B("Certificate"),
                    ", Machine Learning — ",
                    html.I("Coursera")]),
                html.Span(html.B("2025"), className="ms-auto fw-bold")
            ], className="d-flex justify-content-between")]),
    ], className="list-unstyled")])

skills = html.Div([
    html.H2("Technical Skills"),
    html.Ul([
        html.Li([
            html.B("Data Science: "),
            "Data Exploration, Visualization & Dashboards (Matplotlib, Plotly, Seaborn, Dash, JMP)"]),
        html.Li([
            html.B("Machine Learning: "),
            "Supervised, Unsupervised; Model Prototyping, Training & Evaluation; Feature Engineering, Error Analysis"]),
        html.Li([
            html.B("Programming & Tools: "),
            "Python (Pandas, NumPy, Scikit-learn), SQL (PostgreSQL), Git, Jupyter, CoLab, VS Code"]),
        html.Li([
            html.B("Other Skills: "),
            "Project Management, Process Engineering, Test Design, Root Cause Analysis, Batteries, Electrochemistry, Spanish"])
        ], className="list-unstyled")])

# You can modularize each job like this
experience = html.Div([
    html.H2("Professional Experience"),
    dbc.Accordion([
        dbc.AccordionItem([
            html.P("Built Machine Learning models to identify key chemical phenomena, predict product quality, and optimize manufacturing using laboratory, production, and QC/QA data to maximize business impact and provide strategic insight."),
                html.Ul([
                    html.Li("Created pipelines for access, cleaning, and integration of data across R&D, Production, and QC/QA."),
                    html.Li("Developed characterization, test methods, and supporting software to mitigate identified production deficiencies."),
                    html.Li("Collaborated with operations, engineering, R&D and QC/QA to integrate insights into the next generation processes."),
                    ]),
            html.P("Managed interdisciplinary, cross-functional projects, prioritizing high-impact initiatives."),
                html.Ul([
                    html.Li("Built, debugged, and upgraded complex chemical reactors."),
                    ]),
                html.P("Advised the operations and engineering teams during commissioning as the onsite technical expert."),
            ], title="Research Engineer, Group14 Technologies (2023–2024)", item_id="item-1"),
        dbc.AccordionItem([
            html.P("Led science and engineering investigations across industries (forensics, energy storage, nuclear power plants, etc.)."),
            html.Ul([
                html.Li("Managed projects end-to-end: client scoping, budgeting, testing, analysis, reporting and non/technical presentations."),
                html.Li("Conducted research, testing, failure analysis, characterization, data collection & analysis, and findings reporting."),
                ])
            ], title="Materials Engineer, Jensen Hughes (2020–2023)", item_id="item-2"),
        dbc.AccordionItem([
            html.P("Optimized lab increasing testing throughput by 3× through data-informed equipment utilization strategies."),
            html.P("Conducted R&D on battery enclosures, thermal management, and advanced aerodynamic surfaces."),
            ], title="Materials Process & Physics Technical Analyst, Boeing (2019–2020)", item_id="item-3"),
        dbc.AccordionItem([
            html.P("Developed and executed simultaneous R&D projects; collected, reviewed and analyzed data to guide further research; published the findings."),
            html.P("Headed various aspects of laboratory and personnel management."),
            ], title="Graduate Research Assistant, UW (2012–2019)", item_id="item-4")
    ], start_collapsed=True, active_item="item-1", className="no-margin-p")])


other_experience = html.Div([
    html.H2("Additional Experience"),
    html.Ul([
        html.Li("Volunteer Data Scientist – Rat City Roller Derby (2013–2025)"),
        html.Li("Engineering Outreach Volunteer – UW (2013–2019)"),
        html.Li("Emergency Relief Volunteer – City of Warren, MI (2014)"),
        html.Li("Translator – Legal documents (2013)"),
        html.Li("Supplemental Instructor – UNT STEM subjects (2009–2011)")
    ])
])

layout = dbc.Container([
    summary,
    html.Hr(),
    education,
    html.Hr(),
    skills,
    html.Hr(),
    experience,
    html.Hr(),
    other_experience,
    ],  style={
        "maxWidth": "75%",
        "margin": "0 auto",
        "padding": "2rem"
        },
    fluid=False,
    className="pt-4")