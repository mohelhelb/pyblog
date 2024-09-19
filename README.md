# PyBlog

## Description
This web application is a blogging platform that enables Python developers to share insights and knowledge. Some of the features of this application are the following:

- Mobile-first design.

- Create/Delete user accounts.
 
- Reset forgotten passwords.
 
- Follow/Unfollow users.

- Create, read, update, and delete posts.

- Bookmark favorite posts.

## Setup

### Docker  

- Clone the GitHub repository into your chosen directory (e.g. *~/projects/*):
  ~~~	
  mkdir -p ~/projects/ && cd ~/projects/
  ~~~
  ~~~
  git clone git@github.com:mohelhelb/pyblog.git
  ~~~

- Change working directory:
  ~~~
  cd ~/projects/pyblog/
  ~~~	
  
- Create a file with the name *.env_development* and write the following environment variables into it[^1]:
  [^1]: [Sign in with Google app passwords](https://support.google.com/accounts/answer/185833?hl=en) 
  ~~~
  touch .env_development
  ~~~
  ~~~
  FLASK_APP=run_app
  FLASK_DEBUG=True  
  FLASK_ENV=development
  PYBLOG_SECRET_KEY="Replace this with a long, unguessable string"
  PYBLOG_MAIL_USERNAME="Replace this with your gmail"
  PYBLOG_MAIL_PASSWORD="Replace this with your Google app password with no spaces" 
  ~~~ 

- Build the docker image:
  ~~~
  docker build -t pyblog .
  ~~~

- Start a docker container:
  ~~~
  docker container run -d -p 5000:5000 --env-file .env_development --rm pyblog
  ~~~  

- Enter the server address and port number (http://127.0.0.1:5000/) in the browser's search bar. 


### Linux 

- Clone the GitHub repository into your chosen directory (e.g. *~/projects/*):
  ~~~	
  mkdir -p ~/projects/ && cd ~/projects/
  ~~~
  ~~~
  git clone git@github.com:mohelhelb/pyblog.git
  ~~~

- Change working directory:
  ~~~
  cd ~/projects/pyblog/
  ~~~	 

- Create a file with the name *.env_development* and write the following environment variables into it[^1]: 
  ~~~
  touch .env_development
  ~~~
  ~~~
  FLASK_APP=run_app
  FLASK_DEBUG=True  
  FLASK_ENV=development
  PYBLOG_SECRET_KEY="Replace this with a long, unguessable string"
  PYBLOG_MAIL_USERNAME="Replace this with your gmail"
  PYBLOG_MAIL_PASSWORD="Replace this with your Google app password with no spaces" 
  ~~~  

- Create a virtual environment to isolate the application:
	~~~	
  pip install -U virtualenv
  ~~~
  ~~~
  virtualenv venv/
  ~~~

- Adjust the *deactivate* function defined in the *venv/bin/activate* file:
  ~~~
  deactivate() {
    ...
    unset FLASK_APP
    unset FLASK_DEBUG
    unset FLASK_ENV
    unset PYBLOG_SECRET_KEY
    unset PYBLOG_MAIL_USERNAME
    unset PYBLOG_MAIL_PASSWORD
  }
  ~~~

- Redefine the *PROJECT_ROOT_DIR* variable in the *activate_venv_development* file accordingly.

- Activate the virtual environment:
  ~~~
  source activate_venv_development
  ~~~

- Install the application's dependencies:
  ~~~	
  pip install -r requirements.txt
  ~~~

- Create a SQLite database:
  ~~~
  flask db upgrade
  ~~~

- Run the application:
  ~~~
  flask run
  ~~~

- Enter the server address and port number (http://127.0.0.1:5000/) in the browser's search bar.
