import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.data_api import actions


class AutomaticAliasesPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IConfigurable)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'data_api')

    # IConfigurable

    def configure(self, config):
        # Certain config options must exists for the plugin to work. Raise an
        # exception if they're missing.
        missing_config = "{0} is not configured. Please amend your .ini file."
        config_options = (
            'ckanext.data_api.hasura_url',
            'ckanext.data_api.hasura_admin_key',
            'ckanext.data_api.hasura_db',
        )
        for option in config_options:
            if not config.get(option, None):
                raise RuntimeError(missing_config.format(option))

    def get_actions(self):
        return {
            'datastore_create': actions.datastore_create
        }
