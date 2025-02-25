from ._anvil_designer import ProjectListTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..ProjectCard import ProjectCard


class ProjectList(ProjectListTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.projects = anvil.server.call('get_projects')
    for project in self.projects:
      self.column_panel_1.add_component(ProjectCard(item=project))


  def create_new_project_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().create_new_click()

