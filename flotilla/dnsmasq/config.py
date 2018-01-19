from jinja2 import BaseLoader, Environment


CONFIG_TMPL = '''
{% if tftp_enabled %}
enable-tftp
{% endif %}
'''


class Config(object):

    def __init__(self, tftp_enabled=True):
        self.tftp_enabled = tftp_enabled

    def to_file(self, filename):
        template = Environment(loader=BaseLoader()).from_string(CONFIG_TMPL)
        output = template.render(self.__dict__)

        with open(filename, 'wb') as fh:
            fh.write(output)
