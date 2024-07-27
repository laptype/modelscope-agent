
from modelscope_agent.environment.graph_database import GraphDatabaseHandler
from modelscope_agent.agents.codexgraph_agent import (
    CodexGraphAgentGeneral, CodexGraphAgentGenerator
)




if __name__ == '__main__':
    import os
    os.environ["OPENAI_API_KEY"] = "sk-68df19894a0545758668b74ab93fcd6d"
    os.environ['DASHSCOPE_API_KEY'] = "sk-0eaea86b17bb49a9b14757e00194a24e"
    llm_config = {
        'model': 'deepseek-coder',
        'api_base': 'https://api.deepseek.com',
        'model_server': 'openai'
    }
    #
    # graph_db = GraphDatabaseHandler(
    #     uri="bolt://localhost:7687",
    #     user="neo4j",
    #     password="12345678",
    #     database_name="neo4j",
    #     task_id="",
    #     use_lock=True,
    # )
    #
    # prompt_path = os.path.join('prompt','code_generator')
    # schema_path = os.path.join('prompt', 'graph_database')
    # agent = CodexGraphAgentGenerator(llm=llm_config,
    #                                prompt_path=prompt_path,
    #                                schema_path=schema_path,
    #                                task_id='code_unittest',
    #                                graph_db=graph_db,
    #                                max_iterations=5)
    # agent.run('test')
    from modelscope_agent.llm import get_chat_model

    msg = [ {"role": "user", "content": 'hello'} ]
    llm = get_chat_model(**llm_config)
    resp = llm.chat(messages=msg,
                    max_tokens=1024,
                    temperature=1.0,
                    stream=False)
    usage_info = llm.get_usage()

    print(usage_info)