import praw.errors


def repost_submission(submission, bot, settings):
    subreddit = bot.get_subreddit(settings['destination_subreddit'])

    try:
        return subreddit.submit(
            submission.title, url=submission.permalink, raise_captcha_exception=True
        )
    except praw.errors.AlreadySubmitted:
        pass

