from dishka import Provider, provide, Scope
from todo_rpg.application.interactors import GetStatsOverviewInteractor


class StatsProvider(Provider):
    scope = Scope.REQUEST

    get_stats_overview = provide(GetStatsOverviewInteractor)
