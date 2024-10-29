from google.generativeai.types import FunctionDeclaration, Tool

query_candidate_profile_tool = Tool(
    function_declarations=[
        FunctionDeclaration(
            name="query_candidate_profile",
            description="""
            Use this tool to learn about the candidate's career, job search, personal interests, and professional goals.

            args:
                prompt: str
                    The question to ask the bot representing the candidate you are chatting with.
            """,
            parameters={
                "type_": "OBJECT",
                "properties": {
                    "prompt": {
                        "type_": "STRING",
                    },
                },
                "required": ["prompt"],
            },
        )
    ]
)
