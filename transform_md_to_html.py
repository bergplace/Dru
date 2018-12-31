import markdown2
from os import listdir

html_path = './web/src/main/templates/main/'
files = [f for f in listdir(html_path) if f.endswith('.md')]
for file in files:
    html_md = ''
    with open(file, 'r') as f:
        html_md = markdown2.markdown(f.read())
    html_md = """
        {% extends "main/base.html" %}
        {% block content %}
    """ + html_md + "{% endblock %}"
    with open('.'.join(file.split('.')[:-1]) + '.html', 'w') as f:
        f.write(html_md)
