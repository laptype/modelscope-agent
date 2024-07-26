import streamlit as st
import os
import time
import json

from apps.codexgraph_agent.components.setting import setting
from apps.codexgraph_agent.components.sidebar import sidebar
from apps.codexgraph_agent.components.states import initialize_page_state, get_json_files

def agent_test_run(user_query, file_path, call_back):
    for i in range(10):
        message = f"Processing {i + 1}/{10}..."
        call_back(message, "assistant", "🤖")

        time.sleep(1)  # Simulate work by sleeping for 1 second

class PageBase:
    def __init__(self,
                 task_name='code_commenter',
                 page_title="📝 Code Commenter",
                 output_path='CC_conversation',
                 input_title="Code needing comments",
                 default_input_text="Please input the code that requires comments"):

        self.page_name = task_name
        self.page_title = page_title
        self.output_path = output_path
        self.input_title = input_title
        self.default_input_text = default_input_text

        initialize_page_state(self.page_name)
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        self.prompt_path = os.path.join(st.session_state.shared['setting']['prompt_path'], task_name)
        self.schema_path = os.path.join(st.session_state.shared['setting']['prompt_path'], 'graph_database')

        st.session_state[self.page_name]['setting']['history_list'] = get_json_files(self.output_path)
        st.set_page_config(layout="wide")

    def main(self):
        st.title(self.page_title)

        st.session_state[self.page_name]['conversation_history'] = []

        sidebar()

        setting(self.page_name, self.output_path)

        self.repo_db_test()

        openai_api_key = st.session_state.get("OPENAI_API_KEY")

        if not openai_api_key:
            st.warning(
                "Enter your OpenAI API key in the sidebar. You can get a key at"
                " https://platform.openai.com/account/api-keys."
            )

        self.body()

    def body(self):

        col1, col2 = st.columns([1, 2])

        with col2:
            # st.header("Conversation")
            st.session_state[self.page_name]['conversation_container'] = st.container()

        if st.session_state[self.page_name]['reload_button']:
            st.session_state[self.page_name]['conversation_history'] = []
            # st.success(f"File path set to: {st.session_state.history_path}")
            self.reload_history_message(st.session_state[self.page_name]['setting']['history_path'])

        with col1:
            st.header(self.input_title)
            st.session_state[self.page_name]['input_file_path'] = st.text_input("File Path (optional)",
                                                                           placeholder="Enter file path here")
            st.session_state[self.page_name]['input_text'] = st.text_area("Type your question here:", height=300,
                                                                     placeholder=self.default_input_text,
                                                                     label_visibility="collapsed",
                                                                     value=st.session_state[self.page_name]['input_text'])
            col1_1, col1_2, col1_3 = st.columns([1, 1, 1])
            with col1_1:
                if st.button("Send"):
                    if st.session_state[self.page_name]['input_text']:
                        self.agent()

            with col1_2:
                if st.session_state[self.page_name]['conversation_history']:
                    if st.button("Clear Conversation"):
                        self.clear_conversation()

            if st.session_state[self.page_name]['final_result']:
                st.header("Final Result")
                st.write(st.session_state[self.page_name]['final_result'])

    def agent(self):
        st.session_state[self.page_name]['final_result'] = ''

        answer = agent_test_run(user_query=st.session_state[self.page_name]['input_text'],
                                file_path=st.session_state[self.page_name]['input_file_path'],
                                call_back=self.update_message)

        st.session_state[self.page_name]['final_result'] = 'aaa'

    def update_message(self, message, role, avatar=None):
        st.session_state[self.page_name]['conversation_history'].append({'message': message, 'role': role, 'avatar': avatar})
        with st.session_state[self.page_name]['conversation_container']:
            with st.chat_message(role, avatar=avatar):
                st.markdown(message)

    def reload_history_message(self, history_path):
        with open(history_path, 'r') as file:
            history = json.load(file)
        for data in history:
            self.update_message(data['message'], data['role'], data['avatar'])

        st.session_state[self.page_name]['final_result'] = history[-1]['message']

    def clear_conversation(self):
        """Clear conversation list"""
        st.session_state[self.page_name]['conversation_history'] = []


    def repo_db_test(self):
        # TODO: test build code base
        if st.session_state[self.page_name]['build_button']:
            st.session_state[self.page_name]['build_place'].success(
                f"File path set to: {st.session_state.shared['setting']['repo_path']}")
        # TODO: test neo4j
        if st.session_state[self.page_name]['test_connect_button']:
            st.session_state[self.page_name]['test_connect_place'].success(
                f"Success connect to Neo4j: {st.session_state.shared['setting']['neo4j']['url']}")


if __name__ == '__main__':
    page = PageBase()
    page.main()