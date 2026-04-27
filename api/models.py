from django.db import models

class Photographer(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    description = models.TextField()
    image = models.TextField()  # Use TextField to allow high-capacity base64 payloads
    rating = models.FloatField(default=0.0)
    reviews = models.IntegerField(default=0)
    specialty = models.CharField(max_length=255)
    whyChosen = models.TextField()
    mapQuery = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')
    instaUrl = models.TextField(blank=True, null=True)
    portfolio = models.JSONField(default=list)  # Safe for array structures

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'city': self.city,
            'price': self.price,
            'description': self.description,
            'image': self.image,
            'rating': self.rating,
            'reviews': self.reviews,
            'specialty': self.specialty,
            'whyChosen': self.whyChosen,
            'mapQuery': self.mapQuery,
            'status': self.status,
            'instaUrl': self.instaUrl,
            'portfolio': self.portfolio,
        }


class Booking(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    userId = models.CharField(max_length=255)
    clientName = models.CharField(max_length=255)
    clientEmail = models.EmailField(blank=True, null=True)
    clientPhone = models.CharField(max_length=50, blank=True, null=True)
    photographerId = models.CharField(max_length=255)
    photographerName = models.CharField(max_length=255)
    photographerImage = models.TextField(blank=True, null=True)
    photographerCity = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    time = models.CharField(max_length=255, blank=True, null=True)
    eventType = models.CharField(max_length=255, blank=True, null=True)
    locationDetails = models.TextField(blank=True, null=True)
    totalAmount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, default='upcoming')

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'clientName': self.clientName,
            'clientEmail': self.clientEmail,
            'clientPhone': self.clientPhone,
            'photographerId': self.photographerId,
            'photographerName': self.photographerName,
            'photographerImage': self.photographerImage,
            'photographerCity': self.photographerCity,
            'date': self.date,
            'time': self.time,
            'eventType': self.eventType,
            'locationDetails': self.locationDetails,
            'totalAmount': float(self.totalAmount),
            'status': self.status,
        }
