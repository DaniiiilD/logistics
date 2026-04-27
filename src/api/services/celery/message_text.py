class NotificationMessages:
    @staticmethod
    def new_order(order_id: int, transport_type: str) -> str:
        return (
            f"Здравствуйте! Появилась новая заявка на перевозку №{order_id}."
            f"Требуемый транспорт: {transport_type}."
            f"Зайдите в приложение, чтобы откликнуться."
        )

    @staticmethod
    def new_offer_to_company(order_id: int) -> str:
        return f"На ваш заказ №{order_id} откликнулся новый водитель.Проверьте список откликов!"

    @staticmethod
    def offer_accepted(order_id: int) -> str:
        return f"Поздравляем! Ваш отклик на заказ №{order_id} принят."

    @staticmethod
    def offer_rejected(order_id: int) -> str:
        return f"К сожалению, на заказ №{order_id} был выбран дургой водитель."
