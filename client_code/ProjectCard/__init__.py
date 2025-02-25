from ._anvil_designer import ProjectCardTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..CommentModal import CommentModal
from ..ProjectView import ProjectView

class ProjectCard(ProjectCardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def open_project_link_click(self, sender, **event_args):
    """This method is called when the link is clicked"""
    get_open_form().select_link_from_card(self.item)

  def comment_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    modal = CommentModal(item=self.item)
    alert(modal, large=True, buttons=[])

  def delete_project_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    x = alert("Are you sure you want to delete this project?", buttons=[("YES", True), ("Cancel", False)])
    if x:
      anvil.server.call('delete_project', self.item)
      open_form('Frame')





