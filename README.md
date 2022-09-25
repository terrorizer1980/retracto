![Retracto](https://user-images.githubusercontent.com/54491362/192131222-091396c6-c0f4-406d-9c9c-abcaa694840a.png)

YouTube comment spam can take many forms. Major creators are often concerned about spam that impersonates them, promises viewers something good for messaging them, and then directs individuals off YouTube in some way to eventually scam them.Other spam comments can be less overtly malicious but still annoying or potentially harmful. YouTube does have many tools to combat spammy comments, and it removes a huge amount of them automatically.

![spams](https://user-images.githubusercontent.com/54491362/192131234-8d4475d9-e1cd-4f85-8e27-c2f27a470415.png)

<b> Retracto </b> automatically identifies spam comments using Machine Learning and deletes them in a single command.

The package contains the following commands:
- `retracto login`
- `retracto comment <video_id>`

You have to start by logging into your google account by using `retracto login` and then use `retracto comment <video_id>` to strip down spam comments on your video.

`<video_id>`: Go to your video on YouTube and copy the video id from the url(https://www.youtube.com/watch?v=<b><video_id></b>) and use it in the command.

  ### Architectural Diagram
  ![image](https://user-images.githubusercontent.com/54491362/192131119-cac8260f-c4b8-4ce8-86c0-8b0bfff76b9f.png)
  
  ### Techstack Used
  - Typer CLI (https://typer.tiangolo.com/)
  - Youtube API
  - Cohere Platform (https://os.cohere.ai/)
  
