import ckan.plugins.toolkit as toolkit
import ckan.logic.action as actions
from ckan.plugins.toolkit import chained_action, get_action, enqueue_job

def get_resource_name(resource_name):
    splited_resource_name = resource_name.split('.')
    if len(splited_resource_name) > 1:
        return splited_resource_name[0] 
    return resource_name

def create_alias(resource_id, context):
    resource_info = get_action('resource_show')(None, { 'id': resource_id })
    get_action('datastore_create')(context, { 'resource_id': resource_id, 'aliases': get_resource_name(resource_info['name']), 'force': True})

@chained_action
def datastore_create(original_action, context, data_dict):
    result = original_action(context, data_dict)                                                        
    if "aliases" not in data_dict:
        enqueue_job(create_alias, [result['resource_id'], { 'user': context['user'], 'auth_user_obj': context['auth_user_obj']}])
    return result
