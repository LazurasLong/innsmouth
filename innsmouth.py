import sys
import random
import datetime
from twisted.internet import task
from twisted.internet import reactor
from twython import Twython
from os import environ
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

TIMEOUT = datetime.timedelta(days=13).seconds
twitter = Twython(CONSUMER_KEY,
                  CONSUMER_SECRET,
                  ACCESS_KEY,
                  ACCESS_SECRET)


def reservoir(iterator):
    """Select item from iterator.
    Reservoir algorithm from http://stackoverflow.com/a/3540315/250241/
    """
    select = next(iterator)
    for num, item in enumerate(iterator):
        if random.randrange(num + 2):
            continue
        select = item
    return select


def get_line(file_name):
    """Open file and select tweetable line."""
    with open(file_name) as open_file:
        while True: # Loop until an appropriate sentence is found
            open_file.seek(0)  # reset file iterator to 0
            line = reservoir(open_file).strip().replace("  ", " ")
            if line[0].isupper() and 4 < len(line) < 140:
                return line


def tweet(sentence):
    """Tweet sentence to Twitter."""
    try:
        sys.stdout.write("{} {}\n".format(len(sentence), sentence))
        twitter.update_status(status=sentence)
    except:
        pass


def do_tweet(file_name):
    """Get line and tweet it"""
    line = get_line(file_name)
    tweet(line)


if __name__ == '__main__':
    file_name = str(sys.argv[1])
    l = task.LoopingCall(do_tweet, file_name)
    l.start(TIMEOUT)
    reactor.run()
