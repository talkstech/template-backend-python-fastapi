# fastapi-microservice-template

This is an opinionated template for a [FastAPI](https://fastapi.tiangolo.com/).

This template supports being run:

- Locally using [uvicorn](https://www.uvicorn.org/)
- Through Docker with uvicorn (optionally run through [Gunicorn](https://gunicorn.org/))

---

## Documentation Links

**If you want to skip down to the Get Started section, [here you go!](#get-started)**

### Libraries

- [FastAPI](https://fastapi.tiangolo.com/) (Web framework)
  - [Starlette](https://www.starlette.io/) (ASGI toolkit FastAPI builds on)
- [pydantic](https://pydantic-docs.helpmanual.io/) (Data validation)
- [Mangum](https://mangum.io/) (ASGI adapter for Lambda)
- [Loguru](https://loguru.readthedocs.io/en/stable/index.html) (Logging)

### Deployment

- [uvicorn](https://www.uvicorn.org/)
- [Gunicorn](https://docs.gunicorn.org/en/stable/)

### [pre-commit](#pre-commit)/[Formatting](#formatting)

- [pre-commit](https://pre-commit.com/) (pre-commit hook management)
  - [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks) (Out of the box hooks)
- [Black](https://black.readthedocs.io/en/stable/) (Code formatting)
- [isort](https://pycqa.github.io/isort/) (Import sorting)
- [Flake8](https://flake8.pycqa.org/en/latest/) (Linting)
- [mypy](https://mypy.readthedocs.io/en/stable/) (Type checking)

### Other

- [Python 3.11](https://docs.python.org/3.11/reference/)
  - [venv](https://docs.python.org/3.11/library/venv.html) (Virtual enviroment management)
  - [pip](https://pip.pypa.io/en/stable/) (Python package management)

---

## Get Started

You're going to need a couple of prerequisites:

- Python 3.11](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)

To find the version of your Python installation run:

*Note:* For Windows users always replace `python3` with `py` or `python`

### Virtual Enviroment

It's highly recommended to use a virtual enviroment to help with Python versioning and depedency hell ([xkcd](https://xkcd.com/1987/)). I'm not going to talk about them too much, but a great article can be found [here](https://realpython.com/python-virtual-environments-a-primer).

To create your virtual enviroment run:

```zsh
~ python3 -m venv venv
```

On MacOS and Linux run the following to activate:

```zsh
~ source venv/bin/activate
```

On Windows run:

```cmd
> venv\Scripts\activate.bat
```

On both platforms, if you wish to deactivate the virtual enviroment run:

```zsh
(venv) ~ deactivate
```

Everytime you open a new terminal you'll need to activate the virtual enviroment.

### Dependencies

To start, you'll need to install the provided dependencies. This can be done by running:

```zsh
(venv) ~ pip install -r dev-requirements.txt
```

### Code Structure

Feel free to modify the layout of the repo as much as you want but the given structure is as follows:

```
app/
├── __init__.py
├── main.py
├── dependencies.py
├── middlewares/
│   └── execution_time_logging.py
├── routers/
│   └── users.py
├── models/
│   └── user.py
└── stores/
    └── user.py
tests/
├── test_main.py
└── routers/
    └── test_users.py
requirements.txt
dev-requirements.txt
```

**Note:** all the files with "user" in the name are files to demonstrate the recomended structure. They form two endpoints defined in `routers/users.py`.

This file structure is effectively an extension of the recomended file structure for "bigger applications" which can be found [here](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

`__init__.py` defines and initializes the app configuration.

`main.py` defines the FastAPI application, adds middleware, includes routers, and creates the Mangum handler.

`dependencies.py` defines... 🎉 dependencies 🎉! This is where you can put common parameters or basic authentication. If necessary this module can be split up into a package.

`middlewares/` is where custom middleware can be placed. The middleware used to log endpoint execution time is defined here.

`routers/` is for modules defining routers (pretty self explanatory). Again, this can be expanded into even more nested packages but at that point you might be leaving "microservice" territory.

`models/` is the space to define input, output and database models. Once this grows it could be split into `models/db/` and `models/io/` if desired.

`stores/` is the space to define database or "store" interfaces and corresponding wrapper classes. If that doesn't make sense right now, take a look at `stores/user.py` and how it's used in `routers/users.py`.

`tests/` should mimic the file structure of `routers` when defining tests. To see how to use the FastAPI testing system look [here](https://fastapi.tiangolo.com/tutorial/testing/).

Now, you might want to spend a little bit of time starting at `main.py` and looking through the code to see how it's structured in practice. Once your done, and you want to delete the example code:

- Delete the files
  - `app/routers/users.py`
  - `app/models/user.py`
  - `app/stores/user.py`
  - `tests/routers/test_users.py`
- Delete parts involving "user(s)" in
  - `app/main.py`
  - `app/dependencies.py`

### Running Locally

To run your microservice locally you either need to create a new `.env.local` file for your local configuration, or use a `.env` file for an existing stage. To use an enviroment file, the enviroment variable `STAGE` must be set to the stage of the file. For example:

If you want to use the `.env.staging` enviroment run the following on MacOS and Linux:

```zsh
~ export STAGE=staging
```

On Windows:

```cmd
> set STAGE=staging
```

Then run uvicorn from the root of your project using:

```zsh
~ uvicorn app.main:app --reload
```

This will host your API on `localhost` bound to port `8000` by default. When you update and save a file it will automatically reload.

### Running With Docker

While this template primarily supports running serverlessly, it can also be run with Docker. There are two independent Dockerfiles to support this: One where uvicorn is used on its own for use running on a cluster, and one which runs multiple uvicorn workers through Gunicorn for use on a single server or locally.

#### On a Cluster

In short, if you have some sort of cluster of machines running Docker containers, you will likely want to create multiple Docker containers instead of running multiple uvicorn instances in one. To do this you can use the Dockerfile at `docker/cluster/Dockerfile`.

With Docker running, build the image by running:

```zsh
~ docker build -t my-image -f docker/cluster/Dockerfile ./
```

**Note:** You can change the name of the image by replacing `my-cluster-image` with whatever you want.

Now you have an image which you can run by whatever mechanism you wish. You will have to expose port 80 and specify the `.env` file you want to use. To run it detached locally with the `.env.staging` file run:

```zsh
~ docker run -d -p 80:80 --env-file .env.staging my-cluster-image
```

#### On a Server

If you are running your Docker container on a single server or locally, you will likely want to use the Dockerfile at `docker/server/Dockerfile. This file uses the base Dockerfile by [tiangolo](https://github.com/tiangolo) found [here](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker). It will use Gunicorn to start some number of uvicorn workers. That number will be determined automatically by the number of cores the system has.

With Docker running, build the image by running:

```zsh
~ docker build -t my-server-image -f docker/server/Dockerfile ./
```

**Note:** You can change the name of the image by replacing `my-server-image` with whatever you want.

Now you have an image which can again be run any way you wish. Just make sure you expose port 80 and specify the `.env` file you want to use. To run it detached locally with the `.env.staging` file run:

```zsh
~ docker run -p 80:80 --env-file .env.staging my-server-image
```

## Formatting

The recomended code format is [Black](https://black.readthedocs.io/en/stable/). isort is also run as a part of the pre-commit hooks by default. To save yourself a lot of effort you can enable these to run on save in your editor or IDE. Details for [VS Code](https://code.visualstudio.com/) are below, but a tutorial for your editor can often be found by Googling "automatically reformat code on save in **[Insert Editor Name Here]**".

<details>
<summary>Autoformatting in VS Code</summary>
<br>
If you don't already, you'll need an installation of VS Code with the Python plugin installed. You can find a guide to do that <a href="https://code.visualstudio.com/docs/python/python-tutorial">here</a>. You'll also need to have setup your virtual enviroment as instructed in the <a href="#get-started">Get Started</a> section.
<br><br>
Open the Settings editor with the keyboard shortcut (<code>⌘</code>+<code>,</code> or <code>Ctrl</code>+<code>,</code>) or by going:
<ul>
  <li>On Windows/Linux - <b>File > Preferences > Settings</b></li>
  <li>On macOS - <b>Code > Preferences > Settings</b></li>
</ul>
<br>
In the search bar, enter "Python Formatting Provider" and select "black" from the dropdown menu.
Then, search for "Editor: Format on Save" and enable it.
Finally, enabling isort requires a bit more work. Search for "Editor: Code Actions On Save" and click "Edit in settings.json".
<br><br>
Add the following line:

```json
"editor.codeActionsOnSave": {
    "source.organizeImports": true
}
```

Done! Go ahead and try it out.

---

</details>

### pre-commit

Using pre-commit is not required but heavily encouraged. It's an easy way to make sure that style is followed and simple bugs are found before code even makes it to a pull request. On commit, Black, isort, Flake8, and [mypy](#mypy) are run and if any changes are made or errors are raised the commit will fail. Changes will then need to be staged and everything commited again.

To start using pre-commit with the provided config (located in `.pre-commit-config.yaml`) run:

```zsh
(venv) ~ pre-commit install --install-hooks
```

**Note:** The `--install-hooks` flag is optional but you save time on your first commit by installing them now.

**Note 2:** The installed pre-commit hooks do not get commited. Everybody working on the repo will have to run the above command.

### Other Useful Commands**

- `pre-commit run` - Run hooks on currently staged files
- `pre-commit run --all-files` - Run hooks on all files in repo
- `pre-commit autoupdate` - Auto-update pre-commit config to the latest repos' versions

#### mypy

mypy is a Python static type checker, that is run by default in pre-commit. However, it can be a bit of a double-edged sword. It has a lot of benefits including being able to catch bugs that wouldn't even be found with 100% code coverage. Personally, I use it on every project with `strict` mode enabled. The default configuration is relatively lenient but if you find it too pedantic for your needs, you can disable some features in `setup.cfg` or remove it entirely from `.pre-commit-config.yaml`. If you wish to enable additional features, those can be added in `setup.cfg`.
