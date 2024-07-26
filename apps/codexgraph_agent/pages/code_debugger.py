import streamlit as st
import os
import time
import json

from apps.codexgraph_agent.components.page import PageBase, agent_test_run


class CodeDebuggerPage(PageBase):
    def __init__(self):
        super().__init__(task_name='code_debugger',
                         page_title="🛠️ Code Debugger",
                         output_path='CD_conversation',
                         input_title="Bug Issue",
                         default_input_text="Please input the code snippet and describe the bug or issue you are facing. Include any error messages if available.")


    def agent(self):
        st.session_state[self.page_name]['final_result'] = ''

        answer = agent_test_run(user_query=st.session_state[self.page_name]['input_text'],
                                file_path=st.session_state[self.page_name]['input_file_path'],
                                call_back=self.update_message)

        st.session_state[self.page_name]['final_result'] = 'aaa'


if __name__ == '__main__':
    page = CodeDebuggerPage()
    page.main()
