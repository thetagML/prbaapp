from ._anvil_designer import CommentModalTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class CommentModal(CommentModalTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_comment_panel_items()
  
  def refresh_comment_panel_items(self):
    self.comment_panel.items = anvil.server.call('get_comments', self.item)

  def add_comment_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.comment_area.visible = True
    self.add_button.visible = True
    self.add_comment_link.visible = False

  def add_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    comment = self.comment_area.text
    if comment:
      self.comment_area.visible = False
      self.add_button.visible = False
      self.add_comment_link.visible = True
      anvil.server.call('add_comment', comment, self.item)
      self.refresh_comment_panel_items()
      self.comment_area.text = ""
    else:
      #if the add button is clicked when there is no text added, change the textarea to the error role
      self.comment_area.role = "outlined-error"

  def comment_area_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    #if the textarea has the error role but text is added, change it back to normal
    if self.comment_area.text and self.comment_area.role == "outlined-error":
      self.comment_area.role = "outlined"


    

