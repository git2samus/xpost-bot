#!/usr/bin/env python
import sys
from datetime import datetime

from bot import XPostBot
from utils import clean_settings
import settings as raw_settings


if __name__ == '__main__':
    settings = clean_settings(raw_settings)

    xpost_bot = XPostBot(settings)
    xpost_bot.login() # logged-in users get fewer cached responses from Reddit

    newer_than_id = sys.argv[1] if len(sys.argv) > 1 else None
    for submission in xpost_bot.get_submissions(newer_than_id):
        print('[{}] {} - {}'.format(datetime.now().isoformat(), submission.created_utc, submission))
        print(xpost_bot.repost_submission(submission))

