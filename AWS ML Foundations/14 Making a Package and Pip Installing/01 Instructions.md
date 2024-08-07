Following the instructions from the previous video, convert the modularized code into a Python package. 

You can put your code into the 3a_python_package folder in the workspace. Inside the 3a_python_package folder, you'll need to create a few folders and files:
* a setup.py file, which is required in order to use pip install
* a folder called 'distributions', which is the name of the Python package
* inside the 'distributions' folder, you'll need the Gaussiandistribution.py file, Generaldistribution.py and an __init__.py file.

Once everything is set up, open a new terminal window in the workspace by clicking 'NEW TERMINAL'. Then type:
cd 3a_python_package
pip install .

If everything is set up correctly, pip will install the distributions package into the workspace. You can then start the python interpreter from the terminal typing:
python

Then within the Python interpreter, you can use the distributions package:
from distributions import Gaussian
gaussian_one = Gaussian(25, 2)
gaussian_one.mean
gaussian_one + gaussian_one

etcetera...In other words, you can import and use the Gaussian class because the distributions package is now officially installed as part of your Python installation.

If you get stuck, there's a solution in the 3b_answer_python_package folder.

If you want to install the Python package locally to your computer, you might want to set up a virtual environment first. A virtual environment is a siloed Python installation apart from your main Python installation. That way you can easily delete the virtual enviornment without affecting your Python installation.

If you want to try using virtual environments in this workspace first, here is how to do it:
- There is an issue with the Ubuntu operating system and Python3 where the venv package isn't installed correctly. In the workspace, one way to fix this is by running this command in the workspace terminal: `conda update python` See: https://stackoverflow.com/questions/26215790/venv-doesnt-create-activate-script-python3 Then type `y` when prompted. It might take a couple of minutes for the workspace to update. If you are not using anaconda on your local computer, you can skip this first step.
- now, type this command to create a virtual environment `python -m venv venv_name` where venv_name is the name you want to give to your virtual environment. You'll see a new folder appear with the Python installation named venv_name
- In the terminal, type `source venv_name/bin/activate`. You'll notice that the command line now shows (venv_name) at the beginning of the line to indicate you are using the venv_name virtual environment
- Now, you can type `pip install python_package/.` That should install your distributions Python package.
- Try using the package in a program to see if everything works!








