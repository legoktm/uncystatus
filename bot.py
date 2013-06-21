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
import tweepy

import config
auth = tweepy.auth.BasicAuthHandler(config.username, config.password)
api = tweepy.API(auth)

def run(**kw):
    if kw['channel'] == config.channel:
        if kw['text'].startswith('!tweet '):
            msg = ' '.join(kw['text'].split(' ')[1:])
            api.update_status(msg)
            kw['bot'].queue_msg('I tweeted.')

configuration = settings.config
configuration['connections']['card.freenode.net']['channels'] = [config.channel, '##legoktm-bots-chatter']
configuration['modules']['tweeter'] = run
configuration['authenticate'] = False
configuration['nick'] = 'uncycstatus'
configuration['use_memcache'] = False
b = bot.Bot(configuration)
b.run()