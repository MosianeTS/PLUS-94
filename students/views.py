from django.shortcuts import render
from django.db.models import Avg
from .models import Candidate
import datetime
import json
from collections import defaultdict
from django.http import JsonResponse
from django.db.models import Max
from django.db.models.functions import TruncMonth
from datetime import datetime


def home(request):    
    return render(request, 'home.html')


def monthly_averages_line_graph_view(request):
    candidates = Candidate.objects.all().values('candidate', 'score', 'scoring_date', 'province')
    candidates_list = list(candidates)
    for candidate in candidates_list:
        candidate['scoring_date'] = candidate['scoring_date'].strftime('%Y-%m-%d')
    return render(request, 'monthly-averages-line-graph.html', {'candidates': json.dumps(candidates_list)})


def monthly_averages_bar_graph_view(request):
    year = request.GET.get('year', '2020')
    province = request.GET.get('province', 'GP')

    candidates = Candidate.objects.filter(
        scoring_date__year=year,
        province=province
    )
    
    data = defaultdict(list)
    for candidate in candidates:
        month = candidate.scoring_date.strftime('%B')
        data[month].append(candidate.score)

    monthly_averages = {month: sum(scores) / len(scores) for month, scores in data.items()}
    
    chart_data = {
        'months': list(monthly_averages.keys()),
        'averages': list(monthly_averages.values()),
    }

    context = {
        'chart_data': json.dumps(chart_data),
        'candidates': candidates,
        'selected_year': year,
        'selected_province': province
    }
    return render(request, 'monthly-averages-bar-graph.html', context)


def yearly_averages_view(request):
    averages = []
    years = [2020, 2021]    

    for year in years:
        candidates = Candidate.objects.filter(scoring_date__year=year)
        if candidates.exists():
            total_score = sum(candidate.score for candidate in candidates)
            average_score = total_score / candidates.count()
        else:
            average_score = 0
        averages.append(average_score)

    chart_data = {
        'years': years,
        'averages': averages
    }

    context = {
        'chart_data': json.dumps(chart_data)
    }
    return render(request, 'yearly-averages-bar-graph.html', context)


def monthly_scores_view(request):
    year = request.GET.get('year', '2020')  
    candidates = Candidate.objects.filter(scoring_date__year=year)
    
    monthly_scores = [0] * 12
    for candidate in candidates:
        month = candidate.scoring_date.month
        monthly_scores[month - 1] += candidate.score

    chart_data = {
        'months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'scores': monthly_scores
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(chart_data)

    context = {
        'chart_data': json.dumps(chart_data),
        'selected_year': year
    }
    return render(request, 'monthly-scores-line-graph.html', context)


def highest_scores_view(request):
    selected_year = request.GET.get('year', 2020)    
    
    candidates = Candidate.objects.filter(scoring_date__year=selected_year)    
    
    highest_scores = candidates.annotate(month=TruncMonth('scoring_date')).values('month').annotate(max_score=Max('score')).order_by('month')
    
    months = [datetime.strftime(record['month'], '%B') for record in highest_scores]
    scores = [record['max_score'] for record in highest_scores]    
   
    highest_candidates = []
    for record in highest_scores:
        highest_candidate = candidates.filter(scoring_date__month=record['month'].month, score=record['max_score']).first()
        if highest_candidate:
            highest_candidates.append(highest_candidate)
    
    chart_data = {
        'months': months,
        'scores': scores
    }    
    context = {
        'selected_year': int(selected_year),
        'chart_data': json.dumps(chart_data),
        'table_data': highest_candidates,
        'years': range(2020, 2022)
    }
    return render(request, 'highest-scores-line-graph.html', context)
