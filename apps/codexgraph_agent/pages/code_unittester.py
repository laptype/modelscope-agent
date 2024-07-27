import streamlit as st
import os
import time
import json

from apps.codexgraph_agent.components.page import PageBase, agent_test_run
from modelscope_agent.agents.codexgraph_agent import CodexGraphAgentUnitTester


class CodeUnittesterPage(PageBase):
    def __init__(self):
        super().__init__(task_name='code_unittester',
                         page_title="🔍 Code Unit Tester",
                         output_path='log\CU_conversation',
                         input_title="Code needing unittest",
                         default_input_text="Please input the code for which you need unit tests. Include any specific scenarios or edge cases you want to test.")
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

        prompt_path = os.path.join(st.session_state.shared['setting']['prompt_path'], 'code_unittester')
        schema_path = os.path.join(st.session_state.shared['setting']['prompt_path'], 'graph_database')

        try:
            agent = CodexGraphAgentUnitTester(llm=llm_config,
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
    page = CodeUnittesterPage()
    page.main()

if __name__ == '__main__':
    page = CodeUnittesterPage()
    page.main()
