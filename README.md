KidsOut downloader
==================

Что это?
--------
Скрипт для скачивания всех анкет с kidsout.ru для последующего поиска по ним грепом.

Как это использовать?
---------------------

Создать виртуальное окружение и активировать его:

    ./bootstrap
    source env/bin/activate

Сначала надо скопировать куки из браузера в `config.py` примерно в таком виде:

    COOKIES = 'XSRF-TOKEN=QW4RitUyi....'

Куки можно достать из браузера, через консоль разработчика.

Далее надо запустить скрипт `donwload-ankets.py`, который сложит все анкеты в
HTML виде в директорию ankets.


После чего по ним можно искать с помощью grep:

    grep -c область ankets| grep -v ':0'
    # потом открыть в браузере
    open ankets/token.html
