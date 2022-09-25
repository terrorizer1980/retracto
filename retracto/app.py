import typer
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import cohere
import pickle
import os
from dotenv import load_dotenv


load_dotenv()
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

app = typer.Typer()
co = cohere.Client(os.getenv('cohere_key'))


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
def login():
    """
    login
    """

    get_authenticated_service(use_ex=False)


def get_authenticated_service(use_ex=True):
    if (use_ex):
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
        model=os.getenv('model'),
        outputIndicator='this is:',
        inputs=inp)

    cls = classifications.classifications
    out = set()
    spams = []

    for c in cls:
        if(c.prediction == 'spam'):
            out.update(d[c.input])
            spams.append(c.input)

    print("Spam Comments are:" + spams)
    delete_comments(out, youtube)

      
def delete_comments(ids, youtube):
    for id in ids:
        youtube.comments().delete(id=id).execute()
    

