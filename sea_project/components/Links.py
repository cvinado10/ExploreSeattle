from dash import html, dcc


# --STYLING FOR THE LINKS--

# LinkedIn
linkedin = html.Div([
    html.A(
        html.Img(
            src = '/assets/LinkedInLogo.png',
            style = {'width': '65px', 'height': '65px'}
        ),
        href = 'https://www.linkedin.com/in/carolina-vinado/',
        target = '_blank'
        )
    ])

# GitHub
github = html.Div([
    html.A(
        html.Img(
            src = '/assets/GitHubLogo.png',
            style = {'width': '65px', 'height': '65px'}
        ),
        href = 'https://github.com/cvinado10/',
        target = '_blank'
        )
    ])

# Sources link
sdp_sources = html.Div([
    html.H6(['Data from the ',
        dcc.Link('Seattle Open Data Portal',
            href = 'https://data.seattle.gov/',
            target = '_blank'
            )
        ])
    ])

wftda_sources = html.Div([
    html.P(['Data for the model obtained from RCRD and ',
        dcc.Link('WFTDA',
            href = 'https://resources.wftda.org/competition/statsbook/',
            target = '_blank'
            )
        ])
    ])