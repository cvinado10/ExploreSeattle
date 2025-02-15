# ExploreSeattle!  
A Data Analysis and Visualization Project  
  
  
Overview  
This is my practice project in which you can explore   Seattle and its neighborhoods. It uses Dash, Plotly, and GeoPandas to create interactive maps, graphs, and tables that allow users to filter and analyze data by neighborhood.  
-It uses data from the Seattle Data Project  
-It currently only has data from offense reports, but the goal is to add more databases  
  
  
Features  
Interactive map of Seattle's neighborhoods.  
Ability to select single/multiple neighborhoods to filter databases.  
Data visualization in different formats (tables, graphs).  
Semi-responsive design to ensure usability on different screen sizes.  
  
  
Project Structure  
sea_project/  
├── assets/  
│   └── bootstrap.css  
│   └── GitHubLogo.css  
│   └── LinkedInLogo.css  
├── components/  
│   ├── CrimeGraphs.py  
│   ├── CrimeTables.py  
│   ├── CrimeTablesData.py  
│   ├── Explore.py  
│   ├── Links.py  
│   ├── MapComponent.py  
│   ├── Menus.py  
│   └── SeattleMapStyle.py  
├── static/  
│   ├── Created/  
│   │   └── _#The application will create files here_  
│   ├── Data/  
│   │   └── crime.csv _#Data downloaded from Seattle Data Project on reported offenses_  
│   ├── Geo/  
│   │   └── Districts.geojson _#Data downloaded from Seattle Data Project on Seattle's Neighboorhoods_  
├── app.py  
├── CrimeDataProcessing.py  
├── layout.py  
├── Seattle.py  
├── requirements.txt  
└── README.md  
  
  
Installation  
Clone the repository  
Create a virtual environment and activate it  
Install the required packages (requirements.txt)  
Run the CrimeDataProcessing file to process the database and create the required sub files  
  
  
Run the application  
Run the app.py file to intialize the app  
Open your web browser and navigate to http://127.0.0.1:8050/ to view the application.  
Use the interactive map to select neighborhoods and filter offenses data.  
The current selection and filtered data will be displayed on the page.  
  
  
Code Explanation  
-app.py  
This file initializes the Dash application and sets up the layout using the create_layout function from layout.py.  
-layout.py  
This file defines the layout of the application, including the positioning of various components such as the map, graphs, and tables.  
-Seattle.py  
This file contains the logic for rendering the interactive map and handling user interactions. It uses Plotly to create the map and GeoPandas to handle geographic data.  
-CrimeGraphs.py, CrimeTables.py, and CrimeTablesData.py  
These files define the components for data handling and displaying offenses data in graph and table formats.  
-Explore.py, Links.py, MapComponent.py, Menus.py, and SeattleMapStyle.py  
These files define additional components and styles used in the application to simplify the layout.py page.  
  
  
Customization  
To customize the appearance of the application, modify the CSS files in the assets directory.  
To add or modify geographical data, update the GeoJSON file in the Geo directory and adjust the data processing logic in Seattle.py.  
To use an updated Offenses report, download a newer version from the Seattle Data project, and update csv file in the Data directory. Some adjustments to the data processing logic in CrimeDataProcessing.py might be required.  
  
  
Contributing  
Contributions are welcome! Please fork the repository and create a pull request with your changes.  
  
  
Feel free to reach out if you have any questions or need further assistance. Enjoy exploring Seattle's data!  
