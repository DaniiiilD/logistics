import grpc
from src.api.services.grpc import tariff_pb2, tariff_pb2_grpc
from src.core.config import settings

class AccountingGrpcService:
    def __init__(self):
        self.host = settings.gRPC_HOST
        self.port = settings.gRPC_PORT
        
    async def get_trip_cost(self, days: int):
        async with grpc.aio.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = tariff_pb2_grpc.TariffServiceStub(channel)
            
            request = tariff_pb2.GetDailyPriceRequest(days=days)
            
            try:
                response = await stub.CalculatePrice(request)
                return {
                    'price_per_day' : response.price_per_day,
                    'total_price' : response.total_price
                }
                
            except grpc.RpcError as e:
                print(f'gRPC Error: {e.code()} - {e.details()}')
                raise