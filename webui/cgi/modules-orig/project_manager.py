
import orchestration_helper

def load_project_data(project_name):
    """
    Load project data from properties file
    """    
      
    identity_domain = None
    username = None
    image_name = None
    os_project_name = None 
    os_image_name = None
    data_type = "project"
    
    
    identity_domain = orchestration_helper.get_config_item(project_name, project_name, 'identity_domain', data_type)
    username = orchestration_helper.get_config_item(project_name, project_name, 'username', data_type)
    image_name = orchestration_helper.get_config_item(project_name, project_name, 'image_name', data_type)
    os_project_name = orchestration_helper.get_config_item(project_name, project_name, 'openstack_project', data_type)
    os_image_name = orchestration_helper.get_config_item(project_name, project_name, 'openstack_image_name', data_type)
    
    return identity_domain, username, image_name, os_project_name, os_image_name
