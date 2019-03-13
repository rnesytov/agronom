
Email-авторизация
-----------------

`/api/v0_1/auth/send_activation_mail/` - auth_id не передавать,
email - email, на который в продакшене будет отправляться письмо.
В ответ прийдёт `auth_id`.

Повторная отправка письма производится таким же запросом (без auth_id).

Заходим в почту.
Там будет письмо вида
Your activation link is http://api.master.agronom.takewing.ru/api/v0_1/auth/activate/?email=YOUR_EMAIL&hash=YOUR_HASH
Копируем ещё и YOUR_HASH. Открывать ссылку не нужно, она всё равно не работает вне приложения.

`/api/v0_1/auth/verify_magic_link/{auth_id}/{activation_hash}/`
`auth_id` - получен при запросе, `activation_hash` - в письме.
Если всё правильно, то будет получен access token, что означает,
что авторизация прошла успешно.


Авторизация через соцсети
-------------------------

Авторизация приложения VK

https://oauth.vk.com/authorize?client_id=6878710&display=page&redirect_uri=http://takewing.ru&scope=email,offline&response_type=code&v=5.92

Авторизация приложения Facebook

https://www.facebook.com/v3.2/dialog/oauth?client_id=385739375589666&redirect_uri=https://takewing.ru/&scope=email&state=1

Авторизация приложения Google

https://accounts.google.com/o/oauth2/v2/auth?scope=profile%20email&access_type=online&include_granted_scopes=false&state=1&redirect_uri=https://takewing.ru&response_type=code&client_id=211000367150-89rkp2p1ln0b3jskv0jeb42cae4b4i7b.apps.googleusercontent.com

После авторизации вас перекидывает на http://takewing.ru/?code=YOUR_CODE
(неважно, что этот URL не открывается).

Далее `/api/v0_1/auth/oauth_login/` - type - vk, access_code - YOUR_CODE
Он вернет auth_id.

Далее `/api/v0_1/auth/oauth_verify/{auth_id}/`

::

    {
        "is_data_extraction_finished": true,  // Если false, то надо подождать и еще раз запросить
        "access_token": null,  // Если не null, то пользователь уже регистрировался и его авторизация закончена
        "email": "d.musin@takewing.ru",  // null, если не удалось получить
        "first_name": "Дмитрий"  // null, если не удалось получить. Нормализации имени на данный момент нет
    }

`/api/v0_1/auth/send_activation_mail/` - auth_id **тот же auth_id, что был получен на первом шаге**,
email - email, на который будет отправляться письмо.
В ответ прийдёт access_token, если email совпадают, иначе отправится письмо.
Повторная отправка письма: тот же auth_id, email тот же, либо другой (если пользователь решил изменить email).
