PLAN_PROMPT = """As a tool planner, you can make sensible plans to meet the needs of current users by responding to the questions they ask. You can use tools that already exist to meet the needs of users.
Step 1: You need to understand exactly what tools are available and what exactly the tools do .
Step 2: Analyze the user's intent and understand the user's needs.
step 3: the combination of tools and user needs to design a plan, each step needs to give the name of the specific tool to be used and a specific plan, if the current step does not need to use the tool then the tool name is empty.
Step 4: Return to the list of plans.
"""
PLAN_EXAMPLE_PROMPT ="""
Here is some examples about plans:

Input:
tools_summary: {
  "ToolA": "For text analysis and data extraction"
}
input_text: "I need to analyze a piece of text to extract key information."

Output:
[{'tool':'ToolA','plan':'use ToolA as a tool to get the corresponding information and then combine the information to answer the question'}]

Input:
tools_summary: {
}
input_text: "I need to print 1+1."

Output:
[{'tool':'','plan':'Reply to the string "1+1".'}]

"""
PLAN_HINT = """
Your answer should be returned in a strict format, with the plan put into the list in steps, and each step security tool and plan put into the dictionary.
Ensure the output can be parsed by Python ast.literal_eval.
Don't output in markdown format, something like ```json or ```,just output in the corresponding string format
"""