class NotificationService:
    async def notify_new_order(
        self, tg_ids: list[int], order_id: int, transport_type: str
    ):
        from src.api.bot.setup import bot

        for tg_id in tg_ids:
            try:
                text = (
                    f"*Новый заказ №{order_id}*\n"
                    f"Нужен трансопрт: {transport_type}\n"
                    f"Заходите в 'Мои Заявки', чтобы откликнуться!"
                )
                await bot.send_message(chat_id=tg_id, text=text, parse_mode="Markdown")
            except Exception as e:
                print(f"Ошибка отпраки пользователю {tg_id} {e}")
