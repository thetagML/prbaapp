from ._anvil_designer import TagComponentTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TagComponent(TagComponentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.drop_down_1.items = self.items
    if self.text:
      self.tag_link.text = self.text
      self.drop_down_1.selected_value = self.text
      #set the background of the priority tag based on the text
      self.tag_link.background = self.colors[self.text]
      
  def tag_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.container_link.visible = False
    self.drop_down_1.visible = True

  def container_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.tag_link_click()

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    self.text = self.drop_down_1.selected_value
    if self.text:
      self.tag_link.background = self.colors[self.text]
      self.tag_link.text = self.text
      anvil.server.call('change_cell_value', self.row, self.column_id, self.text)
    else:
      anvil.server.call('change_cell_value', self.row, self.column_id, "")
      self.tag_link.text = self.text
    self.container_link.visible = True
    self.drop_down_1.visible = False

