from django.urls import path
from .views import monthly_averages_line_graph_view, monthly_averages_bar_graph_view, yearly_averages_view, monthly_scores_view, highest_scores_view, home

urlpatterns = [
    path('', home, name='home'),
    path('monthly-averages-line-graph/', monthly_averages_line_graph_view, name='monthly-averages-line'),
    path('monthly-averages-bar-graph/', monthly_averages_bar_graph_view, name='monthly-averages-bar'),
    path('yearly-averages-bar-graph/', yearly_averages_view, name='yearly-averages'),
    path('monthly-scores-line-graph/', monthly_scores_view, name='monthly-scores'),
    path('highest-scores-line-graph/', highest_scores_view, name='highest-scores'),
]
