from copy import copy

from fame.common.objects import Dictionary
from fame.common.exceptions import MissingConfiguration
from fame.common.mongo_dict import MongoDict


def config_to_dict(config):
    return {setting['name']: setting for setting in config}


# We will keep configured values, only if they have the same name and type
def apply_config_update(config, config_update):
    new_config = []
    config = config_to_dict(config)

    for setting in config_update:
        new_setting = copy(setting)

        if (
            setting['name'] in config
            and setting['type'] == config[setting['name']]['type']
        ):
            new_setting['value'] = config[setting['name']]['value']
            if 'option' in config[setting['name']]:
                new_setting['option'] = config[setting['name']]['option']

        new_config.append(new_setting)

    return new_config


def incomplete_config(config):
    return any(
        setting['value'] is None and 'default' not in setting
        for setting in config
    )


# This is for FAME's internal configuration
class Config(MongoDict):
    collection_name = 'settings'

    def get_values(self):
        values = Dictionary()
        for setting in self['config']:
            if (setting['value'] is None) and ('default' not in setting):
                raise MissingConfiguration(
                    f"Missing configuration value: {setting['name']} (in '{self['name']}')",
                    self,
                )


            values[setting['name']] = setting['value']
            if setting['value'] is None:
                values[setting['name']] = setting['default']

        return values

    def update_config(self, config):
        self['description'] = config['description']
        self['config'] = apply_config_update(self['config'], config['config'])
        self.save()
