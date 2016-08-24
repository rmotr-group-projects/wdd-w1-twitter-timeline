# Django project setup

This is a simple guide to explain how to setup your Django project. We'll use the `twitter-clone` example.

### Virtualenv and django-admin options

You'll have to setup a Django project from scratch. The first step is to create your virtualenv and install the dependencies:

```bash
$ mkvirtualenv twitter-clone
$ pip install -r requirements.txt
```

Then you can setup the Django project and the django app using:

```bash
$ django-admin startproject twitter_clone
$ cd twitter_clone
$ django-admin startapp twitter
```
_(It's important to respect the names, as the test are importing modules using those names)_

Now we can start working with our Django project. We could try running the migrations and using the shell:

```bash
$ django-admin migrate
```

😬 Did that fail? Well, that's expected. 👹 Django needs a little setup to work properly. First it needs to know where are your projects settings located. In our case, the settings file is located in `twitter_clone/twitter_clone/settings.py`. We'll use the `--settings` option to specify the location of our settings:

```bash
$ django-admin migrate --settings twitter_clone.settings
```

😭 But that will also fail, because Django can't "see" the package `twitter_clone`. So you could try `cd`ing into the `twitter_clone` directory and running your command there (it should work, try it), but that's not really scalable. `django-admin` also supports the `pythonpath` option to specify a directory to add to the python path:

```bash
$ django-admin migrate --settings twitter_clone.settings --pythonpath twitter_clone
```

🎉 It should work now! Be careful as we're passing a relative path for the `pythonpath` option. If you move around, you'll have to change it.

#### Using environment variables instead of options

Personally, we prefer to use environment variables instead of options for the django-admin command, you'll see why later. To achieve the same results as before with envvars you can pass the `DJANGO_SETTINGS_MODULE` envvar (instead of `--settings`) and `PYTHONPATH` (instead of `--pythonpath`):

```bash
$ DJANGO_SETTINGS_MODULE=twitter_clone.settings PYTHONPATH=twitter_clone django-admin migrate
```

As you can see, it's pretty much the same (a little bit more verbose maybe). But the good news are that you can export those env vars and avoid repeating them every time you run your command:

```bash
$ export DJANGO_SETTINGS_MODULE=twitter_clone.settings
$ export PYTHONPATH=twitter_clone
$ django-admin migrate
```

While you're in the same shell session, you can use the `django-admin` command without having to specify the env vars again. The problem is that if you close the session, you'll have to set them again. We need a way to set those variables every time we're working on our Django project. Virtualenvwrapper to the rescue 💪! Virtualenvwrapper provides a few _hooks_ that are invoked anytime you activate or deactivate your virtualenv. They're simple shell scripts called `postactivate` and `postdeactivate` (there are more hooks, we encourage you to take a look) and they're located in a directory called `bin` under your virtualenv home dir (usually `.virtualenvs/[VIRTUALENV-NAME]/bin`). That means we can put our `export` statements in the `postactivate` file in order to have the variables exported every time we activate our virtualenv.

This is how my `.virtualenvs/twitter-clone/bin/postactivate` file looks like for me:

```bash
#!/bin/zsh
# This hook is sourced after this virtualenv is activated.

export OLD_PYTHONPATH=${PYTHONPATH}
export PYTHONPATH=twitter_clone:${PYTHONPATH}
export DJANGO_SETTINGS_MODULE=twitter_clone.settings
```

I'm keeping a reference to the old python path so I can restore it back as it was after the virtualenv is deactivated. Basically, when I deactivate my virtualenv, I want to restore everything as it was before activating it, cleaning up the env vars that I've created so they don't produce conflicts with other projects. This is my `.virtualenvs/twitter-clone/bin/postdeactivate` file:

```bash
#!/bin/zsh
# This hook is sourced after this virtualenv is deactivated.

unset DJANGO_SETTINGS_MODULE
export PYTHONPATH=${OLD_PYTHONPATH}
unset OLD_PYTHONPATH
```

## setup_venv command

To ease this process for you, we have included a tiny script that will write these environment variables for you:

```bash
$ ./setup_venv.sh twitter_clone
```

**Important:** You should execute the command in an active virtualenv.
