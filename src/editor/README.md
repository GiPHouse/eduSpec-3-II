To handle all the imports, I added a pyproject.toml to the project folder.

Now, project/src is always in system path and we can do all imports from the perspective of src/

To be able to use it, one must run the following from project folder (not from src):

**pip install -e .**
