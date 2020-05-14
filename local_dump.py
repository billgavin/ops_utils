from pyswitch import specificdispatch as switch
from ruamel import yaml

import prettytable
import sqlite3
import pickle
import fire
import json
import xlrd
import xlwt
import csv
import os

class LocalDump(object):

    @classmethod
    def dump(cls, data, *titles, path='', dtype='pk'):
        if not path:
            path = f'local_dump.{dtype}'
        path = os.path.abspath(path)
        dirname, fpath = os.path.split(os.path.abspath(path))
        if not os.path.exists(dirname):
            os.makedirs(dirname, 0o600)
        if not os.path.exists(path):
            os.mknod(path, 0o600)
        ld = cls()
        ld._dump(path, data, dtype, *titles)

    @classmethod
    def load(cls, path='', dtype='pk'):
        ld = cls()
        if not path:
            path = f'local_dump.{dtype}'
        path = os.path.abspath(path)
        return ld._load(path, dtype)

    @switch(key=3)
    def _dump(self, path, data, dtype, *titles):
        with open(path, 'wb', encoding='utf-8') as f:
            pickle.dump(data, f)

    @switch(key=2)
    def _load(self, path, dtype):
        with open(path, 'rb', encoding='utf-8') as f:
            return pickle.load(f)

    @_dump.register('db')
    def _(self, path, data, dtype, *titles):
        return f'Path: {path} Titles: {titles} Data: {data} dumps to sqlite3.'

    @_load.register('db')
    def _(self, path, dtype):
        return f'Load data from {path}.'

    @_dump.register('txt')
    def _(self, path, data, dtype, *titles):
        return f'Path: {path} Titles: {titles} Data: {data} dumps to txt file.'

    @_load.register('txt')
    def _(self, path, dtype):
        return f'Load data from {path}.'

    @_dump.register('csv')
    def _(self, path, data, dtype, *titles):
        return f'Path: {path} Titles: {titles} Data: {data} dumps to csv file.'

    @_load.register('csv')
    def _(self, path, dtype):
        return f'Load data from {path}.'

    @_dump.register('xls')
    def _(self, path, data, dtype, *titles):
        return f'Path: {path} Titles: {titles} Data: {data} dumps to xls file.'

    @_load.register('xls')
    def _(self, path, dtype):
        return f'Load data from {path}.'

    @_dump.register('yaml')
    def _(self, path, data, dtype, *titles):
        return f'Path: {path} Titles: {titles} Data: {data} dumps to yaml file.'

    @_load.register('yaml')
    def _(self, path, dtype):
        return f'Load data from {path}.'

    @_dump.register('json')
    def _(self, path, data, dtype, *titles):
        return f'Path: {path} Titles: {titles} Data: {data} dumps to json file.'

    @_load.register('json')
    def _(self, path, dtype):
        return f'Load data from {path}.'


if __name__ == '__main__':
    #LocalDump.dump(11111111111, 'a', 'b', dtype='txt')
    #fire.Fire(LocalDump)
    a = {1:'a', 2:'b', 3:'c'}
    LocalDump.dump(a)
    print(LocalDump.load())
