from praw import Reddit

import settings as raw_settings
from utils import clean_settings

settings = clean_settings(raw_settings)

bot = Reddit(user_agent=settings['user_agent'])
