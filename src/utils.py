import re


def clean_subreddit(raw_subreddit):
    #TODO URL to subreddit
    return raw_subreddit


def clean_username(raw_username):
    #TODO URL to username
    return raw_username


def clean_settings(raw_settings):
    """ return a normalized settings dict from settings module """
    clean_settings = {}

    user_agent = getattr(raw_settings, 'user_agent', None)
    if not user_agent:
        raise Exception('Missing user_agent in settings')
    clean_settings['user_agent'] = user_agent

    bot_username = getattr(raw_settings, 'bot_username', None)
    if not bot_username:
        raise Exception('Missing bot_username in settings')
    clean_settings['bot_username'] = bot_username

    bot_password = getattr(raw_settings, 'bot_password', None)
    if not bot_password:
        raise Exception('Missing bot_password in settings')
    clean_settings['bot_password'] = bot_password

    destination_subreddit = getattr(raw_settings, 'destination_subreddit', None)
    if not destination_subreddit:
        raise Exception('Missing destination_subreddit in settings')
    clean_settings['destination_subreddit'] = clean_subreddit(destination_subreddit)

    clean_settings['title_template'] = unicode(getattr(raw_settings, 'title_template', '{s.title}'))

    matched_keywords = getattr(raw_settings, 'matched_keywords', [])
    if isinstance(matched_keywords, basestring):
        matched_keywords = [matched_keywords]
    clean_settings['matched_keywords'] = [keyword.lower() for keyword in matched_keywords]

    matched_regexps = getattr(raw_settings, 'matched_regexps', [])
    if isinstance(matched_regexps, basestring):
        matched_regexps = [matched_regexps]
    clean_settings['matched_regexps'] = [re.compile(regexp, re.I) for regexp in matched_regexps]

    excluded_keywords = getattr(raw_settings, 'excluded_keywords', [])
    if isinstance(excluded_keywords, basestring):
        excluded_keywords = [excluded_keywords]
    clean_settings['excluded_keywords'] = [keyword.lower() for keyword in excluded_keywords]

    excluded_regexps = getattr(raw_settings, 'excluded_regexps', [])
    if isinstance(excluded_regexps, basestring):
        excluded_regexps = [excluded_regexps]
    clean_settings['excluded_regexps'] = [re.compile(regexp, re.I) for regexp in excluded_regexps]

    target_subreddits = getattr(raw_settings, 'target_subreddits', [])
    if not target_subreddits:
        target_subreddits.append('all')
    elif isinstance(target_subreddits, basestring):
        target_subreddits = [target_subreddits]
    clean_settings['target_subreddits'] = [clean_subreddit(subreddit) for subreddit in target_subreddits]

    ignored_subreddits = getattr(raw_settings, 'ignored_subreddits', [])
    if isinstance(ignored_subreddits, basestring):
        ignored_subreddits = [ignored_subreddits]
    clean_settings['ignored_subreddits'] = [clean_subreddit(subreddit) for subreddit in ignored_subreddits]
    clean_settings['ignored_subreddits'].append(clean_settings['destination_subreddit'])

    ignored_submitters = getattr(raw_settings, 'ignored_submitters', [])
    if isinstance(ignored_submitters, basestring):
        ignored_submitters = [ignored_submitters]
    clean_settings['ignored_submitters'] = [clean_username(username) for username in ignored_submitters]

    return clean_settings

