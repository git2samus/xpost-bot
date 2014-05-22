xpost-bot
=========

Reddit bot to scan and repost submissions of interest to niche subreddits

Setup
-----

* Install Python+pip (tested on Python 2.7.3)
* Install deps with `pip install -r requirements.txt`
* Copy src/settings.py.example to src/settings.py and fill-in
* Run src/bot.py

Settings
--------

**user_agent** string to identify the bot on Reddit (REQUIRED)

**bot_username** Reddit user from which the bot will post, e.g. 'Samus_' (REQUIRED)

**bot_password** credentials for bot_username e.g. 'hunter2' (REQUIRED)

**destination_subreddit** subreddit to repost matches, e.g. 'AskReddit'

**title_template** template string to generate submission title, defaults to '{s.title}' which simply copies the original. `s` is an instance of https://praw.readthedocs.org/en/v2.1.16/pages/code_overview.html#praw.objects.Submission

**matched_keywords**, **matched_regexps** list of strings/string-regexps that the submission must contain/match (any of those) in order to be considered for repost

**excluded_keywords**, **excluded_regexps** list of strings/string-regexps that the submission must not contain/match (none of those) in order to be considered for repost, takes precedence over matched

**target_subreddits** list of subreddits to scan for matches, e.g. ['python', 'django'] (defaults to ['all'] meaning the whole site)
**ignored_subreddits** list of subreddits to exclude from matches (destination_subreddit is automatically ignored)
**ignored_submitters** list of Reddit usernames for users whose submissions won't be reposted

TODO
----

* Handle connection errors
* Stop gracefully
* Add logging messages

<img src="http://makeameme.org/media/created/i-should-write-udvuld.jpg" alt="Sophisticated Cat" title="I should write some tests" />

