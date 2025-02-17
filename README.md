# Ged-go
A Gedcom viewer web app.

Original by Greg Thole 2021 Fork by Gord Tulloch 2025
Objective: Update to new versions of Python and Packages

## About

Ged-go is a Gedcom file viewer web app written in Django with d3.js
visualizations and Bootstrap for mobile scaffolding, with the idea that a
genealogy website and gedcom viewer can be beautiful and intuitive.

Most of the web-based genealogy software out there is pretty ugly and
difficult to navigate in.  There are often silly little icons and
information is presented in hard to read tables.  Instead, the philosophy of
Ged-go is to have fewer features, but to present a gedcom in a clear and well
designed way.


## Features

- Individual view
  - Easy to read podded display
  - Pedigree charts
  - Timeline of events coincided with major world historical events
- Gedcom view
- Basic search
- Blog
  - Tag people in a blog post, and those posts automatically appear in that
    person's individual view.
- Page for displaying documentary videos
- Email contact form
- Secure login and Admin pages
- Gedcom parser and update mechanism
- Automatic thumbnail creation
- Responsive design for all levels of mobile browsing


## Development Environment Setup

Development installation is fairly straight-forward.  We use the Docker toolbox
to abstract away dependencies on the development environment so you don't have
to install packages or a have a database running in order to get started.

#### Dependencies

Download and install [Docker](https://www.docker.com/community-edition).  Test
that it works with `$ docker ps`

Clone this repo and `cd` into it.

```bash
# Build the docker images
$ docker-compose build
```

#### Importing Data

With the images built locally, you can import data from your gedcom file into
the application.

Copy any documents (like photos or PDFs) that your gedcom file references into
`./files/gedcom/` (you may need to create that directory), and copy your
gedcom to the base gedgo directory.

Then run the import:

```bash
# Create the database tables
$ docker-compose run app python manage.py migrate

# Create a user for yourself
$ docker-compose run app python manage.py createsuperuser

# Import your gedcom file
$ docker-compose run app python manage.py add_gedcom your-gedcom-file.ged
```

The initial import may take a while, since it creates thumbnails for any
images.

#### Running the application

Start up the web server and worker with

```bash
$ docker-compose up
```

If you're running a Mac you can go to [http://gedgo.local](http://gedgo.local),
or just [localhost](http://localhost).

#### Overriding settings

Drop any settings overrides (like `SECRET_KEY` or `EMAIL_*` settings) in
`./settings_local.py` to have them auto-imported into your setup.

#### Using Dropbox Files
Dropbox generates previews for more types of files than are supported with the
base file system storage.  Storing your gedcom images and documents there can
also make it easier to keep them in sync between your genealogy application and
the Gedgo server.

To do this, get a Dropbox OAuth token, and add it to your local settings and
tell Gedgo to use the Dropbox storage:

```
DROPBOX_ACCESS_TOKEN = '<your-access-token>
GEDGO_GEDCOM_FILE_STORAGE = 'gedgo.storages.DropBoxSearchableStorage'
GEDGO_GEDCOM_FILE_ROOT = '<dropbox path to your genealogy files>'
```

#### Updating Gedcoms
To update your gedcom, you can either use the manage.py command, passing it
the integer ID of the gedcom object you'd like to update, for example:

```bash
$ docker-compose run app python manage.py update_gedcom 1 your-gedcom-file.ged
```

Or, with the Celery worker running, you can use the web interface.


#### Running the tests
You can run the unit tests with:

```bash
$ docker-compose run app ./test.sh
```
