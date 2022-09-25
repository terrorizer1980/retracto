import os
import pickle
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import cohere


load_dotenv()
co = cohere.Client(os.getenv('cohere_key'))
CLIENT_SECRETS_FILE = 'retracto/client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

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