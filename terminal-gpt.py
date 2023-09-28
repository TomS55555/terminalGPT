import openai
import json
import argparse

# Define the allowed program names
allowed_programs = ['bash', 'mongosh', 'python']

# Create the argument parser
parser = argparse.ArgumentParser(description="Specify a program name with the -m flag")

# Add the -m flag with choices restricted to allowed_programs
parser.add_argument('-m', dest='program_name', choices=allowed_programs, required=True,
                    help="Specify the program name (bash, mongosh, or python)")

# Add input_prompt as a positional argument without a flag
parser.add_argument('input_prompt', type=str, help="Enter an input prompt")

# Parse the command line arguments
args = parser.parse_args()

# Get the selected program name and input prompt from the parsed arguments
program_name = args.program_name
input_prompt = args.input_prompt

# Perform actions based on the selected program name
if program_name == 'bash':
    desciption="Get a list of possible bash commands on an Ubuntu machine"
elif program_name == 'mongosh':
    desciption = "Get a list of possible mongo shell commands"
elif program_name == 'python':
    desciption="Get a list of possible python commands"

# Use the input_prompt provided by the user
print("Input Prompt:", input_prompt)

openai.api_key = open('../openai_key.txt', 'r').read().strip('\n')


completion = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=[{"role": "user", "content": input_prompt}],
        functions=[
        {
            "name": "get_commands",
            "description": desciption,
            "parameters": {
                "type": "object",
                "properties": {
                    "commands": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": f"A {program_name} terminal command string"
                        },
                        "description": f"List of possible {program_name} terminal command strings to be executed"
                    }
                },
                "required": ["commands"]
            }
        }
        ],
        function_call={"name": "get_commands"},
)
reply_content = completion.choices[0].message
funcs = reply_content.to_dict()['function_call']['arguments']
funcs = json.loads(funcs)
commands = funcs['commands']
print("-------------------------------")
print("Possible commands:")
print("-------------------------------")
for cmd in commands:
    print('- ' + cmd)
print('-------------------------------')