import streamlit as st
import os
import time
import json

from apps.codexgraph_agent.components.page import PageBase, agent_test_run


class CodeUnittesterPage(PageBase):
    def __init__(self):
        super().__init__(task_name='code_unittester',
                         page_title="🔍 Code Unit Tester",
                         output_path='CU_conversation',
                         input_title="Code needing unittest",
                         default_input_text="Please input the code for which you need unit tests. Include any specific scenarios or edge cases you want to test.")


    def agent(self):
        st.session_state[self.page_name]['final_result'] = ''

        answer = agent_test_run(user_query=st.session_state[self.page_name]['input_text'],
                                file_path=st.session_state[self.page_name]['input_file_path'],
                                call_back=self.update_message)

        st.session_state[self.page_name]['final_result'] = 'aaa'


if __name__ == '__main__':
    page = CodeUnittesterPage()
    page.main()
