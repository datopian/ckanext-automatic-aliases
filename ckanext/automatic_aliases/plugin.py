import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.automatic_aliases import actions


class AutomaticAliasesPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'automatic_aliases')

    def get_actions(self):
        return {
            'datastore_create': actions.datastore_create
        }
