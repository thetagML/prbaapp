import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

#users is a list of tuples: [(email, name), (email, name)...]
user_emails, user_colors = anvil.server.call('get_user_emails_and_colors')

column_types = ['Text', 'Checkbox', 'Priority', 'Users']

priority_items = ['Low', 'Medium', 'High']

priority_colors = {
      'Low': '#2DAF88',
      'Medium': '#F6CA57',
      'High': '#D64045'
    }
