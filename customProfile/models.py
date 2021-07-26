from django.db import models
from django.contrib.auth.models import User
from recurapp.models import MainDesc, Foodweights


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    SEX_CHOICES = [
        (5, "Male"),
        (-161, "Female")
    ]
    sex = models.IntegerField(choices=SEX_CHOICES,
                              default=5)
    age = models.SmallIntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    WEIGHT_UNIT_CHOICES = [
        (2.20462, "Pounds"),
        (1, "Kilograms"),
    ]
    weightUnit = models.FloatField(choices=WEIGHT_UNIT_CHOICES,
                                   default=1)
    height = models.FloatField(blank=True, null=True)
    HEIGHT_UNIT_CHOICES = [
        (2.54, "Inches"),
        (1, "Centimeters"),
    ]
    heightUnit = models.FloatField(choices=HEIGHT_UNIT_CHOICES,
                                   default=1)
    ACTIVITY_LEVEL_CHOICES = [
        (1.2, "Sedentary"),
        (1.375, "Light Activity"),
        (1.55, "Moderately Active"),
        (1.725, "Very Active"),
        (1.9, "Extremely Active"),
    ]
    activityLevel = models.FloatField(choices=ACTIVITY_LEVEL_CHOICES,
                                      default=1.2)

    def get_calories(self):
        return int(((10 * (self.weight / self.weightUnit)) + (6.25 * (self.height * self.heightUnit)) - (
                5 * self.age) + self.sex) * self.activityLevel)

    def __str__(self):
        return f"{self.user.username} Custom Profile"


class UserConsumedFood(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    day = models.DateTimeField(auto_now_add=True)
    MEAL_CHOICES = [
        ("b", "Breakfast"),
        ("l", "Lunch"),
        ("d", "Dinner"),
        ("s", "Snack")
    ]
    meal = models.CharField(choices=MEAL_CHOICES,
                            default='b',
                            max_length=2)
    food = models.ForeignKey(MainDesc, null=True, blank=True, on_delete=models.SET_NULL)
    servingSize = models.ForeignKey(Foodweights, null=True, blank=True, on_delete=models.SET_NULL)
    takenPortion = models.FloatField(default=1.0)
    returnedPortion = models.FloatField(default=0.0)


class UserWeights(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    oldWeights = models.FloatField()
