# lshash/storage.py
# Copyright 2012 Kay Zhu (a.k.a He Zhu) and contributors (see CONTRIBUTORS.txt)
#
# This module is part of lshash and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import json
try:
    import redis
except ImportError:
    redis = None

__all__ = ['storage']


def storage(storage_config, index):
    """ Given the configuration for storage and the index, return the
    configured storage instance.
    """
    if 'queue' in storage_config:
        return QueueDictStorage(storage_config['queue'])
    elif 'dict' in storage_config:
        return InMemoryStorage(storage_config['dict'])
    elif 'redis' in storage_config:
        storage_config['redis']['db'] = index
        return RedisStorage(storage_config['redis'])
    else:
        raise ValueError("Only in-memory dictionary and Redis are supported.")

class queueStorage(object):
    def __init__(self, maxsize = 100):
        self.queuesize = maxsize
        self.start = 0
        self.end = 0
        self.isFull = False
        self.isEmpty = True
        self.queue= [0 for i in range(maxsize)]
    def put(self, val):
        if self.isFull == True:
            return -1
        self.queue[self.end] = val
        self.end = (self.end + 1) % self.queuesize
        if self.end == self.start:
            self.isFull = True
        self.isEmpty = False
    
    def get(self):
        if self.isEmpty == True:
            return -1
        t = self.queue[self.start]
        self.start = (self.start + 1) % self.queuesize
        if self.start == self.end:
            self.isEmpty = True
        self.isFull = False
        return t
    
    def getArray(self):
        if self.start <= (self.end-1):
            a = self.queue[self.start:self.end]
        else:
            a = self.queue[self.start:] + self.queue[:self.end]
        return a

class BaseStorage(object):
    def __init__(self, config):
        """ An abstract class used as an adapter for storages. """
        raise NotImplementedError

    def keys(self):
        """ Returns a list of binary hashes that are used as dict keys. """
        raise NotImplementedError

    def set_val(self, key, val):
        """ Set `val` at `key`, note that the `val` must be a string. """
        raise NotImplementedError

    def get_val(self, key):
        """ Return `val` at `key`, note that the `val` must be a string. """
        raise NotImplementedError

    def append_val(self, key, val):
        """ Append `val` to the list stored at `key`.

        If the key is not yet present in storage, create a list with `val` at
        `key`.
        """
        raise NotImplementedError

    def get_list(self, key):
        """ Returns a list stored in storage at `key`.

        This method should return a list of values stored at `key`. `[]` should
        be returned if the list is empty or if `key` is not present in storage.
        """
        raise NotImplementedError


class InMemoryStorage(BaseStorage):
    def __init__(self, config):
        self.name = 'dict'
        self.storage = dict()

    def keys(self):
        return self.storage.keys()

    def set_val(self, key, val):
        self.storage[key] = val

    def get_val(self, key):
        return self.storage[key]

    def append_val(self, key, val):
        self.storage.setdefault(key, []).append(val)

    def get_list(self, key):
        return self.storage.get(key, [])


class RedisStorage(BaseStorage):
    def __init__(self, config):
        if not redis:
            raise ImportError("redis-py is required to use Redis as storage.")
        self.name = 'redis'
        self.storage = redis.StrictRedis(**config)

    def keys(self, pattern="*"):
        return self.storage.keys(pattern)

    def set_val(self, key, val):
        self.storage.set(key, val)

    def get_val(self, key):
        return self.storage.get(key)

    def append_val(self, key, val):
        self.storage.rpush(key, json.dumps(val))

    def get_list(self, key):
        return self.storage.lrange(key, 0, -1)

class QueueDictStorage(BaseStorage):
    def __init__(self, config):
        self.name = 'queuedict'
        self.storage = dict()
        self.queue_size = config

    def keys(self):
        return self.storage.keys()

    def set_val(self, key, val):
        self.storage[key] = queueStorage(maxsize = self.queue_size)
        self.storage[key].put(val)
    
    def get_val(self, key):
        return self.storage.get(key)

    def append_val(self, key, val):
        self.storage.setdefault(key, queueStorage(maxsize = self.queue_size))
        if self.storage[key].isFull:
            self.storage[key].get()
        self.storage[key].put(val)

    def get_list(self, key):
        r = self.storage.get(key)
        if r == None:
            return []
        return r.getArray()

if __name__ == '__main__':
    a = queueStorage(maxsize = 2)
    a.put('a')
    a.put('b')
    
