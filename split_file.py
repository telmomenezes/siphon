import json
from datetime import datetime
import gzip


if __name__ == '__main__':
    with open('reddit-submissions.json', 'r') as f:
        for line in f:
            data = json.loads(line)
            ts = data['created_utc']
            month_year = datetime.utcfromtimestamp(ts).strftime('%Y-%m')
            print(month_year)
            outfile = 'reddit-submissions/{}.json.gz'.format(month_year)
            with gzip.open(outfile, 'a') as of:
                of.write('{}\n'.format(json.dumps(data)))
