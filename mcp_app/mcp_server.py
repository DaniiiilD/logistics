from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from src.api.handlers.company.order import create_order_service_manual
from src.api.handlers.user import create_user_service_manual
from src.api.handlers.driver.offer import create_offer_service_manual
from mcp_app.middleware import DatabaseMiddleware
from fastapi import HTTPException

mcp = FastMCP("Logistics")
mcp.add_middleware(DatabaseMiddleware())

order_serivce = create_order_service_manual()
user_serivce = create_user_service_manual()
offer_service = create_offer_service_manual()

@mcp.tool()
async def get_available_orders(transport_type: str = 'грузовик') -> str:
    """ 
    Инструмент для ИИ: получить список заказов по типу транспорта
    """
    try:
        orders, _ = await order_serivce.get_orders_for_bot(transport_type=transport_type, page = 0)
            
        if not orders:
            return f"Заказов для транспорта '{transport_type}' не найдено."
            
        orders_strings = []
        
        for order in orders:
            order_info = (
                f"Заказ №{order.id}: "
                f"Транспорт - {order.transport_type}, "
                f"Компания - {order.company.company_name}"
            )
            orders_strings.append(order_info)
                
        return "Вот список доступных заказов:\n" + "\n".join(orders_strings)
    
    except Exception as e:
        raise ToolError(f"Не удалось получить список доступных заказов: {str(e)}")


@mcp.tool()
async def get_order_info(order_id: int) -> str:
    """ 
    Получить детальную информацию о конкретном заказе по его ID.
    Используй это, когда пользователь выбрал заказ и хочет узнать даты или название компании
    """
    try:
        order = await order_serivce.get_order_with_details_for_drivers(order_id)
        
        if not order:
            return f"Заказ №{order_id} не надйен"
        
        result = (
            f"Детальная информация по заказу №{order.id}: \n"
            f"Компания: {order.company.company_name}\n"
            f"Тип транспорта: {order.transport_type}\n"
            f"Срок доставки: {order.from_date.date()} - {order.to_date.date()}\n"
            f"Статус в базе: {order.status}"
        )
        
        return result
    
    except Exception as e:
        raise ToolError(f"Не удалось получить детальную информацию о заказе: {str(e)}")

@mcp.tool()
async def calculate_trip_cost(days: int) -> str:
    """
    Рассчитать ориентировочную стоимость поездки в зависимости от количества дней в пути.
    Используй это, когда водитель интересуется, сколько он заработает за рейс определенной длительности
    или пользователь хочет узнать цену заказа
    """
    try:
        cost_data = await order_serivce.accounting_service.get_trip_cost(days=days)
        return f"Ориентировочная стоимость поездки за {days} дн. составляет: {cost_data} руб."
    
    except Exception as e:
        raise ToolError(f"Не удалось рассчитать стоимость: {str(e)}")
    
    
@mcp.tool()
async def apply_to_order(order_id: int, email: str):
    """ 
    Откликнуться на заказ от имени водителя.
    Используй этот инструмент, когда водитель просит откликнуться или записаться на конкретный заказ.
    """
    try:
        user = await user_serivce.get_user_by_email(email)
        if not user:
            raise ToolError(f"ошибка: пользователь с email: {email} не найден.")
        
        new_offer = await offer_service.create_offer(user_id=user.id, order_id=order_id)
        return f"Успешно! Вы - {email}, откликнулись на заказ №{order_id}"
    
    except HTTPException as e:
        raise ToolError(f"Не удалось откликнуться: {e.detail}")
    except Exception as e:
        raise ToolError(f"Внутренняя ошибка при создании отклика: {str(e)}")
    

@mcp.tool()
async def get_all_offers(email: str):
    """ 
    Получить список всех откликов водителя по его email.
    Показывает статусы откликов (ожидает, принят, отклонен) и детали заказов.
    """
    try:
        user = await user_serivce.get_user_by_email(email)
        if not user:
            raise ToolError(f"Ошибка: Пользователь с email {email} не найден")
        
        offers = await offer_service.get_my_offers(user_id=user.id, status=None)
        if not offers:
            return f"У водителя с email: {email} пока нет ни одного отклика"

        result = [f"Список откликов для водителя {email}:"]
        for offer in offers:
            order_info = (
                f"- Отклик №{offer.id} на заказ №{offer.order_id}:"
                f"Статус отклика [{offer.status}],"
                f"Транспорт заказа: {offer.order.transport_type}"
            )
            result.append(order_info)
            
        return "\n".join(result)
    
    except HTTPException as e:
        raise ToolError(f"Не удалось получить список откликов: {e.detail}")
    except Exception as e:
        raise ToolError(f"Внутренняя ошибка сервера: {str(e)}")            

if __name__ == "__main__":
    mcp.run()