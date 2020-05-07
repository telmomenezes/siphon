import json
from datetime import datetime


if __name__ == '__main__':
    with open('reddit-submissions.json', 'r') as f:
        for line in f:
            data = json.loads(line)
            ts = data['created_utc']
            print(datetime.utcfromtimestamp(ts).strftime('%Y-%m'))
