import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

USER_COLORS = ['Primary', 'Secondary', 'Tertiary', 'Primary Container', 'On Secondary Container']

@anvil.server.callable(require_user=True)
def add_project_to_table(project_name):
  project_row = app_tables.projects.add_row(project_name=project_name)
  project_row['columns'] = []
  #init the table with predefined columns
  add_column_to_db('Task Name', project_row, "Text") 
  add_column_to_db('Priority', project_row, "Priority")
  add_column_to_db('Done', project_row, "Checkbox") 
  #add an empty row to new project
  row_data = {row.get_id(): '' for row in project_row['columns']}
  add_row_to_rows(project_row, row_data)
  return project_row

@anvil.server.callable(require_user=True)
def add_column_to_db(column_name, project, type):   
  column_row = app_tables.columns.add_row(title=column_name, type=type)
  project['columns'] += [column_row]
  return column_row

@anvil.server.callable(require_user=True)
def get_projects():
  return app_tables.projects.search()

@anvil.server.callable(require_user=True)
def change_project_name(row, new_name):
  row['project_name'] = new_name
  row['project_name'] = row['project_name']

@anvil.server.callable(require_user=True)
def change_cell_value(row, column_id, new_text):
  row['data'] = {**row['data'], column_id: new_text}
  
@anvil.server.callable(require_user=True)
def get_rows(project):
  return app_tables.rows.search(project=project)

@anvil.server.callable(require_user=True)
def add_row_to_rows(project, row_data):
  app_tables.rows.add_row(project=project, data=row_data)

# @anvil.server.callable(require_user=True)
# def get_columns(project):
#   return app_tables.projects.search(project=project)

@anvil.server.callable(require_user=True)
def change_column_title(column_id, new_title):
  app_tables.columns.get(id=column_id)['title'] = new_title

@anvil.server.callable(require_user=True)
def delete_row(row):
  if row is not None:
    row.delete()

@anvil.server.callable(require_user=True)
def delete_column(row, project):
  #row is a row from the columns data table
  if row is not None:
    #remove columns from project data table
    columns = project['columns']
    columns.remove(row)
    project['columns'] = columns
    #remove from columns data table
    row.delete()

@anvil.server.callable(require_user=True)
def get_column_types():
  return app_tables.types.search()

@anvil.server.callable(require_user=True)
def get_comments(project):
  return app_tables.comments.search(project=project)

@anvil.server.callable(require_user=True)
def add_comment(comment, project):
  app_tables.comments.add_row(comment=comment, user=anvil.users.get_user(), project=project)

@anvil.server.callable(require_user=True)
def delete_comment(row):
  if row is not None:
    row.delete()
    
@anvil.server.callable(require_user=True)
def get_user_emails_and_colors():
  users = app_tables.users.search()
  emails = [user['email'] for user in users]
  colors = {user['email']: f"theme:{user['color']}" for user in users}
  return emails, colors 

@anvil.server.callable(require_user=True)
def add_user_color():
  user_row = anvil.users.get_user()
  num_of_users = len(app_tables.users.search())
  user_row['color'] = USER_COLORS[num_of_users%5]

@anvil.server.callable(require_user=True)
def delete_project(project_row):
  if project_row is not None:
    for col in project_row['columns']:
      #delete the columns in the columns data table
      col.delete()
    for row in app_tables.rows.search(project=project_row):
      #delete the rows in the rows data table
      row.delete()
    #delete the actual project row
    project_row.delete()
    
    
    