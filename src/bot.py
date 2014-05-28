import praw

from filters import SubmissionFilter


__version__ = '0.1.1'


class XPostBot(object):
    """ XPostBot - Reddit bot to scan relevant content and repost on specialized subreddits """

    def __init__(self, settings):
        """ create instance of PRAW bot and store settigns """
        self.settings = settings

        full_user_agent = '{user_agent} -- {source} by {author} v{version}'.format(
            user_agent=self.settings['user_agent'],
            source='github.com/git2samus/xpost-bot',
            author='/u/Samus_',
            version=__version__,
        )
        # disable internal cache so praw blocks until it's time to make a new request
        self.bot = praw.Reddit(user_agent=full_user_agent, cache_timeout=0)

    def _submissions_gen(self, target_subreddits, newer_than_id=None):
        """ internal generator for submissions that match the search critetia from settings """
        # construct multireddit url to query from list of target subreddits
        target_multireddit = self.bot.get_subreddit('+'.join(target_subreddits))

        # if there's no anchor get the current newest and continue from there
        if newer_than_id is None:
            submissions = target_multireddit.get_new(limit=1)

            try:
                newer_than_id = next(submissions).name
            except StopIteration:
                # if it's an empty subreddit keep it as None
                # brings everything that gets posted from here until the next request
                pass

        next_anchor_id = None

        while True:
            # uses "before" API param because /new lists from newest to oldest
            # limit=None brings everything that matches (even if it takes multiple requests)
            submissions = target_multireddit.get_new(params={'before': newer_than_id}, limit=None)

            for submission in submissions:
                yield submission

                # save the first id as anchor since it'll be the newest
                if next_anchor_id is None:
                    next_anchor_id = submission.name

            # avoid getting newer_than_id=None when there's no results from the previous iterations
            if next_anchor_id is not None:
                newer_than_id, next_anchor_id = next_anchor_id, None

    def is_logged_in(self):
        """ proxy to PRAW is_logged_in flag """
        return self.bot.is_logged_in()

    def login(self):
        """ perform login to reddit using user-credentials (not OAuth) """
        bot_username = self.settings['bot_username']
        bot_password = self.settings['bot_password']

        self.bot.login(bot_username, bot_password)

    def get_submissions(self, newer_than_id=None):
        """ main method to retrieve matching submissions (yields indefinitely) """
        target_subreddits = self.settings['target_subreddits']
        submissions_gen = self._submissions_gen(target_subreddits, newer_than_id)

        submission_filter = SubmissionFilter(self.settings)
        return submission_filter.filter_stream(submissions_gen)

    def repost_submission(self, submission):
        subreddit = self.bot.get_subreddit(self.settings['destination_subreddit'])

        title = self.settings['title_template'].format(s=submission)
        try:
            return subreddit.submit(
                title, url=submission.permalink, raise_captcha_exception=True
            )
        except praw.errors.AlreadySubmitted:
            pass

