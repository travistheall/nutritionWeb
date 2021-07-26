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
        q1 = AddDesc.objects.filter(Q(additional_food_description__icontains=DescSearchContent) | Q(
            food_code__main_food_description__icontains=DescSearchContent)).distinct()
        q2 = MainDesc.objects.filter(main_food_description__icontains=DescSearchContent)
        df_dict = {}
        for i, addQueryItem in enumerate(q1):
            if i == 0:
                df_dict[addQueryItem.food_code.food_code] = {
                    'MainDesc': addQueryItem.food_code.main_food_description,
                    'AddDesc': [addQueryItem.additional_food_description]}
            else:
                if q1[i].food_code.food_code == q1[i - 1].food_code.food_code:
                    df_dict[addQueryItem.food_code.food_code]['AddFoodDesc'].append(
                        addQueryItem.additional_food_description)
                else:
                    df_dict[addQueryItem.food_code.food_code] = {
                        'MainDesc': addQueryItem.food_code.main_food_description,
                        'AddFoodDesc': [addQueryItem.additional_food_description]
                    }

        dict_list = []
        for dict_item in df_dict:
            dict_list.append(dict_item)

        for mainQueryItem in q2:
            if mainQueryItem.food_code not in dict_list:
                df_dict[mainQueryItem.food_code] = {
                    'MainDesc': mainQueryItem.main_food_description,
                    'AddFoodDesc': ''}
                dict_list.append(mainQueryItem.food_code)

        dict_list.sort()
        ordered = OrderedDict((k, df_dict[k]) for k in dict_list)
        context['mainfoods'] = ordered

        sex = form.cleaned_data['sex']
        age = form.cleaned_data['age']
        weight = form.cleaned_data['weight']
        weightUnit = form.cleaned_data["weightUnit"]
        height = form.cleaned_data['height']
        heightUnit = form.cleaned_data["heightUnit"]
        activityLevel = form.cleaned_data["activityLevel"]
        CustomUser.objects.create(user=get_user_model(),
                                  sex=form.cleaned_data['sex'],
                                  age=form.cleaned_data['age'],
                                  weight=form.cleaned_data['weight'],
                                  height=form.cleaned_data['height'],
                                  activityLevel=form.cleaned_data["activityLevel"])