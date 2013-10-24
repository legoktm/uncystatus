#!/usr/bin/env python
"""
Copyright (C) 2013 Legoktm

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

from mtirc import bot
from mtirc import settings
import ast
import tweepy

import config
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)


def gtfo(botobj, channel, user):
        botobj.servers[botobj.config['default_network']].send_raw('KICK %s %s Thoughtcrime detected!' % (channel, user))


def run(**kw):
    kw['bot'].queue_msg('chanserv', 'op ##en-meta')
    if kw['channel'] == config.channel:
        if kw['text'].startswith('!tweet '):
            msg = ' '.join(kw['text'].split(' ')[1:])
            try:
                api.update_status(msg)
                kw['bot'].queue_msg(kw['channel'], 'I tweeted.')
            except tweepy.TweepError, e:
                error = ast.literal_eval(e.reason)
                kw['bot'].queue_msg(kw['channel'], 'OMG ERROR: {0}'.format(error[0]['message']))
        if hasattr(config, 'bad'):
            if kw['sender'].host in config.bad:
                for thingy in config.bad[kw['sender'].host]:
                    sanitised = ''.join(c for c in thingy if ord(c) >= 32)
                    if sanitised.lower() in kw['text'].lower():
                        gtfo(kw['bot'], kw['channel'], kw['sender'].nick)



configuration = settings.config
configuration['connections']['card.freenode.net']['channels'] = [config.channel, '##legoktm-bots-chatter']
configuration['modules']['tweeter'] = run
configuration['authenticate'] = False
configuration['nick'] = 'uncycstatus'
configuration['use_memcache'] = False
b = bot.Bot(configuration)
b.run()
