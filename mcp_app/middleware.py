from fastmcp.server.middleware import Middleware, MiddlewareContext
from src.orm.database import async_session_factory

class DatabaseMiddleware(Middleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """ 
        успралвение сессией Бд для всех инcтрументов MCP
        """
        async with async_session_factory() as session:
            try:
                result = await call_next(context)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                raise e
        