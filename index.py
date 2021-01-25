import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import re
import emoji
import os
import base64
from urllib.parse import quote as urlquote
from urllib.parse import urlparse
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_uploader as du
from app import app
# from app import server
from apps import suckmydata

UPLOAD_DIRECTORY = os.getcwd()+"/datasets/app_uploaded_files"
du.configure_upload(app, r"datasets/app_uploaded_files",use_upload_id=False)

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

filelist = [ f for f in os.listdir(UPLOAD_DIRECTORY) if True ]
for f in filelist:
    os.remove(os.path.join(UPLOAD_DIRECTORY, f))

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

app.title = 'SuckMyData - Chat Analyzer'


ASSETS = os.path.dirname(os.path.abspath(__file__))

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
how_to = os.path.join(THIS_FOLDER, 'assets/how_to.png')
dots = os.path.join(THIS_FOLDER, 'assets/3dots.png')
encoded_image = base64.b64encode(open(how_to, 'rb').read())
dot_image = base64.b64encode(open(dots, 'rb').read())

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1(html.B("SuckMyData"),
                        className='text-center mt-3'),
                ),
                style={'color': 'Green','font-size':'500px','font-weight': 'bold'},
    ),

    dbc.Row(
        dbc.Col(html.P("A Chat Analyzing Tool",
                        className='text-center mb-0'),
                ),
                style={'color': 'black',},
    ),

    html.Hr(),
    html.Br(),
    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(
            html.H1("Upload File Below",style={'color':'black'}),
        )
    ]),

    html.Div(
                [
                    html.A("Concerned about PRIVACY ?", id="open", className="mr-1",style={'color':'brown','cursor': 'pointer'}),
                    dbc.Modal(
                      [
                        dbc.ModalHeader(html.H4(html.B("Don't Judge us by the Name 😜")),style={'color':'red'},className='text-center'),
                        dbc.ModalBody(["We respect your privacy, no uploaded data or files are stored anywhere on the servers, only an instance of your file is created to compute the data for creating visualizations."]),
                        dbc.ModalFooter(
                         dbc.Button("Close", id="close", className="ml-auto")
                            ),
                     ],id="modal",centered=True,
                    ),
                ],style={'text-align':'center'}
    ),

    html.Br(),

    html.Div([
               du.Upload(id="upload-data",filetypes=['txt']),
            ]),

    dbc.Row(
        dbc.Col(
            html.A("Need help?",id='help',className='text-center',style={'text-decoration':'underline','color':'orange'}, href='#sendhelp')
        )
    ),

    html.Br(),

    dbc.Row(
        dbc.Col(
            html.Div([
                html.Div([
                    dcc.Link(dbc.Button('Start Analysis',id='start_analysis',n_clicks=0,color='success',className="mr-1"), href='/analysis'),
                ], className="center"),
                html.Br(),
                html.Div(
                    html.P(id='status')
                ),
            ])
        )

    ),

    html.Br(),
    html.Br(),
    html.Br(),

    dbc.Row(
        dbc.Col([
            html.H1("Demo",className="text-center",style={'color':'cornflowerblue'}),
            html.P("Check out analysis on a Fake generated chat."),
            dcc.Link(dbc.Button("Demo Analysis",size="sm",className="center"), href='/demo')
        ])
    ),

    html.Br(),
    html.Br(),

    dbc.Row(
        dbc.Col(html.H1("How To Use?",id='sendhelp',
                        className='text-center mt-4'),
                ),
                style={'color': 'purple',},
    ),

    dbc.Row(
        dbc.Col(html.H2(["To use our chat analyzer you need to ", html.B("export your WhatsApp chat to a text file.")],
                        className='text-center'),
                ),
                style={'color': 'black',},
    ),

    dbc.Row(
        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),className='img-fluid')
        )
    ),

    dbc.Row(
        dbc.Col([
                html.H5("Follow the below mentioned steps:"),
                html.P("1. Go to WhatsApp in your mobile phone and select the desired group.",
                        className='text-center'),
                html.P(["2. Press the context menu ( ",html.Img(src='data:image/png;base64,{}'.format(dot_image.decode())), " ) in the top right corner."],
                        className='text-center'),
                html.P(["3. In the context menu, select the ", html.Q("More"), " item"],
                        className='text-center'),
                html.P(["4. In the new menu, choose ", html.Q("Export Chat")],
                        className='text-center'),
                html.P(["5. A popup will ask you to choose between exporting with or without media.", html.P(["Choose the ", html.Q("Without Media")," option."])],
                        className='text-center'),
                html.P("6. Email the exported text file to yourself.",
                className='text-center'),
                html.P(["7. Download the file and upload it ",html.A('above.',href='#')],
                className='text-center')
        ]),
    ),

    html.Br(),
    html.Br(),

    html.Footer(["Created with 🖤 by ", html.A("Atharva Katre",id="creator",style={'text-decoration':'underline','cursor': 'pointer'})]),
    dbc.Modal(
                [
                dbc.ModalHeader(html.H3(html.B("Connect with me ⚡")),style={'color':'Green',}),
                dbc.ModalBody([
                    dbc.Button(html.Span([html.A(className="fab fa-github ml-2",href="https://github.com/AtharvaKatre")])),"        ",
                    dbc.Button(html.Span([html.A(className="fab fa-linkedin ml-2",href="https://www.linkedin.com/in/atharva-katre-563639177")])),"      ",
                    dbc.Button(html.Span([html.A(className="fab fa-twitter ml-2",href="https://twitter.com/katre_atharva")])),"     ",
                    dbc.Button(html.Span([html.A(className="fab fa-instagram ml-2",href="https://www.instagram.com/llatharvall/")])),

                    ],style={'text-align':'center'}),
                dbc.ModalFooter(
                    dbc.Button("Close", id="socials_close", className="ml-auto")
                    ),
                ],id="socials",centered=True,
                    ),

    html.Br(),

    ],style={'text-align':'center'}, fluid=True)

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)(toggle_modal)
app.callback(
    Output("socials", "is_open"),
    [Input("creator", "n_clicks"), Input("socials_close", "n_clicks")],
    [State("socials", "is_open")],
)(toggle_modal)

@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        pass
    else:
        return [html.P(file_download_link(files[0]))]

@app.callback(
    Output('status','children'),
    [Input("start_analysis","n_clicks")]
              )
def analysis_status(n):
    if n>0:
        return "Generating visualizations..."

# -----------------------------------------------START ANALYSIS CALLBACK--------------------------------------------------------------------------

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/demo':
        return suckmydata.layout
    if pathname == '/analysis':
        filelist = [ f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith(".txt") ]
        if len(filelist)!=0:
            # -----------------------------------------Data Cleaning--------------------------------------------------------------------------------
                filelist = [ f for f in os.listdir(UPLOAD_DIRECTORY) if not f.endswith(".txt") ]
                for f in filelist:
                    os.remove(os.path.join(UPLOAD_DIRECTORY, f))

                def startsWithDate(s):
                    pattern = '^(([0-9])|((1)[0-2])|([1-9]|[0-2][0-9]|(3)[0-1]))(\/)([1-9]|[0-2][0-9]|(3)[0-1])(\/)(\d{2}|\d{4}), ([0-9]|[1][0-2]):([0-9][0-9])'
                    result = re.match(pattern, s)
                    if result:
                        return True
                    return False

                def startsWithAuthor(s):
                    patterns = [
                        '([\w]+):',                        # First Name
                        '([\w]+[\s]+[\w]+):',              # First Name + Last Name
                        '([\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
                        '([+]\d{2} \d{5} \d{5}):',         # Mobile Number (India)
                        '([+]\d{2} \d{3} \d{3} \d{4}):',   # Mobile Number (US)
                        '([+]\d{2} \d{4} \d{7})'           # Mobile Number (Europe)
                    ]
                    pattern = '^' + '|'.join(patterns)
                    result = re.match(pattern, s)
                    if result:
                        return True
                    return False

                def getDataPoint(line):
                    # line = 18/06/17, 22:47 - Loki: Why do you have 2 numbers, Banner?

                    splitLine = line.split(' - ') # splitLine = ['18/06/17, 22:47', 'Loki: Why do you have 2 numbers, Banner?']

                    dateTime = splitLine[0] # dateTime = '18/06/17, 22:47'

                    date, time = dateTime.split(', ') # date = '18/06/17'; time = '22:47'

                    message = ' '.join(splitLine[1:]) # message = 'Loki: Why do you have 2 numbers, Banner?'

                    if startsWithAuthor(message): # True
                        splitMessage = message.split(': ') # splitMessage = ['Loki', 'Why do you have 2 numbers, Banner?']
                        author = splitMessage[0] # author = 'Loki'
                        message = ' '.join(splitMessage[1:]) # message = 'Why do you have 2 numbers, Banner?'
                    else:
                        author = None
                    return date, time, author, message

                parsedData = [] # List to keep track of data so it can be used by a Pandas dataframe
                conversationPath = "datasets/app_uploaded_files/"+uploaded_files()[0]
                with open(conversationPath, encoding="utf-8") as fp:
                    fp.readline() # Skipping first line of the file (usually contains information about end-to-end encryption)

                    messageBuffer = [] # Buffer to capture intermediate output for multi-line messages
                    date, time, author = None, None, None # Intermediate variables to keep track of the current message being processed

                    while True:
                        line = fp.readline()
                        if not line: # Stop reading further if end of file has been reached
                            break
                        line = line.strip() # Guarding against erroneous leading and trailing whitespaces
                        if startsWithDate(line): # If a line starts with a Date Time pattern, then this indicates the beginning of a new message
                            if len(messageBuffer) > 0: # Check if the message buffer contains characters from previous iterations
                                parsedData.append([date, time, author, ' '.join(messageBuffer)]) # Save the tokens from the previous message in parsedData
                            messageBuffer.clear() # Clear the message buffer so that it can be used for the next message
                            date, time, author, message = getDataPoint(line) # Identify and extract tokens from the line
                            messageBuffer.append(message) # Append message to buffer
                        else:
                            messageBuffer.append(line) # If a line doesn't start with a Date Time pattern, then it is part of a multi-line message. So, just append to buffer
                filelist = [ f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith(".txt") ]
                for f in filelist:
                    os.remove(os.path.join(UPLOAD_DIRECTORY, f))

                df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Name', 'Message'])
                df = df.dropna()
                df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
                wordcount = df['Message'].apply(len).sum()

                # ----------------------------------------------Plotting Functions---------------------------------------------------------------------------------------
                def gossip_queen():
                    fig  = px.histogram(df, histfunc="count", x='Name', color='Name', color_discrete_sequence=px.colors.sequential.Sunsetdark, hover_data=[df['Name']])
                    fig.update_traces(hovertemplate=None,hoverinfo='y')
                    fig.update_layout(xaxis_title='Group Members', yaxis_title="No. of messages", title_x=0.5)
                    fig.update_layout(template='plotly_white',showlegend=False)
                    return fig

                emoji_list=[]
                def extract_emojis(msg):
                    for word in msg:
                        for char in word:
                            if char in emoji.UNICODE_EMOJI:
                                emoji_list.append(char)

                def emoji_counter():
                    extract_emojis(df['Message'])
                    emoji_df = pd.DataFrame(emoji_list, columns=['emoji'])
                    return len(emoji_df)

                def unique_emoji_counter():
                    extract_emojis(df['Message'])
                    emoji_df = pd.DataFrame(emoji_list, columns=['emoji'])
                    emoji_df = emoji_df.value_counts().rename_axis('emoji').reset_index(name='count')
                    return len(emoji_df)

                def emoji_meter():
                    extract_emojis(df['Message'])
                    emoji_df = pd.DataFrame(emoji_list, columns=['emoji'])
                    emoji_df = emoji_df.value_counts().rename_axis('emoji').reset_index(name='count')

                    fig = px.pie(emoji_df.head(10), names='emoji', values='count',)
                    fig.update_traces(textinfo='percent+label')
                    fig.update_layout(margin=dict(t=50, b=0, l=0, r=0))
                    fig.update_layout(template='plotly_white', title_x=0.5, showlegend=False)
                    return fig

                author_emoji_count=[]
                for author in df['Name'].unique():
                    extract_emojis(df[df['Name']==author]['Message'])
                    author_emoji_count.append(len(emoji_list))
                def emoji_master():
                    fig = px.bar(y=df['Name'].unique(), x=author_emoji_count[::-1],orientation='h', color=df['Name'].unique(), color_discrete_sequence=px.colors.cyclical.Phase,)
                    fig.update_traces(hovertemplate=None,hoverinfo='x')
                    fig.update_layout(barmode = 'stack', yaxis={'categoryorder':'total ascending','showgrid':False}, xaxis_title='No. of Emojis Used', yaxis_title="Group Members", title_x=0.5,)
                    fig.update_layout(template='plotly_white', showlegend = False)
                    return fig

                def night_owls():
                    night_df = df[(df['datetime'].dt.hour >= 23) | (
                                (df['datetime'].dt.hour >= 0) & (df['datetime'].dt.hour <= 4))][
                        'Name'].value_counts().rename('Name').reset_index()
                    night_df.columns = ['Name','count']
                    if len(night_df) == 0:
                        data = [['null', 0]]
                        night_df.reset_index()
                        night_df = pd.DataFrame(data, columns=['Name', 'count'])
                    fig = px.bar(night_df, x='count', y='Name', orientation='h', color='Name', color_discrete_sequence=px.colors.sequential.matter_r)
                    fig.update_traces(hovertemplate=None, hoverinfo='x')
                    fig.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending', 'title': 'Group Members', 'showgrid': False}, xaxis_title='No. of messages from 11 am to 5 am', title_x=0.5, )
                    fig.update_layout(template='plotly_white', showlegend=False)
                    return fig

                def early_birds():
                    early_df = df[(df['datetime'].dt.hour >= 6) & (df['datetime'].dt.hour >= 8)]['Name'].value_counts().rename('Name').reset_index()
                    early_df.columns = ['Name','count']
                    if len(early_df) == 0:
                        data = [['null', 0]]
                        early_df.reset_index()
                        early_df = pd.DataFrame(data, columns=['Name', 'count'])
                    fig = px.bar(early_df, x='count', y='Name', orientation='h', color='Name', color_discrete_sequence=px.colors.sequential.Oryel[::-1])
                    fig.update_traces(hovertemplate=None,hoverinfo='x')
                    fig.update_layout(barmode = 'stack', yaxis={'categoryorder':'total ascending','title':'Group Members','showgrid':False}, xaxis_title='No. of messages from 6 am to 9 am', title_x=0.5,)
                    fig.update_layout(template='plotly_white', showlegend = False)
                    return fig

                def links_shared():
                    link_df = df[df['Message'].apply(lambda x: True if any(word in x for word in ['.com','.in','.net','.org','.to','.io','http'])else False)]['Name'].value_counts().rename('count').reset_index()
                    link_df.columns=['Name','count']
                    fig = px.pie(link_df,names='Name',values='count',)
                    fig.update_traces(textposition='inside',textinfo='percent+label', hovertemplate=None, marker=dict(line=dict(color='#ffffff', width=5)))
                    fig.update_layout(margin=dict(t=50, b=0, l=0, r=0),title_x=0.5)
                    fig.update_layout(template='plotly_white', showlegend = False)
                    return fig

                def freq_domains():
                    link_df = df[df['Message'].apply(lambda x: True if any(word in x for word in ['.com','.in','.net','.org','.to','.io','http'])else False)]

                    def extract_domain(msg):
                        result = '{uri.netloc}'.format(uri=urlparse(msg))
                        if result !="":
                            if 'youtu' in result:
                                return 'www.youtube.com'
                            if '.org' in result:
                                return result.split('.org')[0] + ".com"
                            else:
                                return result

                    domain_df = link_df['Message'].apply(extract_domain).value_counts().rename('count').reset_index()
                    domain_df.columns=['Domains','count']

                    if (len(domain_df)==0):
                        data = [['null', 0]]
                        domain_df.reset_index()
                        domain_df = pd.DataFrame(data, columns=['Domains', 'count'])

                    fig = px.bar(domain_df.head(10), y='Domains', x='count', orientation='h', color='Domains', color_discrete_sequence=px.colors.sequential.dense[::-1])
                    fig.update_traces(hovertemplate=None,hoverinfo='x')
                    fig.update_layout(barmode = 'stack',xaxis_title='No. of Occurences', yaxis={'categoryorder':'total ascending', 'showgrid':False},title_x=0.5)
                    fig.update_layout(template='plotly_white', showlegend = False)
                    return fig

                def radar_plot():
                    msg_count = df['Name'].value_counts().rename('count').reset_index()
                    msg_count.columns = ['Name', 'count']
                    media_count = df[df['Message'] == '<Media omitted>'].groupby('Name').count()['Message'].sort_values(
                        ascending=False).rename('count').reset_index()
                    deleted_count = df[df['Message'] == 'This message was deleted']['Name'].value_counts().reset_index()
                    deleted_count.columns = ['Name', 'count']
                    link_df = df[df['Message'].apply(lambda x: True if any(
                        word in x for word in ['.com', '.in', '.net', '.org', '.to', '.io', 'http']) else False)][
                        'Name'].value_counts().rename('count').reset_index()
                    link_df.columns = ['Name', 'count']
                    contacts_count = df[df['Message'].apply(lambda x: '.vcf (file attached)' in x)][
                        'Name'].value_counts().reset_index()
                    contacts_count.columns = ['Name', 'count']

                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(r=msg_count['count'], theta=msg_count['Name'], name='Texts'))
                    fig.add_trace(go.Scatterpolar(r=deleted_count['count'], theta=deleted_count['Name'], name='Deleted texts'))
                    fig.add_trace(go.Scatterpolar(r=author_emoji_count[::-1], theta=df['Name'].unique(), name='Emojis'))
                    fig.add_trace(go.Scatterpolar(r=media_count['count'], theta=media_count['Name'],
                                                  name='Media(pics, video, audio, gifs) sent'))
                    fig.add_trace(go.Scatterpolar(r=link_df['count'], theta=link_df['Name'], name='Links'))
                    fig.add_trace(go.Scatterpolar(r=contacts_count['count'], theta=contacts_count['Name'], name='Contacts'))
                    fig.update_traces(fill='toself', hovertemplate=None)
                    fig.update_layout(legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ))
                    fig.update_layout(margin=dict(t=50, b=20, l=30, r=30))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
                    return fig
                def overall_activity():
                    no_of_msg=[]
                    for date in df['Date'].unique():
                        no_of_msg.append(len(df[df['Date']==date]))

                    fig = px.line(x=pd.to_datetime(df['Date'].unique()), y=no_of_msg, color_discrete_sequence=px.colors.sequential.Magenta[::-1])
                    fig.update_traces(hovertemplate=None)
                    fig.update_layout( xaxis_title='', yaxis_title="No. of messages", title_x=0.5)
                    fig.update_layout(template='plotly_white', showlegend = False)
                    return fig

                def member_activity():
                    fig = go.Figure()
                    newdf = df.groupby('Date')['Name'].value_counts().rename('msgcount').reset_index()

                    for Date, msgcount in newdf.groupby('Name'):
                        fig.add_trace(go.Scatter(x= pd.to_datetime(msgcount.Date), y = msgcount.msgcount, name=Date, mode='markers', marker=dict(sizemode='area', line_width=0.5)))
                    fig.update_layout(yaxis_title='No. of Messages',  xaxis_title='Timeline', title_x=0.5, template='plotly_white')
                    return fig

                def chat_clock():
                    no_of_msg=[]
                    for hour in df['datetime'].dt.hour.unique():
                        no_of_msg.append(len(df[df['datetime'].dt.hour==hour]))

                    fig = px.bar(x=df['datetime'].dt.hour.unique(), y=no_of_msg, color=no_of_msg)
                    fig.update_layout(xaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 4,
                        ), xaxis_title='Clock Hours', yaxis_title="No. of messages", title_x=0.5,)
                    fig.update_traces(hovertemplate=None)
                    fig.update(layout_coloraxis_showscale=False,)
                    fig.update_layout(template='plotly_white', showlegend = False,)
                    return fig

                def daysofweek():
                    no_of_msg=[]
                    for day in df['datetime'].dt.day_name().unique():
                        no_of_msg.append(len(df[df['datetime'].dt.day_name()==day]))

                    fig = px.pie(names=df['datetime'].dt.day_name().unique(), values=no_of_msg, hole=0.5)
                    fig.update_traces(textinfo='percent+label',hovertemplate=None)
                    fig.update_layout(margin=dict(t=50, b=0, l=0, r=0))
                    fig.update_layout(title_x=0.5)
                    fig.update_layout(template='plotly_white', showlegend = False)
                    return fig

                new_dash = dbc.Container([

                    dbc.Row(
                        dbc.Col(html.H1(html.A(html.B("SuckMyData"),
                                        className='text-center mt-4',href="/",style={'color': 'Green','text-decoration':'None','cursor':'pointer'}))
                                ),
                    ),
                    dbc.Row(
                        dbc.Col(html.P("A Chat Analyzing Tool",
                                        className='text-center mb-0'),
                                ),
                                style={'color': 'black',},
                    ),

                    html.Hr(),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col(
                            html.Div(
                                [
                                    html.H2(["Word Count"], className='text-center mt-4 mb-2'),
                                    html.H2(wordcount, className='text-center mt-4 mb-2',style={'color': 'blue',},),
                                    html.H2(["That's enough words to write ", html.Span(round(wordcount/1139),style={'color': 'red',}) ," Wikipedia articles of average size"], className='text-center mt-3'),
                                ]
                            ),
                        )
                    ]),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2(["Gossip Queen"], className='text-center mt-4'),
                            ]),
                            html.Div([
                            dcc.Graph(
                                id = 'first plot',
                                figure = gossip_queen()
                            )])
                        ])
                    ], no_gutters=True, justify='center'),  # Horizontal:start,center,end,between,around

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2(["Emoji Meter🤙"], className='text-center mt-xl-5'),
                                html.H2(["Total Emoji Count: ", html.Span(emoji_counter(),style={'color': 'red',})], className='text-center mt-3'),
                                html.H2(["Unique Emoji Count: ", html.Span(unique_emoji_counter(),style={'color': 'red',})], className='text-center mt-3'),
                            ]),
                            html.Div([
                            dcc.Graph(
                                id = 'second plot',
                                figure = emoji_meter()
                            )])
                        ])
                    ], no_gutters=True, justify='center'),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2(["Emoji Master🥳"], className='text-center mt-xl-5'),
                            ]),
                            html.Div([
                            dcc.Graph(
                                id = 'third plot',
                                figure = emoji_master()
                            )])
                        ])
                    ], no_gutters=True, justify='center'),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2(["Night Owls - 11 AM to 5 AM"], className='text-center mt-xl-5'),
                            ]),
                            html.Div([
                            dcc.Graph(
                                id = 'fourth plot',
                                figure = night_owls()
                            )])
                        ])
                    ], no_gutters=True, justify='center'),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2(["Early Birds - 6 AM to 9 AM"], className='text-center mt-xl-5'),
                            ]),
                            html.Div([
                            dcc.Graph(
                                id = 'fifth plot',
                                figure = early_birds()
                            )])
                        ])
                    ], no_gutters=True, justify='center'),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2(["Links Shared"], className='text-center mt-xl-5'),
                            ]),
                            html.Div([
                            dcc.Graph(
                                id = 'sixth plot',
                                figure = links_shared()
                            )])
                        ])
                    ], no_gutters=True, justify='center'),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2(["Most Frequent Domains"], className='text-center mt-xl-5'),
                            ]),
                            html.Div([
                            dcc.Graph(
                                id = 'seventh plot',
                                figure = freq_domains()
                            )])
                        ])
                    ], no_gutters=True, justify='center'),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2(["Content Distribution"], className='text-center mt-4'),
                            ]),
                            html.Div([
                                dcc.Graph(
                                    id = 'radar plot',
                                    figure = radar_plot()
                                )])
                        ])
                    ], no_gutters=True, justify='center'),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2(["Overall Group Activity"], className='text-center mt-xl-5'),
                            ]),
                            html.Div([
                            dcc.Graph(
                                id = 'eighth plot',
                                figure = overall_activity()
                            )])
                        ])
                    ], no_gutters=True, justify='center'),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2(["Group Activity Per Member"], className='text-center mt-xl-5'),
                            ]),
                            html.Div([
                            dcc.Graph(
                                id = 'ninth plot',
                                figure = member_activity()
                            )])
                        ])
                    ], no_gutters=True, justify='center'),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2(["Chat Clock"], className='text-center mt-xl-5'),
                            ]),
                            html.Div([
                            dcc.Graph(
                                id = 'tenth plot',
                                figure = chat_clock()
                            )])
                        ])
                    ], no_gutters=True, justify='center'),

                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H2(["Days of the Week"], className='text-center mt-xl-5'),
                            ]),
                            html.Div([
                            dcc.Graph(
                                id = 'eleventh plot',
                                figure = daysofweek()
                            )])
                        ])
                    ], no_gutters=True, justify='center'),

                    html.Br(),
                    html.Br(),

                    html.Footer(["Created with 🖤 by ", html.A("Atharva Katre",id="creator",style={'text-decoration':'underline','cursor': 'pointer'})]),
                    dbc.Modal(
                    [
                    dbc.ModalHeader(html.H3(html.B("Connect with me ⚡")),style={'color':'Green',}),
                    dbc.ModalBody([
                        dbc.Button(html.Span([html.A(className="fab fa-github ml-2",href="https://github.com/AtharvaKatre")])),"        ",
                        dbc.Button(html.Span([html.A(className="fab fa-linkedin ml-2",href="https://www.linkedin.com/in/atharva-katre-563639177")])),"      ",
                        dbc.Button(html.Span([html.A(className="fab fa-twitter ml-2",href="https://twitter.com/katre_atharva")])),"     ",
                        dbc.Button(html.Span([html.A(className="fab fa-instagram ml-2",href="https://www.instagram.com/llatharvall/")])),

                        ],style={'text-align':'center'}),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="socials_close", className="ml-auto")
                        ),
                    ],id="socials",centered=True,
                        ),

                    html.Br(),

                    ],style={'textAlign': 'center'}, fluid=True)

                return new_dash

        else:
            filelist = [ f for f in os.listdir(UPLOAD_DIRECTORY) if True ]
            for f in filelist:
                os.remove(os.path.join(UPLOAD_DIRECTORY, f))
            no_file = dbc.Container([

                dbc.Row(
                    dbc.Col(html.H1(html.A(html.B("SuckMyData"),
                                           className='text-center mt-4', href="/",
                                           style={'color': 'Green', 'text-decoration': 'None', 'cursor': 'pointer'}))
                            ),
                ),

                dbc.Row(
                    dbc.Col(html.P("A Chat Analyzing Tool",
                                   className='text-center mb-0'),
                            ),
                    style={'color': 'black', },
                ),

                html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),

                dbc.Row(
                    dbc.Col(html.H3("No file uploaded! Please upload a file."))
                ),

                html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),html.Br(), html.Br(), html.Br(), html.Br(),
                html.Br(),

                html.Footer(["Created with 🖤 by ", html.A("Atharva Katre", id="creator",
                                                           style={'text-decoration': 'underline',
                                                                  'cursor': 'pointer'})]),
                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H3(html.B("Connect with me ⚡")), style={'color': 'Green'}),
                        dbc.ModalBody([
                            dbc.Button(html.Span(
                                [html.A(className="fab fa-github ml-2", href="https://github.com/AtharvaKatre")])),
                            "        ",
                            dbc.Button(html.Span([html.A(className="fab fa-linkedin ml-2",
                                                         href="https://www.linkedin.com/in/atharva-katre-563639177")])),
                            "      ",
                            dbc.Button(html.Span(
                                [html.A(className="fab fa-twitter ml-2", href="https://twitter.com/katre_atharva")])),
                            "     ",
                            dbc.Button(html.Span([html.A(className="fab fa-instagram ml-2",
                                                         href="https://www.instagram.com/llatharvall/")])),

                        ], style={'text-align': 'center'}),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="socials_close", className="ml-auto")
                        ),
                    ], id="socials", centered=True,
                ),

                html.Br(),

            ],style={'textAlign':'center'}, fluid=True )

            return no_file

    else:
        return index_page

if __name__ == "__main__":
    app.run_server()
