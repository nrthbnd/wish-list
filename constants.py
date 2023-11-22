from datetime import datetime

# core/config
APP_TITLE = 'Поддержка котиков QRKot'
DATABASE_URL = 'sqlite+aiosqlite:///./fastapi.db'
SECRET = 'SECRET'
ENV_FILE_NAME = '.env'

# models/custombase
CREATE_DATE_DEFAULT = datetime.utcnow
CLOSE_DATE_DEFAULT = None

# models/wish
WISH_NAME_MAX_LEN = 100
COMPLETED_DEFAULT = False
RESERVED_DEFAULT = False

# models/reservation
WISH_ID_FOREIGN_KEY = 'wish.id'
