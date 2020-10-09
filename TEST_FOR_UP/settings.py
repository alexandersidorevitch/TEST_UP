try:
    from .deploy_settings import *
except ImportError:
    from .settings_local import *
