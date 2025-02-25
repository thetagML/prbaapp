from ._anvil_designer import EditableLinkTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class EditableLink(EditableLinkTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    self.link_1.text = self.text
    if self.font_size:
      self.link_1.font_size = self.font_size
    self.text_box_1.font_size = self.font_size
      
  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.link_1.visible = False
    self.text_box_1.visible = True
    self.text_box_1.focus()
    self.text_box_1.text = self.text

  def save_text(self, **event_args):
    if self.text_box_1.text != self.text:
      self.raise_event('x-change-text', text=self.text_box_1.text)
      self.text = self.text_box_1.text
      self.link_1.text = self.text
    self.link_1.visible = True
    self.text_box_1.visible = False

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.save_text()

  def text_box_1_lost_focus(self, sender, **event_args):
    """This method is called when the TextBox loses focus"""
    self.save_text()






