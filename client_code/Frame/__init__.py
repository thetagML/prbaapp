from ._anvil_designer import FrameTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..ProjectView import ProjectView
from ..ProjectList import ProjectList



class Frame(FrameTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.content_panel.add_component(ProjectList())
    # anvil.users.login_with_form()
    # anvil.server.call('add_color_to_user')
    self.add_project_links()
    
    
  def add_project_links(self):
    self.link_panel.clear()
    for row in anvil.server.call('get_projects'):
      link = Link(text=row["project_name"], tag=row)
      link.set_event_handler("click", self.select_link)
      self.link_panel.add_component(link)

  def create_new_click(self, **event_args):
    """This method is called when the link is clicked"""
    #add a row to the projects table and return the row
    new_project_row = anvil.server.call('add_project_to_table', project_name="New Project")
    #create a link for the left nav
    new_project_link = Link(text=new_project_row['project_name'], tag=new_project_row)
    new_project_link.set_event_handler("click", self.select_link)
    self.link_panel.add_component(new_project_link)
    #open the new project once the link is created
    self.select_link(sender=new_project_link)
    
  def open_project(self, project):
    self.content_panel.clear()
    self.content_panel.add_component(ProjectView(item=project))
      
  def select_link(self, sender, **event_args):
    for link in self.link_panel.get_components():
      link.role = ""
    sender.role = "selected"
    self.open_project(sender.tag)

  def select_link_from_card(self, project):
    for link in self.link_panel.get_components():
      link.role = ""
      if link.tag == project:
        link.role = "selected"
    self.open_project(project)

  def projects_menu_click(self, sender, **event_args):
    """This method is called when the link is clicked"""
    for link in self.link_panel.get_components():
      link.role = ""
    self.content_panel.clear()
    self.content_panel.add_component(ProjectList())

  def logout_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.users.logout()
    open_form('LogoutScreen')


