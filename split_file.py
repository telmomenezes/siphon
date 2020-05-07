import json
from datetime import datetime
import gzip


if __name__ == '__main__':
    with open('reddit-submissions.json', 'r') as f:
        last_month_year = None
        of = None
        for line in f:
            data = json.loads(line)
            ts = data['created_utc']
            month_year = datetime.utcfromtimestamp(ts).strftime('%Y-%m')
            if last_month_year != month_year:
                if of:
                    of.close()
                outfile = 'reddit-submissions/{}.json.gz'.format(month_year)
                of = gzip.open(outfile, 'at')
                last_month_year = month_year
            of.write('{}\n'.format(json.dumps(data)))
        of.close()
