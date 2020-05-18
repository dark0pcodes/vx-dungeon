import os
import re

import yaml

from app.common.paths import CONFIG_PATH, STORAGE_PATH


def load_config(tag: str = '!ENV'):
    """
    Load config.yaml in memory
    :param tag: the tag to look for
    :return:
    """
    # pattern for global vars: look for ${word}
    pattern = re.compile(r'.*?\${(\w+)}.*?')
    loader = yaml.SafeLoader

    # the tag will be used to mark where to start searching for the pattern
    # e.g. somekey: !ENV somestring${MYENVVAR}blah blah blah
    loader.add_implicit_resolver(tag, pattern, None)

    def constructor_env_variables(loader, node):
        """
        Extracts the environment variable from the node's value
        :param yaml.Loader loader: the yaml loader
        :param node: the current node in the yaml
        :return: the parsed string that contains the value of the environment
        variable
        """
        value = loader.construct_scalar(node)
        match = pattern.findall(value)  # to find all env variables in line
        if match:
            full_value = value
            for g in match:
                full_value = full_value.replace(
                    f'${{{g}}}', os.environ.get(g, g)
                )
            return full_value
        return value

    loader.add_constructor(tag, constructor_env_variables)

    with open(os.path.join(CONFIG_PATH, 'app.yml'), 'r') as f:
        config = yaml.load(f, Loader=loader)
    return config


def create_storage():
    """
    Create storage folder
    Returns:
    """
    if not os.path.exists(STORAGE_PATH):
        os.mkdir(STORAGE_PATH)
