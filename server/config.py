import os

class Config(object):
  JM_ACCT = os.environ.get('JM_ACCT') or ""
  JM_COOKIE = os.environ.get('JM_COOKIE') or ""
  DIV_ACCT = os.environ.get('DIV_ACCT') or ""
  DIV_COOKIE = os.environ.get('DIV_COOKIE') or ""