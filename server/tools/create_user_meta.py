from google.generativeai.types import FunctionDeclaration, Tool

create_user_meta_tool = Tool(
    function_declarations=[
        FunctionDeclaration(
            name="create_user_meta",
            description="""
                Save a datapoint about the candidate that can be useful to describe their professional or personal profile to potenitial employers.

                args:
                - tags: A list of tags that describe the datapoint (3-5).
                - data: The datapoint that should be saved.
            """,
            parameters={
                "type_": "OBJECT",
                "properties": {
                    "tags": {
                        "type_": "STRING",
                    },
                    "data": {
                        "type_": "STRING",
                    },
                },
                "required": ["data", "tags"],
            },
        )
    ]
)
