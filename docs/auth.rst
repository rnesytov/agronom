===========
Авторизация
===========

BASE URL: /api/v0_1/auth/
-------------------------

Авторизация приложения VK

https://oauth.vk.com/authorize?client_id=6878710&display=page&redirect_uri=http://takewing.ru&scope=email,offline&response_type=code&v=5.92

Авторизация приложения Facebook

https://www.facebook.com/v3.2/dialog/oauth?client_id=385739375589666&redirect_uri=https://takewing.ru/&scope=email&state=1

Авторизация приложения Google

https://accounts.google.com/o/oauth2/v2/auth?scope=profile%20email&access_type=online&include_granted_scopes=false&state=1&redirect_uri=https://takewing.ru&response_type=code&client_id=211000367150-89rkp2p1ln0b3jskv0jeb42cae4b4i7b.apps.googleusercontent.com

Авторизация через соцсети [POST] auth/oauth_login/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    {
      "type": "vk",  // vk, fb, ga
      "access_code": "code obtained from social media, required"
    }

Возможные ответы

::

    STATUS 201
    {
      "auth_id": "3176f3ee-0c23-48b6-95aa-a9ce3771d8ae"
    }

Получение данных о пользователе [GET] oauth_verify/{auth_id}/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Возможные ответы

::

    STATUS 200
    {
      "is_data_extraction_finished": true,  // закончен ли запрос данных, если нет, ретраим
      "access_token": null,  // если не null, то пользователь авторизован
      "email": null,  // если не null, то мы получили почту от соцсети
      "first_name": null  // если не null, то мы получили имя от соцсети
    }


Отправка email [POST] send_activation_mail/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    {
      "auth_id": "UUID-4 string, nullable, null при авторизации через email",
      "email": "user email, required",
    }


Возможные ответы

::

    STATUS 201
    {
        "auth_id": "e8f910e2-500f-405f-b11e-fd8b11e8c765"
        "access_token": null,  // если не null, то пользователь авторизован (email тот же что получен от соцсети)
        "next_email_time": 1551797417,  // ближайшее время следующей отправки email
    }


::

    STATUS 400
    {
        "email": [
            "Enter a valid email address."
        ]
    }


Верификация ссылки [GET] verify_magic_link/<auth_id>/<activation_hash>/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    auth_id: "Auth id, UUID4",
    activation_hash: "Activation hash from magic link, UUID4",

Возможные ответы

::

    STATUS 200
    {
      "access_token": "40 symbols string",
      "name": "first name, 32 symbols max, nullable",
    }

::

    STATUS 404
    {
        "detail": "Not found." // pair auth_id:activation_hash not found, expired or used
    }
