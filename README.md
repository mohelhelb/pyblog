## Web Application

### Description
This web application is a simple blogging platform that enables Python developers to share insights and knowledge. Some of the features of this application are the following:

- Mobile-first design.
- Create/Delete user accounts. 
- Reset forgotten passwords. 
- Follow/Unfollow users.
- Create, read, update, and delete posts.
- Bookmark favorite posts.

### Setup
The steps that should be taken to set up this application are as follows:

- Clone the GitHub repository into your chosen directory (e.g. *~/projects/*):
  ~~~	
  mkdir -p ~/projects/
  git clone git@github.com:mohelhelb/pyblog.git ~/projects/pyblog/
  ~~~	
- Create a virtual environment to isolate the application:
	~~~	
  pip install -U virtualenv
  virtualenv ~/projects/pyblog/venv/
  ~~~
- Create a file with the name *.env_development* and write the following environment variables into it:
  ~~~
  touch ~/projects/pyblog/.env_development
  ~~~
  ~~~
  FLASK_APP=run_app
  FLASK_DEBUG=True  
  FLASK_ENV=development
  PYBLOG_SECRET_KEY="Replace this with a long, unguessable string"
  PYBLOG_MAIL_USERNAME="Replace this with your gmail"
  PYBLOG_MAIL_PASSWORD="Replace this with your Google app password with no spaces"[^1]
  [^1]: [Google: Sign in with app passwords](https://support.google.com/accounts/answer/185833?hl=en)  
  ~~~
- Activate the virtual environment:
  ~~~
  source ~/projects/pyblog/.activate_venv_development
  ~~~
- Install the application's dependencies:
  ~~~	
  pip install -r ~/projects/pyblog/requirements.txt
  ~~~
- Create a SQLite database:
  ~~~
  flask shell
  ~~~
  ~~~
  >>> db.create_all()
  >>> exit()
  ~~~
- Run the application:
  ~~~
  flask run
  ~~~
- Enter the generated server address and port number (http://127.0.0.1:5000/) in the browser's search bar.
