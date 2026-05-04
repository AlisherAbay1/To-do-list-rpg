from dishka import Provider, provide, Scope
from src.app.application.interactors import GetStatsOverviewInteractor

class StatsProvider(Provider):
    scope = Scope.REQUEST

    get_stats_overview = provide(GetStatsOverviewInteractor)