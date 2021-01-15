import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import emoji
import os
from urllib.parse import urlparse
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app


df = pd.read_csv(os.getcwd()+"\datasets\Fake Chat.csv")
df = df.dropna()
df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
wordcount = df['Message'].apply(len).sum()

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
    fig = px.bar(df[(df['datetime'].dt.hour >= 23) | ((df['datetime'].dt.hour >= 0) & (df['datetime'].dt.hour <= 4))]['Name'].value_counts().rename_axis('Name').reset_index(name='count'), x='count', y='Name', orientation='h', color='Name', color_discrete_sequence=px.colors.sequential.matter_r)
    fig.update_traces(hovertemplate=None, hoverinfo='x')
    fig.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending', 'title': 'Group Members', 'showgrid': False}, xaxis_title='No. of messages from 11 am to 5 am', title_x=0.5, )
    fig.update_layout(template='plotly_white', showlegend=False)
    return fig

def early_birds():
    fig = px.bar(df[(df['datetime'].dt.hour >= 6) & (df['datetime'].dt.hour <= 8)]['Name'].value_counts().rename_axis('Name').reset_index(name='count'), x='count', y='Name', orientation='h', color='Name', color_discrete_sequence=px.colors.sequential.Oryel[::-1])
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

    fig = px.bar(domain_df.head(10), y='Domains', x='count', orientation='h', color='Domains', color_discrete_sequence=px.colors.sequential.dense[::-1])
    fig.update_traces(hovertemplate=None,hoverinfo='x')
    fig.update_layout(barmode = 'stack',xaxis_title='No. of Occurences', yaxis={'categoryorder':'total ascending', 'showgrid':False},title_x=0.5)
    fig.update_layout(template='plotly_white', showlegend = False)
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

layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1(html.A("SuckMyData",
                               className='text-center mt-4', href="/",
                               style={'color': 'Green', 'text-decoration': 'None', 'cursor': 'pointer'}))
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
                html.P(["Select a content type from below dropdown menu"], className='text-center mt-4'),
            ]),
            dcc.Dropdown(
                id='dropdown',
                options=[
                {'label': 'Texts', 'value': 'text'},
                {'label': 'Media', 'value': 'media'},
                {'label': 'Deleted Messages', 'value': 'deleted'},
                {'label': 'Emojis', 'value': 'emoji'},
                {'label': 'Links', 'value': 'links'},
                {'label': 'Contacts', 'value': 'contacts'},
                ],value='deleted'
                
            ),
            html.Div([
            dcc.Graph(
                id = 'radar plot',
                figure = {}
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
                dbc.ModalHeader(html.H3(html.B("Connect with me ⚡")),style={'color':'Green'}),
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

@app.callback(
    Output(component_id='radar plot',component_property='figure'),
    [Input(component_id='dropdown',component_property='value')],
)
def update_my_graph(val_chosen):
    if val_chosen =='text':
        msg_count = df['Name'].value_counts().rename('count').reset_index()
        msg_count.columns=['Name','count']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=msg_count['count'],theta=msg_count['Name'],name='No of texts sent'))
        fig.update_traces(fill='toself',hovertemplate=None)
        fig.update_layout(margin=dict(t=50, b=20, l=30, r=30))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
        return fig
    if val_chosen =='media':
        media_count = df[df['Message']=='<Media omitted>'].groupby('Name').count()['Message'].sort_values(ascending=False).rename('count').reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=media_count['count'],theta=media_count['Name'],name='Media(pics, video, audio, gifs) sent'))
        fig.update_traces(fill='toself',hovertemplate=None)
        fig.update_layout(margin=dict(t=50, b=20, l=30, r=30))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
        return fig
    if val_chosen =='deleted':
        deleted_count = df[df['Message']=='This message was deleted']['Name'].value_counts().reset_index()
        deleted_count.columns = ['Name','count']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=deleted_count['count'],theta=deleted_count['Name'],name='Media(pics, video, audio, gifs) sent'))
        fig.update_traces(fill='toself',hovertemplate=None)
        fig.update_layout(margin=dict(t=50, b=20, l=30, r=30))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
        return fig
    if val_chosen =='emoji':
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=author_emoji_count[::-1],theta=df['Name'].unique(),name='Emojis sent'))
        fig.update_traces(fill='toself',hovertemplate=None)
        fig.update_layout(margin=dict(t=50, b=0, l=30, r=30))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
        return fig
    if val_chosen =='links':
        link_df = df[df['Message'].apply(lambda x: True if any(word in x for word in ['.com','.in','.net','.org','.to','.io','http'])else False)]['Name'].value_counts().rename('count').reset_index()
        link_df.columns=['Name','count']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=link_df['count'],theta=link_df['Name'],name='Links sent'))
        fig.update_traces(fill='toself',hovertemplate=None)
        fig.update_layout(margin=dict(t=50, b=0, l=30, r=30))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
        return fig
    if val_chosen =='contacts':
        contacts_count = df[df['Message'].apply(lambda x : '.vcf (file attached)' in x)]['Name'].value_counts().reset_index()
        contacts_count.columns = ['Name','count']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=contacts_count['count'],theta=contacts_count['Name'],name='Links sent'))
        fig.update_traces(fill='toself',hovertemplate=None)
        fig.update_layout(margin=dict(t=50, b=0, l=30, r=30))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
        return fig
    else :
        raise dash.exceptions.PreventUpdate


