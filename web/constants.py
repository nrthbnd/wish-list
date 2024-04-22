from datetime import datetime

# core/config
APP_TITLE = 'Приложение для создания списка пожеланий'
ENV_FILE_NAME = '.env'

# models/custombase
CREATE_DATE_DEFAULT = datetime.utcnow
CLOSE_DATE_DEFAULT = None
# models/wish
WISH_NAME_MAX_LEN = 100
COMPLETED_DEFAULT = False
RESERVED_DEFAULT = False
LINK_URL_MAX_LEN = 2000
LINK_URL_DEFAULT = None
# models/reservation
WISH_ID_FOREIGN_KEY = 'wish.id'

# schemas/wish
WISH_NAME_MIN_LEN = 1
WISH_NAME_MAX_LEN = 100
COMMENT_MIN_LEN = 1
EMPTY_FIELD_ERROR = 'Поле {} не может быть пустым!'
CREATE_DATE = datetime.now().isoformat(timespec='seconds')

# api/validators
NAME_DUPLICATE_EXCEPTION = 'Пожелание с таким названием уже существует!'
WISH_NOT_EXISTS_EXCEPTION = 'Пожелание не найдено!'
WISH_ALREADY_RESERVED = 'Это пожелание уже забронировано!'
WISH_ALREADY_COMPLETED = 'Это пожелание уже выполнено!'
RESERVATION_NOT_EXISTS_EXCEPTION = 'Бронирование не найдено!'
NOT_ALLOWED_TO_DELETE_WISH = 'Нельзя удалять забронированное пожелание!'
NOT_ALLOWED_TO_RESERVATION = 'Данное действие доступно только владельцу объекта бронирования!'
NOT_ALLOWED_TO_WISH = 'Данное действие доступно только владельцу объекта пожелания!'

# api/routers
WISH_ROUTER_PREFIX = '/wishes'
WISH_ROUTER_TAG = 'Wishes'
RES_ROUTER_PREFIX = '/reservations'
RES_ROUTER_TAG = 'Reservations'
PAGES_ROUTER_PREFIX = '/pages'
PAGES_ROUTER_TAG = 'Pages'
USERS_ROUTER_PREFIX = '/users'
USERS_ROUTER_TAG = 'users'

# api/endpoints/wish
CLEAR_ROUTE = '/'
WISH_ID_ROUTE = '/{wish_id}'
SWITCH_FIELD_COMPLETED = 'completed'

# api/endpoints/reservation
RESERVATION_ID_ROUTE = '/{reservation_id}'
SWITCH_FIELD_RESERVED = 'reserved'

# api/endpoints/users
USER_WISHES = '/users/{id}/wishes'
USER_NAME = 'users/{id}/info'
