import unittest
import sys
sys.path.append('../')

from app import get_submissions

class TestSubmission(unittest.TestCase):

    def test_return_is_not_none(self):
        """ Test wheter return is not None."""
        submissions = get_submissions(['learnpython'], 'day', 1)
        self.assertIsNotNone(submissions)

        submissions = get_submissions('learnpython', 'day', 5)
        self.assertIsNotNone(submissions)

    def test_string_argument(self):
        """ Test wheter return contain one tuple when the argument 'subreddit_names'
            is a type of string."""
        submissions = get_submissions('learnpython', 'day', 1)
        self.assertEqual(len(submissions), 1)

    def test_list_argument(self):
        """ Test wheter return contain proper number of tuples when the argument
            'subreddit_names' is a type of list."""

        submissions = get_submissions(['learnpython'], 'day', 1)
        self.assertEqual(len(submissions), 1)

        submissions = get_submissions(['learnpython', 'videos'], 'week', 1)
        self.assertEqual(len(submissions), 2)

        submissions = get_submissions(['videos', 'wtf', 'all'], 'week', 1)
        self.assertEqual(len(submissions), 3)

    def test_number_of_submissions(self):
        """ Test wheter return contain proper number of submissions."""

        submissions = get_submissions('videos', 'day', 10)
        self.assertEqual(len(list(submissions[0][1])), 10)

        submissions = get_submissions('videos', 'week', 10)
        self.assertEqual(len(list(submissions[0][1])), 10)

        submissions = get_submissions(['videos'], 'day', 10)
        self.assertEqual(len(list(submissions[0][1])), 10)

        submissions = get_submissions(['videos'], 'week', 10)
        self.assertEqual(len(list(submissions[0][1])), 10)

        submissions = get_submissions(['videos', 'learnpython'], 'week', 10)
        self.assertEqual(len(list(submissions[0][1])), 10)
        self.assertEqual(len(list(submissions[1][1])), 10)


if __name__ == '__main__':
    unittest.main()
