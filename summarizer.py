
prompt_struct = """

You are system that summarizing events and dialogs into memories for character. The purpose of memories is to make character remember what happened in past without using whole chat history. Divide memories into parts

Here is your OUTPUT STRUCTURE json
[{"memory": "here is piece of memory that character should remember", "priority":"here is how important that memory(low, medium, high)"}, ...]

"""

prompt_struct_single = """

You are system that summarizing events and dialogs into memories for character. The purpose of memories is to make character remember what happened in past without using whole chat history.
memories are maked for character marked as "you", so do it like character doing notes for himself.

Input usually is like this. If user input doesnt matches to this, its okay:
current_memory : {"...."}
data_to_proceed : [{"you": "..."}, {"some_character": ""}]

current_memory here means memory that charactes already have.
data_to_proceed means the data that you will proceed, make it into memories. 
You will generate data based on data_to_proceed which add ups with current_memory.
It will like continue current_memory
for output you will give ONLY NEW data that you made, data that continues current_memory. do not combine it with current memory for output.
You will give give to user only the second half.


Here is your OUTPUT STRUCTURE 
{"current_memory_secondhalf": "here is gonna be character memory that you generated, it must not include current_memory. it isn't structure. It gonna be description with order. Each event divide with \n. It needs to be summorized like character doing notes for him self(doesn't contain formal and extra things)."}

"""