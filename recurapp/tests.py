from django.test import TestCase

# Create your tests here.
foodweight = Foodweights.objects.all()
len(foodweight)
for weight in foodweight:
    to_int = weight.portion_weight * 100
    weight.update(url_weight=to_int, )