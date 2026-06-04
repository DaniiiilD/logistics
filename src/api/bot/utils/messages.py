class BotMessages:
    class AUTH:
        ENTER_EMAIL = "Введите Email для входа:"
        INVALID_EMAIL= "Это не похоже на Email. Попробуйте еще раз"
        USER_NOT_FOUND = "Пользователь с таким Email не найден в системе"
        CODE_SENT ="Код подтверждения отправлен на вашу почту. Введите его:"
        SUCCESS = "Вход выполнен успешно!"
        INVALID_CODE = "Невверный код или истек срок его действия истек. Поробуйте еще раз:"
        
    class Menu:
        PRFILE = (
            "Ваш прифиль:\n"
            "ФИО: {user.driver.full_name}\n"
            "Телефон: {user.driver.phone}\n"
            "Трансопрт: {user.driver.transport_type}"
        )
        NOT_FOUND = "Профиль не найден. Пожалуйста авторизуйтесь!"
        HELP = "Здесь будет помощь по навигации и работе с заказами."

    class Orders:
        NO_ACTIVE = "Активных заявок пока нет."
        AVAILABLE_LIST = "*Список доступных заявок:*"
        OUTDATED ="Заказ больше не актуален"
        DETAIL = (
            "*Заказ №{order_id}*\n\n"
            "*Отправитель:* {company_name}\n"
            "*Тип авто:* {transport_type}\n"
            "*Даты доставки:* {from_date} - {to_date}\n"
        )
        CONFIRM_APPLY = "*Вы увернеы что хотите откликнуться на заказ №{order_id}*"
        USER_NOT_FOUND = ("Ошибка: пользователь не найден.")
        APPLY_SUCCESS =(
            "*Заявка на заказ №{order_id} успешно отправлена!*\n\n"
            "Компания получила ваше уведомление. Если вас выберут, бот пришлет сообщение.",
        )
        APPLY_ERROR = ("Произошла ошибка при отправке заявки.")
        
    class Start:
        ACCOUNT_LINKED = ("Аккаунт успешно привязан!")
        ACCESS_DENIED = ("Доступ Запрещен. Этот бот прeдназначен для водителей.")
        WELCOME_BACK = ("С возвращением, {user.driver.full_name} if {user.driver} else 'Водитель'}!")
        WELCOME_NEW = "Добро пожаловать! Пожалуйста, авторизуйтеся для работы."
    
    class NOTIFICATIONS:
        NEW_ORDER = (
            "*Новый заказ №{order_id}*\n\n"
            "Нужен транспорт: {transport_type}\n\n"
            "Заходите в 'Мои Заявки', чтобы откликнкуться!"
        )