import praw.errors


def repost_submission(submission, bot, settings):
    subreddit = bot.get_subreddit(settings['destination_subreddit'])

    title = settings['title_template'].format(s=submission)
    try:
        return subreddit.submit(
            title, url=submission.permalink, raise_captcha_exception=True
        )
    except praw.errors.AlreadySubmitted:
        pass

