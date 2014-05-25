class SubmissionFilter(object):
    """ methods to determine whether a submission is relevant for reposting """

    def __init__(self, settings):
        """ store settings """
        self.settings = settings

    def _is_valid_submitter(self, submission):
        """ returns True when the submission isn't from an ignored submitter or the submitter deleted his account """
        ignored_submitters = self.settings['ignored_submitters']

        if not submission.author:
            return True # allow [deleted]

        author_name = submission.author.name.lower()
        return author_name not in ignored_submitters

    def _is_valid_subreddit(self, submission):
        """ returns True when the submission hasn't been done on an ignored subreddit """
        ignored_subreddits = self.settings['ignored_subreddits']

        subreddit_name = submission.subreddit.display_name.lower()
        return subreddit_name not in ignored_subreddits

    def _test_text(self, text, target_keywords=None, target_regexps=None):
        """ returns True when 'text' contains any of the target_keywords or matches any of the target_regexps """
        target_keywords = [] if target_keywords is None else target_keywords
        target_regexps  = [] if target_regexps  is None else target_regexps

        text = text.lower()
        return any(
            keyword in text for keyword in target_keywords
        ) or any(
            regexp.search(text) for regexp in target_regexps
        )

    def _test_matches(self, submission):
        """ returns True when the submission's title or selftext contains any of the matched_keywords or matches any of the matched_regexps """
        matched_keywords = self.settings['matched_keywords']
        matched_regexps  = self.settings['matched_regexps']

        match = self._test_text(submission.title, matched_keywords, matched_regexps)
        if not match and submission.is_self:
            match = self._test_text(submission.selftext, matched_keywords, matched_regexps)

        return match

    def _test_exclusions(self, submission):
        """ returns True when the submission's title or selftext contains any of the excluded_keywords or matches any of the excluded_regexps """
        excluded_keywords = self.settings['excluded_keywords']
        excluded_regexps  = self.settings['excluded_regexps']

        excluded = self._test_text(submission.title, excluded_keywords, excluded_regexps)
        if not excluded and submission.is_self:
            excluded = self._test_text(submission.selftext, excluded_keywords, excluded_regexps)

        return excluded

    def filter_submission(self, submission):
        """ determine whether this submission should be filtered or not, returns True when the sumission:
             -isn't from an ignored submitter
             -hasn't been posted on an ignored subreddit
             -contains any of the matched_keywords or matches any of the matched_regexps
             -doesn't contain any of the excluded_keywords or matches any of the excluded_regexps
        """
        return all((
            self._is_valid_submitter(submission),
            self._is_valid_subreddit(submission),
            self._test_matches(submission),
            not self._test_exclusions(submission),
        ))

    def filter_stream(self, stream):
        """ apply self.filter_submission to each element of the stream """
        for submission in stream:
            if self.filter_submission(submission):
                yield submission

