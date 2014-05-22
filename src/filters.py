def _test_submitter(submission, settings):
    if not submission.author:
        return True # ignore [deleted]
    author_name = submission.author.name.lower()
    return author_name in settings['ignored_submitters']


def _test_subreddit(submission, settings):
    subreddit_name = submission.subreddit.display_name.lower()
    return subreddit_name in settings['ignored_subreddits']


def _test_matched(text, settings):
    matched_keywords, matched_regexps = settings['matched_keywords'], settings['matched_regexps']

    text = text.lower()
    return any(
        keyword in text for keyword in matched_keywords
    ) or any(
        regexp.search(text) for regexp in matched_regexps
    )


def _test_excluded(text, settings):
    excluded_keywords, excluded_regexps = settings['excluded_keywords'], settings['excluded_regexps']

    text = text.lower()
    return not any(
        keyword in text for keyword in excluded_keywords
    ) and not any(
        regexp.search(text) for regexp in excluded_regexps
    )


def filter_submission(submission, settings):
    if _test_submitter(submission, settings) or _test_subreddit(submission, settings):
        return False

    match = _test_matched(submission.title, settings)
    if not match and submission.is_self:
        match = _test_matched(submission.selftext, settings)

    if match:
        match = _test_excluded(submission.title, settings)
    if match and submission.is_self:
        match = _test_excluded(submission.selftext, settings)

    return match

