from math import pi
from pydantic import create_model_from_namedtuple
import typer
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import cohere
import pickle


CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

app = typer.Typer()
co = cohere.Client('4GulVsuVRGhCWBBQejv2WwZYeyIpJiE8VNL4MDqt')


@app.command()
def comments(video_id: str):
    """ Get comments """
    youtube = get_authenticated_service()
    res = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id
    ).execute()
    d = {}
    for x in res['items']:
        comm = x['snippet']['topLevelComment']
        dsp = comm['snippet']['textDisplay']
        id = comm['id']
        l = d.get(dsp, [])
        l.append(id)
        d[dsp] = l

    classify_and_delete(list(d.keys()), d, youtube)


@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")


def get_authenticated_service():
    try:
        credentials = pickle.load(open('cred', 'rb'))
        return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
    except:
        pass

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(host='localhost',
    port=8080, 
    authorization_prompt_message='Please visit this URL: {url}', 
    success_message='The auth flow is complete; you may close this window.',
    open_browser=True)
    pickle.dump(credentials, open('cred', 'wb'))

    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def classify_and_delete(inp, d, youtube):
    classifications = co.classify(
        model='15b6a8b8-85de-4c4b-8adf-b5b7134e4ff5-ft',
        outputIndicator='this is:',
        inputs=inp)

    cls = classifications.classifications
    out = set()
    spams = []

    for c in cls:
        if(c.prediction == 'spam'):
            out.update(d[c.input])
            spams.append(c.input)

    print(spams)
    delete_comments(out, youtube)

      
def delete_comments(ids, youtube):
    for id in ids:
        youtube.comments().delete(id=id).execute()
    

