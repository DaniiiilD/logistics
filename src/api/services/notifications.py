from src.core.security import decrypt_tg_id
from src.api.bot.utils.messages import BotMessages
import logging
from src.api.bot.bot_instance import bot
        
logger = logging.getLogger(__name__)

class NotificationService:
    async def notify_new_order(
        self, encrypted_tg_ids: list[str], order_id: int, transport_type: str
    ):

        for enc_id in encrypted_tg_ids:
            try:
                real_tg_id = decrypt_tg_id(enc_id)
                text = BotMessages.NOTIFICATIONS.NEW_ORDER.format(
                    order_id=order_id,
                    transport_type=transport_type
                )
                
                await bot.send_message(chat_id=real_tg_id, text=text, parse_mode="Markdown")
            except Exception as e:
                logger.error(f'Ошибка отправки уведомления в TG для {real_tg_id}:{e}', exc_info=True)
