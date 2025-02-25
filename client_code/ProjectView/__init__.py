from ._anvil_designer import ProjectViewTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..EditableLink import EditableLink
from ..NewColumnModal import NewColumnModal


class ProjectView(ProjectViewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #set self.project and self.columns
    self.editable_project_name.add_event_handler("x-change-text", self.change_project_name)
    self.get_project_and_columns()

    self.add_new_column_link = Link(text="New Column", icon="fa:plus", spacing_above="small", spacing_below="none")
    self.add_new_column_link.add_event_handler('click', self.add_new_column_link_click)

    #set up the Data Grid
    self.add_data_to_grid()
    self.create_header_row()
    self.repeating_panel_1.add_event_handler("x-delete-row", self.add_data_to_grid)

  def get_project_and_columns(self):
    #self.item is a row from the projects table
    self.project = self.item
    self.project.update()
    self.columns = self.project['columns']
    
  def add_data_to_grid(self, **event_args):
    #reset self.project and self.columns in case data has changed since form init
    self.get_project_and_columns()
    cols = [{'id':row.get_id(), 'title':row['title'], 'data_key':row.get_id()} for row in self.columns]
    #add "New" column for the add new column link 
    cols.append({'id': 'Add New', 'title': '+ New Column'})
    #set the Data Grid columns to None then set them to our custom columns
    # self.data_grid_1.columns = None
    self.data_grid_1.columns = cols
    #populate repeating panel with row data in Rows Data Table
    self.rows = anvil.server.call('get_rows', self.project)
    self.repeating_panel_1.items = [row for row in self.rows]

  def create_header_row(self):
    #auto header is turned off so that I can add links to the header
    self.header_row_panel = DataRowPanel(role="tonal-data-row-header")
    #loop through columns and add an EditableLink and a delete link for each column title
    for row in self.columns:
      self.create_header_link(row)
    
    #add link to end of data grid to add a new column
    self.header_row_panel.add_component(self.add_new_column_link, column="Add New")
    #add header panel to data grid at the top
    self.data_grid_1.add_component(self.header_row_panel, index=0)

  def create_header_link(self, row):
    #put the EditableLink and delete link in a flow panel
    flow_panel = FlowPanel(role="visible-hover-only", spacing_above="none", spacing_below="none")
    editable_link = EditableLink(text=row["title"], column_id=row.get_id(), type="header")
    #need text = " " to make icon align properly
    delete_column_link = Link(icon="fa:trash", text=" ", icon_align="left", tag=row, role="delete-link", foreground=app.theme_colors['Secondary'])
    delete_column_link.add_event_handler("click", self.delete_column_link_click)
    flow_panel.add_component(editable_link)
    flow_panel.add_component(delete_column_link)
    self.header_row_panel.add_component(flow_panel, column=row.get_id())
    
  def add_new_column_link_click(self, **event_args):
    #present a popup ask the type and title of the new column
    new_column_modal = NewColumnModal()
    new_column_alert = alert(new_column_modal, large=True, buttons=None)
    if new_column_alert:
      #type is either 'Text', 'Checkbox', 'Users' or 'Priority'
      title, type = new_column_alert
      #add new row to columns data table and return the id of that row
      column_row = anvil.server.call('add_column_to_db', title, self.project, type)
      #add empty strings to the rows Data Table for the new column
      # anvil.server.call('add_empty_string_to_rows', self.rows, column_row.get_id())
      self.add_data_to_grid()
      self.create_header_link(column_row)

  def change_project_name(self, text, **event_args):
    """This method is called when enter is pressed in the project-name TextBox"""
    #check if the name has actually changed
    if text != self.project['project_name']:
      anvil.server.call('change_project_name', row=self.item, new_name=text)
      get_open_form().add_project_links()

  def add_new_row_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    row_data = {row.get_id(): '' for row in self.columns}
    #add the new row to the data table
    anvil.server.call('add_row_to_rows', self.project, row_data)
    self.repeating_panel_1.items = [row for row in anvil.server.call('get_rows', self.project)]

  def delete_column_link_click(self, sender, **event_args):
    #sender is the delete_link which has a tag prop which is the row from columns Data Table
    anvil.server.call('delete_column', sender.tag, self.project)
    self.add_data_to_grid()
    self.header_row_panel.clear()
    self.header_row_panel.remove_from_parent()
    self.create_header_row()
    




