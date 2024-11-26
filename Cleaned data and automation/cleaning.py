import json
import re

def dialogue_to_json(dialogue_lines):
    system_message = {
        "role": "system",
        "content": "Your name is star. You are to engage naturally, build rapport and contribute to the conversation by actively listening, share insights and ask open ended questions."
    }
    # Remove brackets from dialogue_lines using regular expression
    dialogue_lines = re.sub(r'\[|\]', '', dialogue_lines).strip()

    messages = [system_message]
    
    roles = ["user", "assistant"]
    for i, line in enumerate(dialogue_lines.strip().split("\n")):
        clean_line = line.strip()
        role_index = i % 2 
        messages.append({"role": roles[role_index], "content": clean_line})

    final_object = {"messages": messages}
    return json.dumps(final_object, ensure_ascii=False)

# Read input from file
with open("cleaned.txt", "r", encoding="utf-8") as file:
    input_text = file.read()

# Split input_text into dialogues enclosed in brackets []
dialogues = re.findall(r'\[(.*?)\]', input_text, re.DOTALL)

# Convert each dialogue to JSON and write to output file
with open("new.jsonl", "a", encoding="utf-8") as output_file:
    for dialogue in dialogues:
        json_output = dialogue_to_json(dialogue)
        output_file.write(json_output + "\n")