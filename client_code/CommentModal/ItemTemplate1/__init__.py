from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    

    # Any code you write here will run when the form opens.

  def delete_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.server.call('delete_row', self.item)
    self.parent.parent.refresh_comment_panel_items()



