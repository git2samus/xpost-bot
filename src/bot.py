#!/usr/bin/env python
from praw import Reddit

import settings as raw_settings
from generators import submissions_gen
from filters import filter_submission
from utils import clean_settings


if __name__ == '__main__':
    from datetime import datetime

    settings = clean_settings(raw_settings)
    bot = Reddit(user_agent=settings['user_agent'], cache_timeout=0)

    submissions = submissions_gen(bot, settings)
    submissions = (submission for submission in submissions if filter_submission(submission, settings))

    for submission in submissions:
        print('[{}] {} - {}'.format(datetime.now().isoformat(), submission.created_utc, submission))

