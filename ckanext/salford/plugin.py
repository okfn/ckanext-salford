import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def information_classes():
    """Return the set of available "information classes" for datasets.

    On the Salford site each dataset can belong to an information class
    (custom dataset field).

    This function is used to fill in the options for the Information Class
    dropdown in the dataset form, and in other places where a list of all the
    information classes is needed.

    """
    return ["Who we are and what we do", "What we spend and how we spend it",
            "What our priorities are and how we are doing",
            "How we make decisions", "Our policies and procedures",
            "Lists and registers", "Services provided by the council"]


def datasets_for_information_class(information_class):
    """Return a list of all the datasets with the given information class."""
    q = 'information_class:"{iclass}"'.format(iclass=information_class)
    datasets = toolkit.get_action("package_search")(
        context={}, data_dict={"q": q})["results"]
    return datasets


class SalfordPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.ITemplateHelpers)


    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'salford')


    # IDatasetForm

    def _modify_package_schema(self, schema):
        schema.update({
            'information_class': [toolkit.get_validator('ignore_missing'),
                                  toolkit.get_converter('convert_to_extras')]
        })
        return schema

    def create_package_schema(self):
        schema = super(SalfordPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(SalfordPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(SalfordPlugin, self).show_package_schema()
        schema.update({
            'information_class': [toolkit.get_converter('convert_from_extras'),
                                  toolkit.get_validator('ignore_missing')]
        })
        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        return []


    # IRoutes

    def before_map(self, map_):
        map_.connect(
            "publication_scheme", "/publication_scheme",
            controller="ckanext.salford.plugin:SalfordController",
            action="publication_scheme")
        return map_

    def after_map(self, map_):
        return map_


    # ITemplateHelpers

    def get_helpers(self):
        return {
            "information_classes": information_classes,
            "datasets_for_information_class": datasets_for_information_class,
            }


class SalfordController(toolkit.BaseController):

    def publication_scheme(self):
        return toolkit.render('publication_scheme.html')
