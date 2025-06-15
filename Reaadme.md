//this is a documentation on how to set up the python enviroment, for the front end, you can just run live server

//your folder stricture:

# Ensure this structure:
project-root/
├── app.py                    # Main Flask application
├── asl_alphabet_cnn.h5      # Your trained model
├── requirements.txt         # Dependencies
├── templates/
│   └── index.html          # Frontend template
└── uploads/                # Auto-created for file storage


# Check Python version
open your terminal and type:

python --version 

 # Should show Python 3.10.0

 if not, uninstall it and download python 3.10.0 exactly, nothing higher or lower

 when youve done that, restart vs code and open the terminal and run  python --version 

 # Should show Python 3.10.0




# Create virtual environment
in your terminal, run this command to create your virtual enviroment:
python -m venv venv

# Activate virtual environment
run this command to activate your virtual enviroment:

asl_env\Scripts\activate

# You should see (venv) in your command prompt

if your comand propmpt does not show (venv), run this command:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

then run this command again:

asl_env\Scripts\activate


# Make sure your virtual environment is activated
# Install all required packages by running this command:

pip install -r requirements.txt

# If you encounter issues, try upgrading pip first:

pip install --upgrade pip


# Check if all packages are installed correctly by running this command:

pip list

# You should see:
# - flask>=2.0.0
# - flask-cors>=3.0.0
# - tensorflow==2.12.0
# - numpy>=1.21.0
# - opencv-python>=4.5.0


# Run the Flask app by running this command:

python app.py