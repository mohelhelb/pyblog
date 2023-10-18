## Web Application

### Description
This project is a simple blog-based web application built with Flask (Python web framework), JavaScript, CSS, and HTML. Some of the features of the application are the following:

- Mobile-first design.
- Create/Delete user accounts. 
- Reset forgotten passwords. 
- Follow/Unfollow users.
- Create, read, update, and delete posts.
- Bookmark favorite posts.

### Setup
The steps that should be taken to set up this application are as follows:

- Clone the GitHub repository into the preferred directory (e.g. *~/projects/*).
  ~~~	
  mkdir -p ~/projects/
  git clone git@github.com:mohelhelb/pyblog.git ~/projects/pyblog/
  ~~~	
- Isolate the application by creating and activating a virtual environment.
	~~~	
  [pip install -U virtualenv]
  virtualenv ~/projects/pyblog/venv/
  source ~/projects/pyblog/venv/bin/activate
  ~~~	
- Install the application's dependencies (See the *requirements.txt* file).
  ~~~	
	pip install -r ~/projects/pyblog/requirements.txt
  ~~~
- Set the application's configuration keys (See the *config.py* file)[^1].
  [^1]: [Google: Sign in with app passwords](https://support.google.com/accounts/answer/185833?hl=en)
  ~~~
  export PYBLOG_DEVELOPMENT_SECRET_KEY="Substitute this for a random string"
  export PYBLOG_MAIL_USERNAME="Substitute this for your gmail address"
  export PYBLOG_MAIL_PASSWORD="Substitute this for your Google app password"
  ~~~
- Create a SQLite database.
  ~~~
  flask --app ~/projects/pyblog/pyblog shell
  ~~~
  ~~~
  Python 3.10.12 (main, Jun 11 2023, 05:26:28) [GCC 11.4.0] on linux
  App: pyblog
  Instance: ~/projects/pyblog/instance
  >>> db.create_all()
  >>> exit()
  ~~~
- Run the application.
  ~~~
  flask --app ~/projects/pyblog/pyblog run
  ~~~
- Enter the local server address and port number (http://127.0.0.1:5000/) that are generated in the browser's search bar.
