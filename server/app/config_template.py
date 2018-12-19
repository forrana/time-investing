# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

MONGODB_SETTINGS = {
  'DB': 'time_investement',
  'host': 'mongo',
  'port': 27017,
}

USER_APP_NAME = "Time investing"      # Shown in and email templates and page footers
USER_ENABLE_EMAIL = False      # Disable email authentication
USER_ENABLE_USERNAME = True    # Enable username authentication
USER_REQUIRE_RETYPE_PASSWORD = True    # Simplify register form

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "enter here super secret session key"

# Secret key for signing cookies
SECRET_KEY = "enter here super secret secret key"

FACEBOOK_CLIENT_ID = ''
FACEBOOK_CLIENT_SECRET = ''

GOOGLE_CLIENT_ID = 'your-ket.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'your-secret'
