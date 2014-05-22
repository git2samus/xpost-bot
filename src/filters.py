import re


def _test_matched(text, settings):
    keywords, regexps = settings['matched_keywords'], settings['matched_regexps']

    text = text.lower()
    return any(
        keyword.lower() in text for keyword in keywords
    ) or any(
        regexp.search(text, re.IGNORECASE) for regexp in regexps
    )


def _test_excluded(text, settings):
    keywords, regexps = settings['excluded_keywords'], settings['excluded_regexps']

    text = text.lower()
    return not any(
        keyword.lower() in text for keyword in keywords
    ) and not any(
        regexp.search(text, re.IGNORECASE) for regexp in regexps
    )


def filter_submission(submission, settings):
    match = _test_matched(submission.title, settings)
    if not match and submission.is_self:
        match = _test_matched(submission.selftext, settings)

    if match:
        match = _test_excluded(submission.title, settings)
    if match and submission.is_self:
        match = _test_excluded(submission.selftext, settings)

    return match

