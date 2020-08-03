import os
import glob
import json
import gzip
from time import time
from datetime import datetime
from pushshift_py import PushshiftAPI


def get_submissions(api, subreddit=None, min_utc=0):
    if subreddit is None:
        gen = api.search_submissions(limit=5000, sort='asc', after=min_utc)
    else:
        gen = api.search_submissions(limit=5000, sort='asc', after=min_utc,
                                     subreddit=subreddit)
    results = list(result.d_ for result in gen)
    return results


def cur_time_file(outfile, min_utc=0):
    last_utc = min_utc
    try:
        with gzip.open(outfile, 'rt') as jsonfile:
            for line in jsonfile:
                data = json.loads(line)
                if 'created_utc' in data:
                    if data['created_utc'] > last_utc:
                        last_utc = data['created_utc']
    except Exception:
        pass
    dt = datetime.utcfromtimestamp(last_utc).strftime('%Y-%m-%d %H:%M:%S')
    print('current time: {}'.format(dt))
    return last_utc


def cur_file(outdir):
    file_names = glob.glob(os.path.join(outdir, '*.json.gz'))
    for file_name in file_names:
        max_date_month = 0
        latest_file = None
        base = os.path.basename(file_name)
        base = base.split('.')[0]
        date_month = int(base.replace('-', ''))
        if date_month > max_date_month:
            max_date_month = date_month
            latest_file = file_name
    print('latest_file: {}'.format(latest_file))
    return latest_file


def cur_time_dir(outdir, min_utc=0):
    outfile = cur_file(outdir)
    return cur_time_file(outfile)


def retrieve_to_file(outfile, subreddit=None, min_utc=0):
    api = PushshiftAPI()
    after = cur_time_file(outfile, min_utc)
    i = 0
    start_ts = time()
    total_subs = 0
    done = False
    while not done:
        results = get_submissions(api, subreddit=subreddit, min_utc=after)

        if len(results) == 0:
            done = True

        with gzip.open(outfile, 'at') as jsonfile:
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


def retrieve_to_dir(outdir, subreddit=None, min_utc=0):
    api = PushshiftAPI()
    after = cur_time_dir(outdir, min_utc)
    i = 0
    start_ts = time()
    total_subs = 0
    done = False
    last_month_year = None
    jsonfile = None
    while not done:
        results = get_submissions(api, subreddit=subreddit, min_utc=after)

        if len(results) == 0:
            done = True

        for result in results:
            ts = result['created_utc']
            month_year = datetime.utcfromtimestamp(ts).strftime('%Y-%m')
            if month_year != last_month_year:
                outfile = os.path.join(outdir, '{}.json.gz'.format(month_year))
                if jsonfile:
                    jsonfile.close()
                jsonfile = gzip.open(outfile, 'at')
                last_month_year = month_year

            jsonfile.write('{}\n'.format(json.dumps(result)))

        total_subs += len(results)
        for result in results:
            after = result['created_utc']
        dt_object = datetime.fromtimestamp(after)
        delta_t = time() - start_ts
        rate = total_subs / (delta_t / 1440.)
        print('[#{}] {} ({} subs/h)'.format(str(i), dt_object, rate))
        i += 1

    jsonfile.close()

    print('Total submissions retrieved: {}'.format(str(total_subs)))
