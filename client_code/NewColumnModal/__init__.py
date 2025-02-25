from ._anvil_designer import NewColumnModalTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..GlobalVars import column_types

class NewColumnModal(NewColumnModalTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #types are Text, Checkbox, Users and Priority
    self.type_dropdown.items = column_types

  def create_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    title = self.title_text_box.text
    type = self.type_dropdown.selected_value
    if title:
      self.raise_event("x-close-alert", value=(title, type))
    else:
      #if no title has been entered, change the role of the textbox to error
      self.title_text_box.role = "input-error"

  def title_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.title_text_box.role == "input-error" and self.title_text_box.text:
        #if the textbox role was error and text is added, change the role back to normal
        self.title_text_box.role = "default"
      

      

