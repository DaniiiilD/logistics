# test_realtime.py
import asyncio
from src.api.services.centrifugo.realtime import RealtimeService

async def main():
    print("=== ЗАПУСК ТЕСТА CENTRIFUGO ===")
    
    # Инициализируем наш сервис
    service = RealtimeService()
    print(f"[*] Используемый URL: {service.api_url}")
    print(f"[*] Используемый ключ: {service.api_key}")
    
    print("\n[*] Отправка тестового отклика...")
    
    # Пытаемся отправить сообщение напрямую для компании 6
    success = await service.notify_new_offer(
        company_id=6,
        order_id=999,
        driver_name="Тестовый Водитель",
        transport_type="грузовик"
    )
    
    if success:
        print("\n🎉 УСПЕХ! Тестовый запрос успешно долетел до Centrifugo!")
    else:
        print("\n❌ СБОЙ! Запрос был отклонен или не долетел.")

if __name__ == "__main__":
    asyncio.run(main())