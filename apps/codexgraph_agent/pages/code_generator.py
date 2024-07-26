import streamlit as st
import os
import time
import json

from apps.codexgraph_agent.components.page import PageBase, agent_test_run


class CodeGeneratorPage(PageBase):
    def __init__(self):
        super().__init__(task_name='code_generator',
                         page_title="🔧 Code Generator",
                         output_path='CG_conversation',
                         input_title="New Requirements",
                         default_input_text="Please input the requirements or specifications for the new feature or module you need.")


    def agent(self):
        st.session_state[self.page_name]['final_result'] = ''

        answer = agent_test_run(user_query=st.session_state[self.page_name]['input_text'],
                                file_path=st.session_state[self.page_name]['input_file_path'],
                                call_back=self.update_message)

        st.session_state[self.page_name]['final_result'] = 'aaa'


if __name__ == '__main__':
    page = CodeGeneratorPage()
    page.main()
