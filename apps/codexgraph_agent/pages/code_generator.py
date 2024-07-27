import streamlit as st
import os
import time
import json

from apps.codexgraph_agent.components.page import PageBase, agent_test_run
from modelscope_agent.agents.codexgraph_agent import CodexGraphAgentGenerator

class CodeGeneratorPage(PageBase):
    def __init__(self):
        super().__init__(task_name='code_generator',
                         page_title="🔧 Code Generator",
                         output_path='log\CG_conversation',
                         input_title="New Requirements",
                         default_input_text="Please input the requirements or specifications for the new feature or module you need.")

        self.agent = self.get_agent()

    def get_agent(self):
        graph_db = self.get_graph_db(st.session_state.shared['setting']['project_id'])

        if not graph_db:
            return None

        llm_config = {
            'model': 'deepseek-coder',
            'api_base': 'https://api.deepseek.com',
            'model_server': 'openai'
        }

        prompt_path = os.path.join(st.session_state.shared['setting']['prompt_path'], 'code_generator')
        schema_path = os.path.join(st.session_state.shared['setting']['prompt_path'], 'graph_database')

        try:
            agent = CodexGraphAgentGenerator(llm=llm_config,
                                             prompt_path=prompt_path,
                                             schema_path=schema_path,
                                             task_id=st.session_state.shared['setting']['project_id'],
                                             graph_db=graph_db,
                                             max_iterations=5,
                                             message_callback=self.create_update_message())
        except:
            agent = None
        return agent

def show():
    page = CodeGeneratorPage()
    page.main()

if __name__ == '__main__':
    page = CodeGeneratorPage()
    page.main()
