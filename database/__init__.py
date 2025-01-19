import dataset
import datetime
import requests
import asyncio
from bs4 import BeautifulSoup
from util import PrintBox, getName

log = PrintBox(title="DATABASE", border_style="green")
  

class Thread:
  def __init__(self, thread_id):
    self._connect = dataset.connect('sqlite:///database/threads.db')
    self.db = self._connect[thread_id]
  
  def insert(self, data):
    self.db.insert(data)
  
  def find(self, *_clause, **kwargs):
    return self.db.find(*_clause, **kwargs)
  
  def find_one(self, *arg, **kwarg):
    return self.db.find_one(*arg, **kwarg)
  
  def update(self, row, keys):
    self.db.update(row, keys)


class Database:
  def __init__(self, table):
    self._connect = dataset.connect('sqlite:///database/database.db')
    self.db = self._connect[table]
  
  def insert(self, data):
    self.db.insert(data)
  
  def find(self, *_clause, **kwargs):
    return self.db.find(*_clause, **kwargs)
  
  def find_one(self, *arg, **kwarg):
    return self.db.find_one(*arg, **kwarg)
  
  def update(self, row, keys):
    self.db.update(row, keys)
  
  def upsert(self, row, keys):
    self.db.upsert(row, keys)


class User(Database):
  def __init__(self):
    super().__init__('users')
  
  def _new(self, uid, name):
    self.upsert(dict(
      uid = uid,
      name = name,
      points = 0, # Coming soon
      money = 200, # Bank system
    ), ['uid'])
    log.border_style = 'green'
    log.message(f"New user - [yellow]{uid}[/yellow] | [yellow]{name}[/yellow]")
  
  def get(self, uid):
    user = self.find_one(uid=uid)
    return user
  def add(self, uid, name='Facebook User'):
    if not self.get(uid):
      if name == 'Facebook User':
        name = getName(uid)
      self._new(uid, name)

class Bank(User):
  def __init__(self, uid):
    super().__init__()
    self.uid = uid
    if not self.get(self.uid):
      self.add(self.uid)
  @property
  def balance(self):
    user = self.get(self.uid)
    return user.get('money', 0)
  
  def add_money(self, amount:int):
    prev = self.balance
    if not isinstance(amount, int):
      print("\033[91m[BANK] \033[0mInvalid argument")
      return prev
    if amount <= 0:
      print("\033[91m[BANK] \033[0mInvalid amount of money")
      return prev
    self.upsert(dict(uid=self.uid,money=prev+amount), ['uid'])
    return prev + amount
  
  def sub_money(self, amount:int):
    prev = self.balance
    if not isinstance(amount, int):
      print("\033[91m[BANK] \033[0mInvalid argument")
      return prev
    if amount > prev:
      print(f"\033[91m[BANK] \033[0mCurrent money is not enough to subtract by {amount}")
      return prev
    self.upsert(dict(uid=self.uid,money=prev-amount), ['uid'])
    return prev - amount