import json

def processfile(inname, outname):
    f2 = open(outname, 'a')
    with open(inname) as f:
        for line in f:
            data = json.loads(line)
            if data['rtds_tweet']['yst_tweet_language']=='en':
                output = dict()
                output['text'] = data['rtds_tweet']['text']
                output['timestamp'] = data['rtds_tweet']['created_at_timestamp']
                output['id'] = data['self']['_id']
                f2.write(json.dumps(output) + '\n')
    f2.close()

if __name__ == "__main__":
    inname = 'twitterlogs/msg4_twitter.10136.log_1372176300'
    outname = 'processesTweets.txt'
    processfile(inname, outname)