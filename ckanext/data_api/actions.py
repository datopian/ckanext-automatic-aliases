import requests
import ckan.plugins.toolkit as toolkit
import ckan.logic.action as actions
from ckan.plugins.toolkit import chained_action, get_action, enqueue_job
from ckan.common import config

def add_permissions(table_name):
    url = config.get("ckanext.data_api.hasura_url") + "/v1/metadata"
    body = {
        "type": "pg_create_select_permission",
        "args": {
            "source": config.get("ckanext.data_api.hasura_db"),
            "table": table_name,
            "role": "anon",
            "permission": {"columns": "*", "filter": {}, "allow_aggregations": True},
        },
    }
    headers = {
        "X-Hasura-Role": "admin",
        "X-Hasura-Admin-Secret": config.get("ckanext.data_api.hasura_admin_key"),
    }
    response = requests.post(url, json=body, headers=headers)
    return response.status_code


def track_view(table_name):
    url = config.get("ckanext.data_api.hasura_url") + "/v1/metadata"
    body = {
        "type": "pg_track_table",
        "args": {
            "source": config.get("ckanext.data_api.hasura_db"),
            "table": table_name,
        },
    }
    headers = {
        "X-Hasura-Role": "admin",
        "X-Hasura-Admin-Secret": config.get("ckanext.data_api.hasura_admin_key"),
    }
    response = requests.post(url, json=body, headers=headers)
    return response.status_code



def get_resource_name(resource_name):
    splited_resource_name = resource_name.split('.')
    if len(splited_resource_name) > 1:
        return splited_resource_name[0] 
    return resource_name.lower()

def create_alias(resource_id, context):
    resource_info = get_action('resource_show')(None, { 'id': resource_id })
    get_action('datastore_create')(context, { 'resource_id': resource_id, 'aliases': get_resource_name(resource_info['name']), 'force': True})
    track_view(get_resource_name(resource_info['name']))
    add_permissions(get_resource_name(resource_info['name']))

@chained_action
def datastore_create(original_action, context, data_dict):
    result = original_action(context, data_dict)                                                        
    if "aliases" not in data_dict:
        enqueue_job(create_alias, [result['resource_id'], { 'user': context['user'], 'auth_user_obj': context['auth_user_obj']}])
    return result