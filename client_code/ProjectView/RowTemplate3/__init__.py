from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...EditableLink import EditableLink
from ...TagComponent import TagComponent
from ...GlobalVars import user_colors, user_emails, priority_items, priority_colors


class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #self.data is the row data from the rows data table, self.schema is the columns for the project
    self.data = self.item['data']
    self.schema = self.item['project']['columns']
    for col in self.schema:
      column_id = col.get_id()
      #if the column is a text type, add an EditableLink
      if col['type'] == 'Text':
        editable_link = EditableLink(text=self.data.get(column_id))
        editable_link.tag = column_id
        editable_link.add_event_handler('x-change-text', self.change_text)
        self.add_component(editable_link, column=column_id)
      #elif the column is a checkbox type, add a checkbox and set up an event handler to save the value
      elif col['type'] == 'Checkbox':
        c = CheckBox(checked=self.data.get(column_id), tag=column_id, align="center")
        c.add_event_handler("change", self.save_checkbox_value)
        self.add_component(c, column=column_id)
      #elif the column is a users type, add a  TagComponent with user emails and colors
      elif col['type'] == 'Users':
        u = TagComponent(row=self.item, column_id=column_id, text=self.data.get(column_id), items=user_emails, colors=user_colors)
        self.add_component(u, column=column_id)
      #elif the column is a priority type, add a TagComponent with priority levels and colors
      elif col['type'] == 'Priority':
        p = TagComponent(row=self.item, column_id=column_id, text=self.data.get(column_id), items=priority_items, colors=priority_colors)
        self.add_component(p, column=column_id)
        
    #add a delete link in the final column. it's only visible when its container is hovered
    cp = ColumnPanel(spacing_above="none", spacing_below="none", role="visible-hover-only")
    self.delete_row_link = Link(icon="fa:trash", text="Delete Row", role="delete-link", foreground=app.theme_colors['Secondary'])
    cp.add_component(self.delete_row_link)
    self.add_component(cp, column="Add New")

    self.delete_row_link.add_event_handler("click", self.delete_row)

  def delete_row(self, **event_args):
    anvil.server.call("delete_row", self.item)
    #raising the x-delete-row event calls the add_data_to_grid function in ProjectView
    self.parent.raise_event("x-delete-row")

  def save_checkbox_value(self, sender, **event_args):
    #sender.tag is the column_id
    anvil.server.call("change_cell_value", self.item, sender.tag, sender.checked)

  def change_text(self, sender, text, **event_args):
    #sender.tag is the column_id
    anvil.server.call('change_cell_value', self.item, sender.tag, text)

    
    
    
      
      
    