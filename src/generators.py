def submissions_gen(bot, settings, newer_than_id=None):
    # construct multireddit url to query from list of target subreddits
    target_subreddit = bot.get_subreddit('+'.join(settings['target_subreddits']))

    # if there's no anchor get the current newest and continue from there
    if newer_than_id is None:
        submissions = target_subreddit.get_new(limit=1)

        try:
            newer_than_id = next(submissions).name
        except StopIteration:
            # if it's an empty subreddit set as None
            # brings everything that gets posted from here until the next request
            newer_than_id = None

    next_anchor_id = None

    while True:
        # uses "before" API param because /new lists from newest to oldest
        # limit=None brings everything that matches (even if it takes multiple requests)
        submissions = target_subreddit.get_new(params={'before': newer_than_id}, limit=None)

        for submission in submissions:
            yield submission

            # save the first id as anchor since it'll be the newest
            if next_anchor_id is None:
                next_anchor_id = submission.name

        # avoid getting newer_than_id=None when there's no results from the previous iterations
        if next_anchor_id is not None:
            newer_than_id, next_anchor_id = next_anchor_id, None

