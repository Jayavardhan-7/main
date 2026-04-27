import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Photographer, Booking

@csrf_exempt
def handle_photographers(request):
    if request.method == 'GET':
        photographers = [p.to_dict() for p in Photographer.objects.all()]
        return JsonResponse(photographers, safe=False)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Support array for bulk initial seeding
            if isinstance(data, list):
                for p in data:
                    Photographer.objects.update_or_create(id=p.get('id'), defaults=p)
                return JsonResponse([p.to_dict() for p in Photographer.objects.all()], safe=False)
                
            p = Photographer.objects.create(**data)
            return JsonResponse(p.to_dict(), status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def handle_photographer_detail(request, pk):
    try:
        p = Photographer.objects.get(pk=pk)
    except Photographer.DoesNotExist:
        return JsonResponse({'error': 'Photographer not found'}, status=404)
        
    if request.method == 'GET':
        return JsonResponse(p.to_dict())
        
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                if hasattr(p, key):
                    setattr(p, key, value)
            p.save()
            return JsonResponse(p.to_dict())
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    if request.method == 'DELETE':
        p.delete()
        return JsonResponse({'success': True})

@csrf_exempt
def handle_bookings(request):
    if request.method == 'GET':
        bookings = [b.to_dict() for b in Booking.objects.all()]
        return JsonResponse(bookings, safe=False)
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if isinstance(data, list):
                for b in data:
                    Booking.objects.update_or_create(id=b.get('id'), defaults=b)
                return JsonResponse([b.to_dict() for b in Booking.objects.all()], safe=False)
                
            b = Booking.objects.create(**data)
            return JsonResponse(b.to_dict(), status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def handle_booking_detail(request, pk):
    try:
        b = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)
        
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                if hasattr(b, key):
                    setattr(b, key, value)
            b.save()
            return JsonResponse(b.to_dict())
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
