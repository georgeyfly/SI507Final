# SI507Final
This is SI507 final project. This program can extract data from Linkedin and select suitable job according to users' choice.

Instruction for Demo:
1. Download the files including tree.py, saveload.py, flaskdemo.py, cache.json, input.html, response.html. Create templates file and put input.html and response.html to templates.

2. Install requests package in Python.

3. Run flaskdemo.py

4. Open http://127.0.0.1:5000 in the web browser.

5. Go to http://127.0.0.1:5000/demo to answer questions according to your choice. Select the presentation mode(give brief jobs or not) and submit the form. Then you can see job information or “No suitable job!”.

Data Structure Readme:

1. Tree of 5 level

2. 1-4 level has nodes(internal nodes) whose val is questions

3. 5 level has nodes(leaf nodes) whose val is a list of Jobs.
