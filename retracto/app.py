import typer
from .helpers import get_authenticated_service, classify_and_delete


app = typer.Typer()


@app.command()
def comments(video_id: str):
    """ Get spam comments and delete them"""
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



    

