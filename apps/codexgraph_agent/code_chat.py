import sys
project_path = r'D:\study\postgraduate\study_project\alibaba_LLM\codexgraph\modelscope-agent'
if project_path not in sys.path:
    sys.path.append(project_path)

import streamlit as st
import os
import time
import json
from datetime import datetime
from apps.codexgraph_agent.components.page import PageBase, agent_test_run


class CodeChatPage(PageBase):
    def __init__(self):
        super().__init__(task_name='code_chat',
                         page_title="💬 Code Chat",
                         output_path='CCH_conversation',
                         input_title="",
                         default_input_text="")

    def body(self):
        col2, col3 = st.columns([2, 2])

        with col2:
            # st.header("Chat")
            st.session_state[self.page_name]['conversation_container_chat'] = st.container()

        with col3:
            st.session_state[self.page_name]['conversation_container'] = st.container()

        if st.session_state[self.page_name]['reload_button']:
            # st.success(f"File path set to: {st.session_state.history_path}")
            self.reload_history_message(st.session_state[self.page_name]['setting']['history_path'])

        if user_input := st.chat_input(placeholder="input any question..."):
            if user_input:
                st.session_state[self.page_name]['conversation_history'] = []
                # graph_db = get_graph_db(repo_path=None, task_id=config['task_id'], is_build=False,
                #                         env_path_dict=None)

                st.session_state[self.page_name]['conversation_history'].append(
                    {'message': user_input, 'role': "user", 'avatar': "🧑‍💻"})
                st.session_state[self.page_name]['chat'].append({'message': user_input, 'role': "user", 'avatar': "🧑‍💻"})
                self.update_chat()

                answer = agent_test_run(user_input, '', self.update_message)

                timestamp = datetime.now().strftime("%d%H%M")
                st.session_state[self.page_name]['conversation_history'].append(
                    {'message': answer, 'role': "assistant", 'avatar': "🤖"})
                st.session_state[self.page_name]['chat'].append({'message': answer, 'role': "assistant", 'avatar': "🤖"})

                self.display_chat(answer, 'assistant', "🤖")

                with open(os.path.join(self.output_path, f'CCH_conversation_history_{timestamp}.json'), 'w') as file:
                    json.dump(st.session_state[self.page_name]['conversation_history'], file)

        with st.session_state[self.page_name]['conversation_container_chat']:
            if len(st.session_state[self.page_name]['chat']) == 0:
                with st.chat_message('assistant', avatar="🤖"):
                    st.markdown('How can i help you?')

    def update_chat(self):
        with st.session_state[self.page_name]['conversation_container_chat']:
            for msg in st.session_state[self.page_name]['chat']:
                with st.chat_message(msg['role'], avatar=msg['avatar']):
                    st.markdown(msg['message'])

    def display_chat(self, message, role, avatar=None):
        with st.session_state[self.page_name]['conversation_container_chat']:
            with st.chat_message(role, avatar=avatar):
                st.markdown(message)

    def reload_history_message(self, history_path):
        with open(history_path, 'r') as file:
            history = json.load(file)
        if 'chat' in history_path:
            st.session_state[self.page_name]['chat'] = history
        else:
            st.session_state[self.page_name]['conversation_history'] = history

        self.update_chat()
        for data in st.session_state[self.page_name]['conversation_history']:
            self.show_message(data['message'], data['role'], data['avatar'])

    def show_message(self, message, role, avatar=None):
        with st.session_state[self.page_name]['conversation_container']:
            with st.chat_message(role, avatar=avatar):
                st.markdown(message)


if __name__ == '__main__':
    page = CodeChatPage()
    page.main()
