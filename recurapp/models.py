from django.db import models


class MainDesc(models.Model):
    food_code = models.IntegerField(db_column='Food_code', primary_key=True)
    main_food_description = models.CharField(db_column='Main_food_description', max_length=200)
    fortification_identifier_code = models.CharField(db_column='Fortification_identifier_code', max_length=2, blank=True, null=True)
    wweia_category_code = models.IntegerField(db_column='WWEIA_Category_code')
    wweia_category_description = models.CharField(db_column='WWEIA_Category_description', max_length=80)
    start_date = models.DateTimeField(db_column='Start_date')
    end_date = models.DateTimeField(db_column='End_date')

    def __str__(self):
        return f"{self.food_code}"

    class Meta:
        managed = True
        db_table = 'MainDesc'
        ordering = ['food_code']


class Foodportiondesc(models.Model):
    portion_code = models.IntegerField(primary_key=True, db_column='Portion_code')
    portion_description = models.CharField(db_column='Portion_description', max_length=120)
    start_date = models.DateTimeField(db_column='Start_date')
    end_date = models.DateTimeField(db_column='End_date')

    class Meta:
        managed = True
        db_table = 'foodportiondesc'


class Subcodedesc(models.Model):
    subcode = models.IntegerField(primary_key=True, db_column='Subcode')
    subcode_description = models.CharField(max_length=80, db_column='Subcode_description')
    start_date = models.DateTimeField(db_column='Start_date')
    end_date = models.DateTimeField(db_column='End_date')

    class Meta:
        managed = True
        db_table = 'subcodedesc'


class AddDesc(models.Model):
    food_code = models.ForeignKey(MainDesc, to_field='food_code', db_column='Food_code', related_name='AddDescs', on_delete=models.CASCADE)
    seq_num = models.SmallIntegerField(db_column='Seq_num')
    additional_food_description = models.CharField(db_column='Additional_food_description', max_length=80, blank=True, null=True)
    start_date = models.DateTimeField(db_column='Start_date')
    end_date = models.DateTimeField(db_column='End_date')

    def __int__(self):
        return f"{self.food_code}"

    class Meta:
        managed = True
        db_table = 'AddDesc'


class Ingredients(models.Model):
    food_code = models.ForeignKey(MainDesc, to_field='food_code', db_column='Food_code', related_name='Ingreds', on_delete=models.CASCADE)
    seq_num = models.SmallIntegerField(db_column='Seq_num')
    ingredient_code = models.IntegerField(db_column='Ingredient_code')
    ingredient_description = models.CharField(db_column='Ingredient_description', max_length=240)
    amount = models.DecimalField(db_column='Amount', max_digits=8,  decimal_places=4)
    measure = models.CharField(db_column='Measure', max_length=3, blank=True, null=True)
    portion_code = models.ForeignKey(Foodportiondesc, to_field='portion_code', db_column='Portion_code', on_delete=models.CASCADE)
    path = models.CharField(max_length=100, blank=True, null=True)
    retention_code = models.SmallIntegerField(db_column='Retention_code')
    ingredient_weight = models.DecimalField(db_column='Ingredient_weight', max_digits=8, decimal_places=4)
    start_date = models.DateTimeField(db_column='Start_date')
    end_date = models.DateTimeField(db_column='End_date')

    def __int__(self):
        return f"{self.ingredient_code}"

    class Meta:
        managed = True
        db_table = 'Ingredients'


class SrFoodDes(models.Model):
    ndb_no = models.IntegerField(db_column='NDB_No', primary_key=True)
    fdgrp_cd = models.CharField(db_column='FdGrp_Cd', max_length=4)
    long_desc = models.CharField(db_column='Long_Desc', max_length=200)
    shrt_desc = models.CharField(db_column='Shrt_Desc', max_length=60)
    comname = models.CharField(db_column='ComName', max_length=100, blank=True, null=True)
    manufacname = models.CharField(db_column='ManufacName', max_length=65, blank=True, null=True)
    survey = models.CharField(db_column='Survey', max_length=1, blank=True, null=True)
    ref_desc = models.CharField(db_column='Ref_Desc', max_length=135, blank=True, null=True)
    refuse = models.SmallIntegerField(db_column='Refuse', null=True)
    sciname = models.CharField(db_column='SciName', max_length=65, blank=True, null=True)
    n_factor = models.DecimalField(db_column='N_Factor', max_digits=3, decimal_places=2, blank=True, null=True)
    pro_factor = models.DecimalField(db_column='Pro_Factor', max_digits=3, decimal_places=2, blank=True, null=True)
    fat_factor = models.DecimalField(db_column='Fat_Factor', max_digits=3, decimal_places=2, blank=True, null=True)
    cho_factor = models.DecimalField(db_column='CHO_Factor', max_digits=3, decimal_places=2, blank=True, null=True)

    def __int__(self):
        return f"{self.ndb_no}"

    class Meta:
        managed = True
        db_table = 'SrFoodDes'


class Foodsubcodelinks(models.Model):
    food_code = models.ForeignKey(MainDesc, to_field='food_code', db_column='Food_code', on_delete=models.CASCADE)
    subcode = models.ForeignKey(Subcodedesc, to_field='subcode', db_column='Subcode', related_name='subdescs', on_delete=models.CASCADE)
    start_date = models.DateTimeField(db_column='Start_date', blank=True, null=True)
    end_date = models.DateTimeField(db_column='End_date', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'foodsubcodelinks'


class Foodweights(models.Model):
    food_code = models.ForeignKey(MainDesc, to_field='food_code', db_column='Food_code', related_name='Weights', on_delete=models.CASCADE)
    subcode = models.ForeignKey(Subcodedesc, related_name='subcodedescs', db_column='Subcode', blank=True, null=True, on_delete=models.CASCADE)
    seq_num = models.SmallIntegerField(db_column='Seq_num', blank=True, null=True)
    portion_code = models.ForeignKey(Foodportiondesc, related_name='portiondescs', db_column='Portion_code', on_delete=models.CASCADE)
    portion_weight = models.DecimalField(db_column='Portion_weight', max_digits=6, decimal_places=2, blank=True, null=True)
    url_weight = models.IntegerField(db_column='Url_weight', blank=True, null=True)
    start_date = models.DateTimeField(db_column='Start_date')
    end_date = models.DateTimeField(db_column='End_date')

    def adjust_portion_weight_to_int(self, portion_weight):
        return portion_weight * 100

    class Meta:
        managed = True
        db_table = 'foodweights'


class Nutdesc(models.Model):
    nutrient_code = models.SmallIntegerField(primary_key=True, db_column='Nutrient_code')
    nutrient_description = models.CharField(db_column='Nutrient_description', max_length=45)
    tagname = models.CharField(db_column='Tagname', max_length=15, blank=True, null=True)
    unit = models.CharField(db_column='Unit', max_length=10)
    decimals = models.SmallIntegerField(db_column='Decimals')

    def __str__(self):
        return f"{self.nutrient_description}"

    class Meta:
        managed = True
        db_table = 'nutdesc'


class Fnddsnutval(models.Model):
    food_code = models.ForeignKey(MainDesc, related_name='NutrientValues', on_delete=models.CASCADE, db_column='Food_code')
    nutrient_code = models.ForeignKey(Nutdesc, on_delete=models.CASCADE, related_name='NutrientDescriptions', db_column='Nutrient_code', blank=True, null=True)
    nutrient_value = models.DecimalField(db_column='Nutrient_value', max_digits=8, decimal_places=3)
    start_date = models.DateTimeField(db_column='Start_date')
    end_date = models.DateTimeField(db_column='End_date')

    class Meta:
        managed = True
        db_table = 'fnddsnutval'
