from openbb_terminal import api as openbb

import dash
from dash.dependencies import Input, Output

from dash import dcc, html
import dash_admin_components as dac
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate

import inspect
print(inspect.signature(openbb.stocks.search).parameters)
for item in inspect.signature(openbb.stocks.search).parameters:
        print(inspect.signature(openbb.stocks.search).parameters[item], item)
# =============================================================================
# Dash App and Flask Server
# =============================================================================
app = dash.Dash(__name__)
server = app.server 

# =============================================================================
# Dash Admin Components
# =============================================================================
# Navbar
navbar = dac.Navbar(color = "white") 

SIDEBAR_DATA_LEVEL = [
        ("Stocks", 0),
              ("Search", 1),
              ("Load", 1),
              ("Candle", 1),
              ("Quote", 1),
              ("News", 1),
              ("Codes", 1),
              ("Discovery", 2),
                      ("Pipo", 3),
                      ("Fipo", 3),
                      ("Gainers", 3),
                      ("Losers", 3),
                      ("Ugs", 3),
                      ("Gtech", 3),
                      ("Active", 3),
                      ("Ulc", 3),
                      ("Asc", 3),
                      ("Ford", 3),
                      ("Arkord", 3),
                      ("Upcoming", 3),
                      ("Cnews", 3),
                      ("Trending", 3),
                      ("Lowfloat", 3),
                      ("Hotpenny", 3),
                      ("Fds", 3),
                      ("Rtat", 3),
                      ("Divcal", 3),
                      ("Cramer", 3),
              ("Sector/Industry Analysis", 1),
        ("Cryptocurrency", 0),
        ("Economy", 0),
        ("Etf", 0),
        ("Funds", 0),
        ("Portfolio", 0),
        ("Forex", 0),
        ("Alternative", 0),
        ("Econometrics", 0),
        ]

'''
def levels(l, depth = -1):
    if not isinstance(l, list):
        yield (l, depth)
    else:
        for sublist in l:
            yield from levels(sublist, depth + 1)

SIDEBAR_DATA_LEVEL = list(levels(SIDEBAR_DATA))
'''

# Sidebar
'''
subitems_stocks = []
for item, tab in SIDEBAR_DATA_LEVEL:
    subitems_stocks += [dac.SidebarMenuSubItem(id=str(tab)+item, 
                                label=item)
                    ]
'''

sidebarmenu_variable = []
subitems=[]
for item, tab in SIDEBAR_DATA_LEVEL:
    if tab==0:
        sidebarmenu_variable += [dac.SidebarHeader(children=item)]
    elif tab==1:
        sidebarmenu_variable += [dac.SidebarMenuItem(id=item, label=item, icon='box')]
    elif tab==2:       
        sidebarmenu_variable += [dac.SidebarMenuItem(label=item, icon='cubes', children=subitems)]
    elif tab==3:
        subitems += [dac.SidebarMenuSubItem(id=item, label=item)]
print(subitems) # add list dans list, ajouter ID par tab=2 et iterate l'id a chaque id=2 trigger
sidebar = dac.Sidebar(
	dac.SidebarMenu(
            sidebarmenu_variable
	),
    title='Arcane Terminal',
	skin="light",
    color="dark",
	brand_color="dark",
    url="https://google.com",
    src="https://www.e-pass.education/themes/template/img/160x160/img1.jpg",
    elevation=3,
    opacity=0.8
)

# Body
body = dac.Body(
    dac.TabItems([
dac.TabItem(id='content_stocks_1',           
    children=dbc.Form(
    dbc.Row(
        [
            dbc.Label("Email", width="auto"),
            dbc.Col(
                dbc.Input(type="email", placeholder="Enter email"),
                className="me-3",
            ),
            dbc.Label("Password", width="auto"),
            dbc.Col(
                dbc.Input(type="password", placeholder="Enter password"),
                className="me-3",
            ),
            dbc.Col(dbc.Button("Submit", color="primary"), width="auto"),
        ],
        className="g-2",
    )
)
),
        dac.TabItem(html.P('Gallery 2 (You can add Dash Bootstrap Components!)'), 
                    id='content_stocks_2'),
    ])
)

# Controlbar
controlbar = dac.Controlbar(
    [
        html.Br(),
        html.P("Slide to change graph in Basic Boxes"),
        dcc.Slider(
            id='controlbar-slider',
            min=10,
            max=50,
            step=10,
            value=20
        )
    ],
    title = "API Keys",
    skin = "light"
)

footer = dac.Footer(
	html.A("@Benjamin Capron",
		href = "https://twitter.com/quanteeai", 
		target = "_blank", 
	),
)

# =============================================================================
# App Layout
# =============================================================================
app.layout = dac.Page([navbar, sidebar, body, controlbar, footer])

# =============================================================================
# Callbacks
# =============================================================================
def activate(input_id, 
             n_stocks_1, n_stocks_2):
    
    # Depending on tab which triggered a callback, show/hide contents of app
    if input_id == 'tab_stocks_1' and n_stocks_1:
        return True, False
    elif input_id == 'tab_stocks_2' and n_stocks_2:
        return False, True
    else:
        return True, False # App init
    
@app.callback([
               Output('content_stocks_1', 'active'),
               Output('content_stocks_2', 'active')],
               [
                Input('tab_stocks_1', 'n_clicks'),
                Input('tab_stocks_2', 'n_clicks')]
)

def display_tab(n_stocks_1, n_stocks_2):
    
    ctx = dash.callback_context # Callback context to recognize which input has been triggered

    # Get id of input which triggered callback  
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]   

    return activate(input_id, 
                    n_stocks_1, n_stocks_2)

@app.callback([
               Output('tab_stocks_1', 'active'),
               Output('tab_stocks_2', 'active')],
               [
                Input('tab_stocks_1', 'n_clicks'),
                Input('tab_stocks_2', 'n_clicks')]
)
def activate_tab(n_stocks_1, n_stocks_2):
    
    ctx = dash.callback_context # Callback context to recognize which input has been triggered

    # Get id of input which triggered callback  
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]   

    return activate(input_id, 
                    n_stocks_1, n_stocks_2)
    

# =============================================================================
# Run app    
# =============================================================================
if __name__ == '__main__':
    app.run_server(debug=True)

