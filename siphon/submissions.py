import json
from time import time
from datetime import datetime
from pushshift_py import PushshiftAPI


def get_submissions(api, subreddit=None, min_utc=0):
    if subreddit is None:
        gen = api.search_submissions(limit=500, sort='asc', after=min_utc)
    else:
        gen = api.search_submissions(limit=500, sort='asc', after=min_utc,
                                     subreddit=subreddit)
    results = list(result.d_ for result in gen)
    return results


def cur_time(outfile, min_utc=0):
    last_utc = min_utc
    try:
        with open(outfile, 'r') as jsonfile:
            for line in jsonfile:
                data = json.loads(line)
                if 'created_utc' in data:
                    if data['created_utc'] > last_utc:
                        last_utc = data['created_utc']
    except Exception:
        pass
    return last_utc


def retrieve(outfile, subreddit=None, min_utc=0):
    api = PushshiftAPI()
    after = cur_time(outfile, min_utc)
    i = 0
    start_ts = time()
    total_subs = 0
    done = False
    while not done:
        results = get_submissions(api, subreddit=subreddit, min_utc=after)

        if len(results) == 0:
            done = True

        with open(outfile, 'a') as jsonfile:
            for result in results:
                jsonfile.write('{}\n'.format(json.dumps(result)))

        total_subs += len(results)
        for result in results:
            after = result['created_utc']
        dt_object = datetime.fromtimestamp(after)
        delta_t = time() - start_ts
        rate = total_subs / (delta_t / 1440.)
        print('[#{}] {} ({} subs/h)'.format(str(i), dt_object, rate))
        i += 1

    print('Total submissions retrieved: {}'.format(str(total_subs)))
