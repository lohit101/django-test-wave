import praw

reddit = praw.Reddit(
    client_id="knbUbBEc4z1gwkCsTgSqtA",
    client_secret="l82ipqXjyzttMwa5DwBs0EvfdkOwaA",
    user_agent="Window11:YTFaceless:v0.1 by u/Msfvenomm",
)


def getstory(subreddit):
    textlistfinal = []
    textlist = []
    n = 0
    for submission in reddit.subreddit(subreddit).hot(limit = 3):
        textlist.append(submission.title)
        for top_level_comment in submission.comments:
            try:
                textlist.append(top_level_comment.body)
                n += 1
                if n >= 5:
                    break
            except AttributeError:
                break
        textlistfinal.append(textlist)
        textlist = []
        n = 0
        
    response = {
        'response' : textlistfinal
    }
    
    return JsonResponse(response)
    
getstory("askreddit")