from src.core.config import settings
import httpx
import asyncio
import logging

logger = logging.getLogger(__name__)

class RealtimeService:
    def __init__(self):
        self.api_url = f"{settings.CENTRIFUGO_API_URL}/publish"
        self.api_key = settings.CENTRIFUGO_API_KEY
        
    async def notify_new_offer(
        self,
        company_id: int,
        order_id : int,
        driver_name : str,
        transport_type : str,
    ) -> bool:
        """
        Отправляет real - time уведомление в Centrifugo для конкетрной компании
        """
        channel_name = f"company_orders_{company_id}"
        
        headers = {
            "X-API-Key": self.api_key,
            "Content-type": "applocation/json"
        }
        
        payload = {
            "channel": channel_name,
            "data": {
                "event" : "new_offer",
                "order_id": order_id,
                "driver_name": driver_name,
                "transport_type": transport_type
            }
        }
    
        try:
            
            print(f" [DEBUG] Отправляем запрос на URL: {self.api_url}")
            print(f" [DEBUG] С ключом авторизации: {self.api_key}")
            print(f" [DEBUG] Тело запроса (payload): {payload}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, headers=headers, json=payload)
                
                print(f" [DEBUG] Centrifugo ответил кодом: {response.status_code}")
                print(f" [DEBUG] Тело ответа: {response.text}")
                
                if response.status_code == 200:
                    logger.info(f"Уведомление успешно установлено в Centrifugo для компании {company_id}")
                    return True
                else: 
                    logger.error(f"Centrifugo вернул ошибку {response.status_code}: {response.text}")
                    return False
                
        except Exception as e:
            print(f" [DEBUG] ИСКЛЮЧЕНИЕ ПРИ ОТПРАВКЕ: {str(e)}")
            logger.error(f"Ошибки при отправке запроса в Centrifugo: {str(e)}", exc_info=True)
            return False