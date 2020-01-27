from services.BanksService import BanksService
from services.providers.CursMdService import CursMdService


def from_url():
    banks_service = BanksService(
        CursMdService()
    )
    banks_service.init()


from_url()
