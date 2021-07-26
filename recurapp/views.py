from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from customProfile.forms import CustomUserForm, CustomConsumptionForm
from .models import *
from decimal import Decimal
from decimal import Decimal, getcontext
from django.db.models import Q
from collections import OrderedDict
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from recurapp.serializers import UserSerializer, GroupSerializer, FoodSerializer
from django.contrib.auth import get_user_model
from customProfile.models import CustomUser
from django.contrib import messages


ONEPLACE = Decimal(10) ** -1

def is_valid_queryparam(param):
    return param != 0 and param is not None


def home(request):
    context = {'home': 'home'}
    return render(request, 'home.html', context)


def profile(request):
    context = {
        "profile": "profile",
    }
    return render(request, 'account/profile.html', context)


@login_required(redirect_field_name='home')
def create_meal(request):
    context = {'create_meal': "create_meal"}
    user = request.user
    instance = CustomUser.objects.get(user=user)
    form = CustomConsumptionForm(request.POST or None, instance=instance)
    context["form"] = form
    if form.is_valid():
        form.save()
        messages.success(request, "You successfully created a meal")
        return render(request, 'calorieCreate.html', context)
    else:
        context["error"] = 'The form was not updated successfully.'
    return render(request, 'create_meal.html', context)


@login_required(redirect_field_name='home')
def calorieDisplay(request):
    context = {
        "user_calories": "user_calories",
    }
    user = request.user
    context['user'] = user
    customUser = CustomUser.objects.get(user=user)
    context['customUser'] = customUser
    calories = customUser.get_calories()
    calories = int(calories)
    context['calories'] = calories
    return render(request, 'calorie.html', context)


@login_required
def calorieCreate(request):
    context = {"user_calories": "user_calories"}
    user = request.user
    instance = CustomUser.objects.get(user=user)
    form = CustomUserForm(request.POST or None, instance=instance)
    context["form"] = form
    if form.is_valid():
        form.save()
        messages.success(request, "You successfully updated the your calories")
        return redirect('/calorieDisplay/')
    else:
        context["error"] = 'The form was not updated successfully.'

    return render(request, 'calorieCreate.html', context)


def desc_search(request):
    DescSearchContent = request.GET.get('FoodDesc')
    context = {
        "nutsearch": "nutsearch",
    }
    if is_valid_queryparam(DescSearchContent):
        if DescSearchContent.count(' ') >= 1:
            foodDescWordList = DescSearchContent.split(' ')
            querySetList = []
            for i, searchedWord in enumerate(foodDescWordList):
                if i == 0:
                    querySetList.append(
                        MainDesc.objects.filter(main_food_description__icontains=searchedWord).prefetch_related(
                            'AddDescs').all())
                if i > 0:
                    querySetList.append(querySetList[0].filter(main_food_description__icontains=searchedWord))
                    querySetList.remove(querySetList[0])
                context["mainfood"] = querySetList[0]
        else:
            context["mainfood"] = MainDesc.objects.filter(
                main_food_description__icontains=DescSearchContent).prefetch_related('AddDescs', 'Weights').all()

    return render(request, 'desc_search.html', context)


def nutrient_search(request, food_code):
    context = {}
    context["nutsearch"] = "nutsearch"
    DescSearchContent = request.GET.get('FoodDesc')
    if is_valid_queryparam(DescSearchContent):
        if DescSearchContent.count(' ') >= 1:
            foodDescWordList = DescSearchContent.split(' ')
            querySetList = []
            for i, searchedWord in enumerate(foodDescWordList):
                if i == 0:
                    querySetList.append(
                        MainDesc.objects.filter(main_food_description__icontains=searchedWord).prefetch_related(
                            'AddDescs').all())
                if i > 0:
                    querySetList.append(querySetList[0].filter(main_food_description__icontains=searchedWord))
                    querySetList.remove(querySetList[0])
                context["mainfood"] = querySetList[0]
        else:
            context["mainfood"] = MainDesc.objects.filter(
                main_food_description__icontains=DescSearchContent).prefetch_related('AddDescs', 'Weights').all()
    context["main"] = MainDesc.objects.filter(food_code=food_code).prefetch_related('NutrientValues', 'Weights').all()[0]
    context["mainNutVal"] = context["main"].NutrientValues.all()
    user = request.user
    customUser = CustomUser.objects.get(user=user)
    context['customUser'] = customUser
    calories = customUser.get_calories()
    context['calories'] = calories
    context['totalFat'] = Decimal((calories * 0.288)/9).quantize(ONEPLACE)
    for nutrient in context["mainNutVal"]:
        tagname = nutrient.nutrient_code.tagname
        value = nutrient.nutrient_value
        context[tagname] = {
            "value": value,
            "tagname": tagname,
        }

    context["FATTotalCal"] = f'{context["FAT"]["value"] * 9}'
    context["FATpercentDaily"] = f'{int(((context["FAT"]["value"] * 9)/calories) * 100)}%'
    context["FASATpercentDaily"] = f'{int(((context["FASAT"]["value"] * 9)/calories) * 100)}%'
    return render(request, 'searchWithFacts.html', context)


def ndb_search(request, food_code):
    context = {
        "nutsearch": "nutsearch",
    }
    # Raw SQL Query that creates a list of all of the ingredients into paths
    ingred = Ingredients.objects.raw(
        """
            WITH RECURSIVE ingred_paths (id, Food_code, Seq_num, Ingredient_code, Ingredient_description, path) AS
            (
              SELECT id, Food_code, Seq_num, Ingredient_code, Ingredient_description, CAST(Ingredient_code AS CHAR(200))
                FROM ingredients
              UNION ALL
              SELECT i.id, i.Food_code, i.Seq_num, i.Ingredient_code, i.Ingredient_description, CONCAT(ip.path, ',', i.Ingredient_code)
                FROM ingred_paths AS ip JOIN ingredients AS i
                  ON i.Ingredient_code = ip.Food_code
            )
            SELECT * FROM ingred_paths WHERE Food_code = %s ORDER BY path;
        """, [food_code]
    )
    # configuring lists to quickly sort through the SQL
    IngredientFoodCodes = []
    IngredientSRCodes = []
    ingredQList = []
    # configuring lists to deposit queries
    FoodCodeObjects = []
    SRCodeObjects = []

    for firstIngred in ingred:
        if firstIngred.path.count(',') > 0:
            endCode = firstIngred.path[:firstIngred.path.index(',')]
        else:
            endCode = firstIngred.path
        # if it's a SR code  place it in the correct lists and search the model
        if int(endCode) < 907028:
            if endCode not in IngredientSRCodes:
                IngredientSRCodes.append(endCode)
                SRCodeObjects.append(SrFoodDes.objects.get(ndb_no=endCode))
        # if it's a Food code  place it in the correct lists and search the model
        elif int(endCode) > 999328:
            if endCode not in IngredientFoodCodes:
                IngredientFoodCodes.append(endCode)
                FoodCodeObjects.append(MainDesc.objects.get(food_code=endCode))
        # if it's the weird one that I don't know what to do put it in here
        else:
            if endCode not in ingredQList:
                ingredQList.append(endCode)

    if FoodCodeObjects:
        context["Food_codes"] = FoodCodeObjects
    if SRCodeObjects:
        context["SR_codes"] = SRCodeObjects
    if ingredQList:
        context["Q_codes"] = ingredQList
    return render(request, 'ndb_search.html', context)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserList(generics.ListCreateAPIView):
    queryset = MainDesc.objects.all()
    serializer_class = FoodSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
