import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

if project_root not in sys.path:
    sys.path.append(project_root)

import streamlit as st
from apps.codexgraph_agent.components.states import initialize_page_state
from apps.codexgraph_agent.components.setting import setting_neo4j, setting_repo
from apps.codexgraph_agent.components.page import PageBase

class Help(PageBase):
    def __init__(self):
        self.page_name = 'help'
    def get_agent(self):
        pass

    def main(self):
        initialize_page_state(self.page_name)
        st.set_page_config(layout="wide")
        st.title('Help')
        st.markdown('# 1. Connect to Neo4j\n')
        setting_neo4j(self.page_name)
        st.markdown('# 2. Build a code repo\n')
        setting_repo(self.page_name)

        self.repo_db_test()


if __name__ == '__main__':
    page = Help()
    page.main()