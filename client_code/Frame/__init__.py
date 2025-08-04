from ._anvil_designer import FrameTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..ProjectView import ProjectView
from ..ProjectList import ProjectList
import anvil.js
from anvil.js.window import jQuery

class Frame(FrameTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        #self.content_panel.add_component(ProjectList())
        #self.add_project_links()

        jQuery( "#anvil-header" ).remove()

    def form_show(self, **event_args):
      """This method is called when the HTML panel is shown on the screen"""
      jQuery( ".app-bar" ).css( "top", "0px" )
      jQuery( ".content" ).css( "margin-top", "9px" )
      jQuery( ".sidebar-toggle" ).css( "margin-top", "0px" )
      jQuery( ".title.anvil-inline-container div" ).css( "margin-top", "0px" )


      #move to the bottom
      el = anvil.js.get_dom_node( self.create_new )
      el.parentElement.parentElement.parentElement.parentElement.parentElement.style.position = "absolute"
      el.parentElement.parentElement.parentElement.parentElement.parentElement.style.bottom = "0"
  
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

    def desktops_menu_click(self, sender, **event_args):
        """This method is called when the link is clicked"""
        for link in self.link_panel.get_components():
            link.role = ""
        self.content_panel.clear()
        self.content_panel.add_component(ProjectList())

    def logout_link_click(self, **event_args):
        """This method is called when the link is clicked"""
        anvil.users.logout()
        open_form('LogoutScreen')



