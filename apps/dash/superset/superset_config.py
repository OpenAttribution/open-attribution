# Superset specific config
ROW_LIMIT = 5000

# Flask App Builder configuration
# Your App secret key will be used for securely signing the session cookie
# and encrypting sensitive information on the database
# Make sure you are changing this key for your deployment with a strong key.
# Alternatively you can set it with `SUPERSET_SECRET_KEY` environment variable.
# You MUST set this for production environments or the server will not refuse
# to start and you will see an error in the logs accordingly.
SECRET_KEY = "Mub5QPSdu10uAEjBRdsiEFYd+XQjACQ26u1Od5oNxwNo6tsIhq/I+mMy"

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
# The check_same_thread=false property ensures the sqlite client does not attempt
# to enforce single-threaded access, which may be problematic in some edge cases
SQLALCHEMY_DATABASE_URI: str = (
    "sqlite:////home/james/app-track/superset/superset.db?check_same_thread=false"
)

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED: bool = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST: list = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT: int = 60 * 60 * 24 * 365

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY: str = ""
