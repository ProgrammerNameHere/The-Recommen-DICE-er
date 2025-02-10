
# The-Recommend-DICE-er

This repo is the source code of our boardgame recommendation engine. We built this as our capstone project for the neuefische bootcamp "Data Science, ML & AI"

## 

## Set up your Environment

To follow along with the scripts and notebooks you can set up a virtual environment. For this purpose you can use the following commands:

The added [requirements file](requirements.txt) contains all libraries and dependencies we need to execute the notebooks.

*Note: If there are errors during environment setup, try removing the versions from the failing packages in the requirements file.*

### **`macOS`** type the following commands : 

- We have also added a [Makefile](Makefile) which has the recipe called 'setup' which will run all the commands for setting up the environment.


```BASH
    make setup
    ```
    After that active your environment by following commands:
    ```BASH
    source .venv/bin/activate
```
Or ....
- Install the virtual environment and the required packages by following commands:

```BASH
    pyenv local 3.11.3
    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
```
    
### **`WindowsOS`** type the following commands :

- Install the virtual environment and the required packages by following commands.

   For `PowerShell` CLI :

    ```PowerShell
    pyenv local 3.11.3
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    For `Git-bash` CLI :
  
    ```BASH
    pyenv local 3.11.3
    python -m venv .venv
    source .venv/Scripts/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    **`Note:`**
    If you encounter an error when trying to run `pip install --upgrade pip`, try using the following command:
    ```Bash
    python.exe -m pip install --upgrade pip
    ```
  
