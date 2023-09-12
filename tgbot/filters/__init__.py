from .admin import AdminFilter, ChatAdminFilter
from .features import register_all_features_filters
from .group import IsSubscribeActiveFilter


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(ChatAdminFilter)
    dp.filters_factory.bind(IsSubscribeActiveFilter)
    register_all_features_filters(dp)
