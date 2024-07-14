BOT_TOKEN = ''

ENV_PROD = 'prod'
ENV_TEST = 'test'

ENV_TEST_WORDS = ['test', 'тест', 'тесте']

STATUS_WAITING = 'waiting'
STATUS_PROCESSING = 'processing'
STATUS_FINISHED = 'finished'
STATUS_CANCELLED = 'cancelled'

SMILE_STATUS = {
    STATUS_WAITING:     '🔴',
    STATUS_PROCESSING:  '🟡',
    STATUS_FINISHED:    '🟢',
    STATUS_CANCELLED:   '🟣'
}

SERVICE_NAME = {
    'a': 'arcadia',
    'infra': 'infra',
    'st': 'tracker',
    'yd': 'deploy'
}

