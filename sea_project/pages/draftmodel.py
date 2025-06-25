import dash
from dash import html, Input, Output, dcc, callback
import dash_bootstrap_components as dbc


# --LOGIC FOR THE LAYOUT--

dash.register_page(
    __name__,
    path='/DraftModel',
    title='RCRD Draft Model',
    name='RCRD Draft Model'
)

heading = html.Div([
    html.H2('RCRD Draft Balancing Model'),
    html.Div('A Machine Learning Approach to Balancing Roller Derby Teams'),
    html.I(html.P(['Data for the model obtained from RCRD and ',
        dcc.Link('WFTDA', href = 'https://resources.wftda.org/competition/statsbook/', target = '_blank')], style={'marginBottom': '0'})),
    html.Div('June 2025', className='text-secondary', style={'marginTop': '0'})
    ], className = 'mb-4')


video = html.Div([
    html.Iframe(
        src="https://www.youtube.com/embed/OId6gTd2LCM?list=PLgt96IetJvxItxb-jrDjDb6r_DQKgQ70l",
        style={"width": "80%", "aspectRatio": '1.77', "border": "none"},
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
        title="Roller Derby 101: Gameplay"
        )
    ], className="d-flex justify-content-center")
    
cap0 = html.Div('Intro to Roller Derby', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

background = dbc.Row([
    html.Div([
        html.H3("Background"),
        html.P([
            html.A("Rat City Roller Derby", href="https://ratcityrollerderby.com", target="_blank"),
            " (RCRD) is a roller derby league in Seattle. It is comprised of travel teams, four home teams, a recreational team, and cohorts of skaters being developed through training bootcamps. Incoming and upcoming skaters that wish to participate in the home teams are distributed among the four home teams at semi-regularly scheduled drafts."
            ]),
        html.P(["Every season each home team plays each other once, and sometimes against visiting teams. At the end of the season, the top two teams (by W/L record and point differential as tie breaker) play a game for the RCRD Champion title. If teams are too mismatched in terms of skill or abilities, the games are not close, resulting in loss of engagement from both the audience and the team's skaters if the mismatch is persistent over the seasons."
            ]),
        html.P(["Please note that due to privacy, only snippets of the code and publicly available data will be shared. The code shared on ",
            html.A("GitHub", href="https://github.com/YOUR_REPO_HERE", target="_blank"),
            " has been cleaned of identifiable information, and parts might not run."
            ], className="text-muted fst-italic"),
        html.P(["For an introduction to roller derby, and how it is played, feel free to watch the video below from the ",
            html.A("Women's Flat Track Derby Association", href="https://wftda.org/", target="_blank"),
            " (WFTDA), the sport's governing body."
            ]),
        video,
        cap0,
        ], className="mt-0 mb-4 d-flex flex-column")
    ], align="center", className="mb-2")


goal = dbc.Row([
    html.Div([
        html.H3("Goal"),
        html.P(["The goal for this project is to distribute the draft eligible skaters into the four home teams, in such way that the teams are as balanced as possible."]),
    ], className="mb-4 d-flex flex-column")
    ], align="center", className="mb-2")


tools = dbc.Row([
    html.Div([
        html.H3("Tools"),
        html.P("This project was built using a wide range of Python tools, including:"),
        html.Ul([
            html.Li([
                html.B("Jupyter Notebooks"),
                ": for prototyping and iterative exploration"
                ]),
            html.Li([
                html.B("Pandas"), ", ",
                html.B("NumPy"),
                ": for data wrangling and numerical operations"
                ]),
            html.Li([
                html.B("Levenshtein"), " and ",
                html.B("rapidfuzz"),
                ": for fuzzy string matching and similarity scoring"
                ]),
            html.Li([
                html.B("Matplotlib"), ", ",
                html.B("Plotly"), ", and ",
                html.B("Seaborn"),
                ": to cover everything from quick plots to interactive visualizations"
                ]),
            html.Li([
                html.B("Core Python utilities"),
                " like ", html.Code("itertools"), ", ",
                html.Code("datetime"), ", and ",
                html.Code("collections.defaultdict"),
                ": small, powerful workhorses that made a big difference"
                ]),
            html.Li([
                "And what felt like the entire ",
                html.B("scikit-learn library"),
                ", although realistically, I only scratched the surface"
                ])
            ]),
        ], className="mb-4 d-flex flex-column")
    ], align="center", className="mb-2")


challenges = dbc.Row([
    html.Div([
        html.H3("Challenges"),
        html.P([
            "Some challenges were easily foreseeable, such as how do we define and quantify ",
            html.B("'balanced'"),
            "; others came along the way. Below is a non-comprehensive list of challenges that had to be addressed. I tend to work problems backwards — first determining the end goal, then working back toward what would be needed to achieve it. The list therefore reads in reverse order, to walk you through how I arrived at each requirement/stage of the project, but though the article is written in the forward sequence to walk along the actual implementation."]),
        html.Ul([
            html.Li([
                html.B("Defining and scoping the goal/metrics of improvement"),
                html.Ul([
                    html.Li(["Since the goal is to balance teams, we needed to define and quantify balance. ",
                        "Many factors go into defining a team, so choosing and quantifying which ones to balance was the first step. ",
                        "Through conversations with the league, ",
                        html.B("body count"),
                        " and ",
                        html.B("team strength"),
                        " were chosen as equally high priorities."]),
                    html.Li("The metrics for improvement were a reduction in variance among the four home teams in both body count and team strength.")])]),
            html.Li([
                html.B("Determining team strength"),
                html.Ul([
                    html.Li("Team strength was defined as the average skater strength (or 'rank') of all active skaters in a team. Position was determined but not considered in this iteration."),
                    html.Li("Team strength was associated with aggregated skater data rather than team data, allowing flexibility and responsiveness to roster changes.")])]),
            html.Li([
                html.B("Determining skater rank"),
                html.Ul([
                    html.Li("Assigning rank is contentious when metrics aren't empirically quantifiable or easily standardized."),
                    html.Li("Due to this, I proposed a model-driven approach using machine learning to assign skater value in a more objective way.")])]),
            html.Li([
                html.B("Reconciling skater stats with rosters"),
                html.Ul([
                    html.Li("As part of the derby culture, skaters often use pseudonyms which may change over time or to fit the 'theme' of certain games."),
                    html.Li("Game stats are manually recorded, increasing the risk of typos, inconsistencies, or the use of shorthand."),
                    html.Li("A method was needed to track name changes and reliably link skater identities across data sources.")])]),
            html.Li([
                html.B("Model training"),
                html.Ul([
                    html.Li("Limited data is available due to the infrequency of RCRD games, making training on a small dataset a challenge.")])]),
            html.Li([
                html.B("Choosing and evaluating a model"),
                html.Ul([
                    html.Li("With little to no prior ML literature on roller derby, model selection and validation had to be developed from scratch.")])]),
            html.Li([
                html.B("Compiling in-house and public data"),
                html.Ul([
                    html.Li("Although WFTDA provides a standard format, data is not consistently structured or collected."),
                    html.Li("Code had to handle formatting inconsistencies, data entry errors, and other idiosyncrasies.")
                    ])]),
            html.Li([
                html.B("Making the model accessible"),
                html.Ul([
                    html.Li("The tool needs to run independently of my own machine."),
                    html.Li("It must be documented well enough for league members with minimal coding experience to update (stats, rosters) and maintain it.")])])])
        ], className="mb-4 d-flex flex-column")
    ], align="center", className="mb-2")


implementation = dbc.Row([
    html.Div([
        html.H3("Implementation"),
        ], className="d-flex flex-column")
    ], align="center", className="mb-2")

img1 = html.Div([
        html.Img(
            src = '/assets/1_folder.png',
            style = {'width': '30%', 'height': 'auto'})
    ], className="d-flex justify-content-center")

cap1 = html.Div('Tabs within WFTDA formatted spreadsheet for a game', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

img2 = html.Div([
        html.Img(
            src = '/assets/2_tab.png',
            style = {'width': '100%', 'height': 'auto', 'max-width': '800px'},
            className="bg-light")
    ], className="d-flex justify-content-center")

cap2 = html.Div("'Game Summary' tab structure and content", className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

img3 = html.Div([
        html.Img(
            src = '/assets/3_parse.png',
            style = {'width': '100%', 'height': 'auto', 'max-width': '800px'})
    ], className="d-flex justify-content-center")

cap3 = html.Div('Code to parse spreadsheet data', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

compile = dbc.Row([
    html.Div([
        html.H4("Compiling Data"),
        html.P(["Several data streams were tapped into for this project. Details as follows."]),
        html.H5("WFTDA Data"),
        html.P(["Due to limited RCRD data, I trained the model using data from ",
                html.A("WFTDA's repository", href="https://resources.wftda.org/competition/statsbook/", target="_blank"),
                ". WFTDA has made publicly available game data from 2023 onward, covering approximately 2,200 games up to June 2025 (when data for the model was last updated). About 50 files were excluded from the dataset due to formatting issues, incomplete data, or inconsistencies. Each game file contains extensive information spread across 22 tabs."]),
        img1,
        cap1,
        html.P(["For this draft model, I focused solely on the tab labeled ",
                html.B("'Game Summary'"),
                "."]),
        img2,
        cap2,
        html.P(["As the name indicates, it offers a high-level view: which skaters participated for each team, how often they played each position, points scored and conceded, and more."]),
        html.P(["The folder containing these files was looped through during parsing. Each skater's stats were extracted into a row in the resulting DataFrame. Additional columns were added to capture the skater's team, the game date, the game outcome (win = 1, tie = 0.5, loss = 0), and the source file."]),
        img3,
        cap3,
        html.P(["Since all statistical columns were already numeric, no one-hot encoding was required. Feature engineering was kept to a minimum to suit the model's purpose."]),
        html.H5("RCRD Data"),
        html.H6("Game Stats"),
        html.P(["RCRD specific game stats were processed in the same way as the WFTDA data. Currently, 57 games, across Home, Travel, and Recreational contexts, are included. The intent was to capture skater performance across a wide range of scenarios. Due to the inherently collaborative nature of roller derby, few statistics can be considered purely individual. Even penalties, which are served individually, may be attributed based on proximity, team role (e.g., captain), or perceived opportunity to prevent the infraction when multiple skaters are involved. Incorporating data from diverse game contexts, rather than limiting ourselves to home games, helps better approximate a skater's individual skill, and mitigates the bias of team usage patterns. For instance, a veteran skater frequently sent out with a less experienced lineup might otherwise appear to underperform. Including broader game data also strengthens the model's resilience to changes in leadership, strategy, or team composition."]),
        html.H6("Rosters"),
        html.P(["RCRD maintains an internal league directory which includes skater names, current teams, and status (e.g., active, leave of absence, retired). This directory was used to link skaters to their current team context and filter out non-active participants."]),
        html.H6("Draftees and Returnees"),
        html.P(["RCRD also provided a spreadsheet of draftees and returnees, including an estimated rank assigned by the training department in collaboration with the draft committee. Since many incoming and returning skaters have limited or no game data, these ranks (scaled between 0 and 1) are used to seed them into the model."]),
        ], className="mb-4 d-flex flex-column")
    ], align="center", className="mb-2")


img4 = html.Div([
        html.Img(
            src = '/assets/4_trymodel.png',
            style = {'width': '100%', 'height': 'auto', 'max-width': '800px'})
    ], className="d-flex justify-content-center")

cap4 = html.Div('Loop to prescreen all estimators in the scikit-learn library', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

img5 = html.Div([
        html.Img(
            src = '/assets/5_modeleval.png',
            style = {'width': '90%', 'height': 'auto', 'max-width': '720px'})
    ], className="d-flex justify-content-center")

cap5 = html.Div("Output of the estimator evaluation loop", className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

img6 = html.Div([
        html.Img(
            src = '/assets/6_RFE.png',
            style = {'width': '60%', 'height': 'auto', 'max-width': '480px'})
    ], className="d-flex justify-content-center")

cap6 = html.Div('Output of the Recursive Feature Elimination test', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

img7 = html.Div([
        html.Img(
            src = '/assets/7_HGBC.png',
            style = {'width': '60%', 'height': 'auto', 'max-width': '480px'})
    ], className="d-flex justify-content-center")

cap7 = html.Div("Output of HGBC's features by importance after training the model on the full dataset", className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

img8 = html.Div([
        html.Img(
            src = '/assets/8_modelevaler.png',
            style = {'width': '100%', 'height': 'auto', 'max-width': '800px'})
    ], className="d-flex justify-content-center")

cap8 = html.Div("Code and results of the model evaluation", className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

img9 = html.Div([
        html.Img(
            src = '/assets/9_modelmetrics.png',
            style = {'width': '60%', 'height': 'auto', 'max-width': '480px'},
            className= "bg-light")
    ], className="d-flex justify-content-center")

cap9 = html.Div('Summary of the model evaluation', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

img10 = html.Div([
        html.Img(
            src = '/assets/10_LC.png',
            style = {'width': '60%', 'height': 'auto', 'max-width': '480px'})
    ], className="d-flex justify-content-center")

cap10 = html.Div('Learning Curve for HGBC', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

model = dbc.Row([
    html.Div([
        html.H4("Model Selection, Evaluation and Training"),
        html.P([
            "As mentioned earlier, a win/loss outcome column (",
            html.Code("['WIN']"),
            ") was added to the WFTDA DataFrame. To quickly evaluate potential models, all estimators available in ",
            html.Code("scikit-learn"),
            " were looped through using a ",
            html.Code("StratifiedShuffleSplit"),
            " on a sample subset of approximately 10% of the full dataset (nearly 57,000 rows), with just ",
            html.Strong("2 cross-validation folds"),
            ". This approach provided a rapid yet informative prescreening of model performance."
            ]),
        img4,
        cap4,
        html.P("Estimators that required NaN values to be imputed were skipped. This decision was based on the nature of the data: for example, skaters who exclusively played as Blockers would naturally have empty columns for Jammer-specific stats. Imputing values in these cases would have been both illogical and misleading."),
        html.P(["For meta-estimators requiring a base estimator, ",
            html.Code("RandomForestClassifier"),
            " was used, since it was broadly compatible with many models and had performed best in the round without meta-estimators. Tied values were rounded to integers to enable classifier evaluation during prescreening."
            ]),
        html.P("Of the 145 estimators available in scikit-learn, 72 worked without requiring imputation. From these, only 19 ran successfully through the evaluation loop without errors."),
        img5,
        cap5,
        html.P("As expected, classification models outperformed others for this binary win/loss task. The five best-performing estimators were selected for a more thorough evaluation using the full dataset, with a 0.2 train/test split and 5-fold cross-validation."),
        html.P(["To narrow down input variables, ",
            html.B("Recursive Feature Elimination (RFE)"),
            " was performed. It identified the optimal features as: ",
            html.Code("'TOTAL +/-'"), ", ",
            html.Code("'AVG +/-'"), ", ",
            html.Code("'VTAR TOTAL +/-'"), ", and ",
            html.Code("'TOTAL VTAR AVG +/-'"),
            "."]),
        img6,
        cap6,
        html.P(["This aligned well with the top features identified by the ",
            html.Code("HistGradientBoostingClassifier (HGBC)"),
            ", and so only those columns were retained for final training."
            ]),
        img7,
        cap7,
        html.P("The top models all performed comparably during final evaluation."),
        img8,
        cap8,
        html.P("Ultimately, HGBC was selected because it slightly outperformed the others across most metrics."),
        img9,
        cap9,
        html.P("As a final check, the effect of dataset size on model performance was examined. A learning curve was plotted, which showed diminishing returns: adding more data would not significantly improve model accuracy."),
        img10,
        cap10,
        html.P("At that point, the chosen model's output, interpreted as the probability that a skater's stats contributed to a win, was ready to be used in the next stage of the project.")
        ], className="mb-4 d-flex flex-column")
    ], align="center", className="mb-2")


img11 = html.Div([
        html.Img(
            src = '/assets/11_matching.png',
            style = {'width': '100%', 'height': 'auto', 'max-width': '800px'})
    ], className="d-flex justify-content-center")

cap11 = html.Div('Loop to match skater names on game stats to those on the directory', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

img12 = html.Div([
        html.Img(
            src = '/assets/12_filter.png',
            style = {'width': '100%', 'height': 'auto', 'max-width': '800px'})
    ], className="d-flex justify-content-center")

cap12 = html.Div("Known name mismatches and match filtering", className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

reconcile = dbc.Row([
    html.Div([
        html.H4("Reconciling Skater Names"),
        html.P([
            "In roller derby culture, skaters often use pseudonyms rather than their legal names. These pseudonyms are frequently puns, themed for specific games, or updated to better reflect the skater's evolving identity. Furthermore, game statistics are collected manually, which opens the door to human error: typos, abbreviations, or inconsistencies in how names are recorded."
            ]),
        html.P(["To manage name changes over time, a renaming dictionary was developed. When the RCRD game data is loaded, this dictionary is applied to ",
            html.Code("['Skater']"),
            ". Through filtering by team names, a new column is also added to indicate whether the team is an RCRD team or a visiting team."
            ]),
        html.P(["To correct for typos and other inconsistencies, a custom matching function compares skater names in the game data with those in the league directory. The function evaluates possible matches using a scoring system across multiple string similarity metrics. At the end of the process, the highest scoring match is selected."
            ]),
        html.P(["The matching process begins with direct string equality. If no exact match is found, the system applies a series of increasingly flexible checks: ",
            html.Code("Levenshtein ratio"),
            " for minor typos (e.g., ",
            html.I("Lily"),
            " vs ",
            html.I("Lilly"),
            "), ",
            html.Code("partial ratio"),
            " for shorthand (e.g., ",
            html.I("Blaze"),
            " vs ",
            html.I("Blaze of Lori"),
            "), and finally ",
            html.Code("fuzzy ratio"),
            " for more complex mismatches or renames (e.g., ",
            html.I("Anasinn Skywalker"),
            " vs ",
            html.I("Sinnamon Slam"),
            ")."
            ]),
        img11,
        cap11,
        html.P(["If at the end of the first loop, a match scores less than 100, both the game stat name and the directory name are 'cleaned' by stripping down to lowercase alphabetic characters only, and the matching loop is repeated. After all comparisons are complete, several columns are added to the game DataFrame: the best-matching directory name, the matching score, the associated team, and the skater's current status."
            ]),
        html.P(["Additional logic is applied to minimize false positives. For instance, if the skater is on an ",
            html.B("RCRD team"),
            ", the score threshold is relaxed to 80. If they are not, it remains at 100, this is to acknowledging that some skaters may compete for multiple leagues. A curated list of known mismatches was also introduced to catch any cases that slipped through the filters. At the end of the process, we are left with a DataFrame where each skater entry from game stats is matched to a unique game in the directory, along with their current team and status, ready for the next step."
            ]),
        img12,
        cap12,
        ], className="mb-4 d-flex flex-column")], align="center", className="mb-2")

img13 = html.Div([
        html.Img(
            src = '/assets/13_seasoning.png',
            style = {'width': '60%', 'height': 'auto', 'max-width': '520px'})
    ], className="d-flex justify-content-center")

cap13 = html.Div('Function to aggregate and add features to the skater data', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

img14 = html.Div([
        html.Img(
            src = '/assets/14_skagg.png',
            style = {'width': '80%', 'height': 'auto', 'max-width': '640px'})
    ], className="d-flex justify-content-center")

cap14 = html.Div('Function to aggregate and add features to the skater data', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

skater = dbc.Row([
    html.Div([
        html.H4("Determining Skater Rank"),
        html.P(["Once the RCRD data had been parsed, the names reconciled, and game statistics linked to individual skaters in the league directory, the dataset was ready to have the model applied to it. Logic was added to allow for the application of any or all of the trained models, with ",
            html.Code("['Rank']"),
            " being their collective average."
            ]),
        img13,
        cap13,
        html.P(["Afterward, skater game data was aggregated at the skater level. Most statistical columns were summarized using the ",
            html.B("median"),
            ", providing resilience against outliers, such as skaters underperforming in casual games or overperforming during one-sided matchups."
            ]),
        html.P(["However, columns representing the ",
            html.B("number of times a skater played each position"),
            " were aggregated using the ",
            html.B("mean"),
            ". This allowed the model to estimate which position a skater plays most frequently, offering insight into their role on the team."
            ]),
        img14,
        cap14,
        ], className="mb-4 d-flex flex-column")], align="center", className="mb-2") 
        
        
img15 = html.Div([
    html.Img(
        src = '/assets/15_teamcomp.png',
        style = {'width': '100%', 'height': 'auto', 'max-width': '800px'})
], className="d-flex justify-content-center")

cap15 = html.Div('Function to analyze team composition', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')
        
img16 = html.Div([
    html.Img(
        src = '/assets/16_teamagg.png',
        style = {'width': '100%', 'height': 'auto', 'max-width': '800px'})
], className="d-flex justify-content-center")

cap16 = html.Div('Function to aggregate skaters into teams', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

team = dbc.Row([
    html.Div([
        html.H4("Determining Team Strength"),
        html.P([
            "To understand team composition more clearly, a ",
            html.B("nested dictionary"),
            " was built to count the number of skaters at each rank level and position per team. This helped identify imbalances such as a shortage of high-level jammers or a surplus of low-level blockers. While insightful, skaters' position and level information is not currently being used for draft balancing. Instead, it is a tool for understanding team composition and identifying potential areas for improvement."
            ]),
        img15,
        cap15,
        html.P([
            "As previously noted, ",
            html.B("team strength"),
            " was defined as the ",
            html.B("mean rank of all active skaters"),
            " on a given team. The average was chosen to reflect the contributions of all skaters in the team. ",
            html.Code("['Active']"),
            " was aggregated by addition to have a count of active skaters per team. Additionally, returning skaters (those rejoining from leave or injury) were appended to the teams at this point using the supplemental ",
            html.I("retunees"),
            " spreadsheet mentioned above, to ensure the team representation was current and complete."
            ]),
        img16,
        cap16,
        ], className="mb-4 d-flex flex-column")], align="center", className="mb-2")
 
        
img17 = html.Div([
    html.Img(
        src = '/assets/17_balancing.png',
        style = {'width': '100%', 'height': 'auto', 'max-width': '800px'})
], className="d-flex justify-content-center")

cap17 = html.Div('Function to distribute draftees', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')
        
img18 = html.Div([
    html.Img(
        src = '/assets/18_bot.png',
        style = {'width': '50%', 'height': 'auto', 'max-width': '400px'})
], className="d-flex justify-content-center")

cap18 = html.Div('Plot of balance over iterations', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

draftees = dbc.Row([
    html.Div([
        html.H4("Distributing Draftees"),
        html.P(["To distribute incoming draftees across teams in a balanced way, an ",
            html.B("iterative optimization loop"),
            " was implemented. Since the league identified ",
            html.B("team strength"),
            " and ",
            html.B("body count"),
            " as equally important, both metrics were weighted equally during the balancing process."
            ]),
        html.P(["The function begins by assigning draftees to teams and updating each team's average rank. Then, using a series of ",
            html.B("pairwise team comparisons"),
            ", it attempts to move each draftee between teams. If the move reduces the differences in team strength or body count, the change is kept. Otherwise, the move is reverted. This process is repeated across ",
            html.B("all possible team combinations for 1000 iterations"),
            " to find a near-optimal distribution."
            ]),
        img17,
        cap17,
        html.P(["A real-time ",
            html.B("imbalance plot"),
            " is generated to monitor the optimization progress. Once the loop completes, the final draftee assignments and their new teams are printed."
            ]),
        img18,
        cap18,
        ], className="mb-4 d-flex flex-column")], align="center", className="mb-2")


img19 = html.Div([
    html.Img(
        src = '/assets/19_mt.png',
        style = {'width': '100%', 'height': 'auto', 'max-width': '800px'})
], className="d-flex justify-content-center")

cap19 = html.Div('Function to calculate before-and-after metrics', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')
        
img20 = html.Div([
    html.Img(
        src = '/assets/20_mb.png',
        style = {'width': '100%', 'height': 'auto', 'max-width': '800px'})
], className="d-flex justify-content-center")

cap20 = html.Div('Function and bar plot of before-and-after metrics', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')

img21 = html.Div([
    html.Img(
        src = '/assets/21_mv.png',
        style = {'width': '100%', 'height': 'auto', 'max-width': '800px'})
], className="d-flex justify-content-center")

cap21 = html.Div('Function and box plot of before-and-after metrics', className = 'mb-4 d-flex justify-content-center text-secondary fst-italic')
        
metrics = dbc.Row([
    html.Div([
        html.H4("Metrics of Improvement"),
        html.P(["To verify the effectiveness of the draftee placement, several summary statistics and visualizations are generated to measure improvement in the two target metrics: ",
            html.B("team strength"),
            " and ",
            html.B("body count"),
            "."
            ]),
        html.P([
            "The results are displayed in three formats for easier interpretation:"
            ]),
        html.Ul([
            html.Li([
                html.B("Text summary"),
                ": Describes before-and-after draft metrics."
                ]),
            img19,
            cap19,
            html.Li([
                html.B("Bar plot"),
                ": Allows for easier metric visualization."
                ]),
            img20,
            cap20,
            html.Li([
                html.B("Box plot"),
                ": Visualizes the variance in individual skater rank per team as well as the variance in body count among teams (though this would traditionally be represented as a bar chart) before-and-after draft."
                ]),
            img21,
            cap21
            ])
    ], className="mb-4 d-flex flex-column")], align="center", className="mb-2")
        
        
accessibility = dbc.Row([
    html.Div([
        html.H4("Accessibility"),
        html.P([
            "In order for the league to actively use and benefit from this tool, several steps were taken to ensure the project is accessible and sustainable. Some of the more labor-intensive features are awaiting final approval from the league before full implementation."
        ]),
        html.H5("Location"),
        html.P([
            "The project was moved to the league’s ",
            html.B("Google Drive"),
            " and adapted to run seamlessly within ",
            html.B("Google Colab"),
            ". This ensures the code is accessible from multiple devices without local setup."
        ]),
        html.H5("Documentation"),
        html.P(["While the code is well-structured and commented, an ",
            html.B("instruction manual"),
            " will be created to guide users with limited coding experience through setup, usage, and updates."
        ]),
        html.H5("Updating"),
        html.P(["The code is configured to read from specific folders. As long as the ",
            html.B("folder structure is maintained"),
            ", updating the data (e.g., WFTDA stats, RCRD stats, rosters, or draftee files) is simply a matter of placing new files in the appropriate directory before executing the relevant script."
        ]),
    ], className="mb-4 d-flex flex-column")], align="center", className="mb-2")
        
future = dbc.Row([
    html.Div([
        html.H3("Options for Change & Improvement"),
        html.H4("Account for Position"),
        html.P(["Currently, the model balances teams using only ",
            html.B("team strength"),
            " and ",
            html.B("body count"),
            ". A meaningful enhancement would be to factor in ",
            html.B("player position"),
            " as a balancing criterion. To implement this, it would require assigning a weight to position, adjustable relative to existing priorities, and doing minor modifications the distribution function accordingly."
        ]),
        html.H4("Maintenance & Customization"),
        html.P(["Skater rank is currently calculated based on stats from the ",
            html.B("last two seasons"),
            ". Filters for this are embedded directly in the code. Additionally, name-matching logic and renaming dictionaries are scattered throughout the file. Moving these components to the top of the script or separating them into a configuration section would improve ",
            html.B("maintainability and adaptability"),
            " as league needs evolve."
        ])
    ], className="mb-4 d-flex flex-column")], align="center", className="mb-2")
        
        
layout = dbc.Container([
    heading,
    background,
    goal,
    tools,
    challenges,
    implementation,
    compile,
    model,
    reconcile,
    skater,
    team,
    draftees,
    metrics,
    accessibility,
    future
    ],  style={
        "maxWidth": "50%",
        "margin": "0 auto",
        "padding": "2rem"
        },
    fluid=False,
    className="pt-4")