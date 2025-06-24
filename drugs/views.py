from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from drugs.models import Drugs
from django.db.models.functions import Concat, Lower
from django.db.models import Value,TextField

# Create your views here.
def search_drugs(req):
    q = req.GET.get('q', "").strip().lower()
    if not q :
        return JsonResponse([],safe=False)
    # exact_matches = Drugs.objects.filter(
    #     Q(generic__iexact = q)|
    #     Q(name__istartswith=q) |
    #     Q(generic__icontains=q)|
    #     Q(dosage__icontains = q) |
    #     Q(generic__icontains=q)|
    #     Q(name__iexact = q)
    # ).values()
    # query_result = list(exact_matches)
    
    if  q: 
        # print('nothing')
        drugs = Drugs.objects.annotate(
            combined=Concat(
                'name',
                Value(' '),
                'dosage',
                Value(' '),
                'generic',
                output_field=TextField()
            )
        )
        keywords = q.split(" ")
        for k in keywords:
            drugs = drugs.filter(combined__icontains = k).values()
        query_result = list(drugs)
    result = query_result[:5]
    return JsonResponse(result, safe=False)