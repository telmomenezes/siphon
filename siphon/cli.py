import argparse
import time
import calendar
import siphon.submissions as submissions


def ddmmyy2utc(s):
    return calendar.timegm(time.strptime(s, '%d.%m.%Y'))


def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', type=str, help='command to execute')
    parser.add_argument('--outfile', type=str,
                        help='output file', default=None)
    parser.add_argument('--errfile', type=str,
                        help='error file', default='error.log')
    parser.add_argument('--mindate', type=str, help='earliest date for items',
                        default=None)
    parser.add_argument('--subreddit', type=str, help='subreddit name',
                        default=None)

    args = parser.parse_args()

    if args.subreddit:
        print('subreddit: {}'.format(args.subreddit))
    if args.outfile:
        print('output file: {}'.format(args.outfile))

    min_utc = None
    if args.mindate:
        min_utc = ddmmyy2utc(args.mindate)
        print('minimum date: {}'.format(args.mindate))
    else:
        min_utc = 0

    if args.command == 'submissions':
        print('Retrieving reddit submissions...')
        submissions.retrieve(args.outfile, args.subreddit, min_utc)
    else:
        print('Unknown command: {}'.format(args.command))
