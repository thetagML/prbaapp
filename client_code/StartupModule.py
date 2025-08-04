import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import anvil.facebook.auth

def startup():
    user = anvil.users.login_with_form()
    open_form("Frame")

startup()