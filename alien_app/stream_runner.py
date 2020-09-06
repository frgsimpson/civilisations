""" Script for launching streamlit within PyCharm """

from streamlit import bootstrap

real_script = './stream.py'

bootstrap.run(real_script, f'run.py {real_script}', [])
