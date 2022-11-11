from rest_framework import serializers

                          # for instance BlogPost and BlogPostRus
def ru_or_en(lan, pk, first_lang_obj, second_lan_obj):

    if lan == 'ru':
        try:
            post = first_lang_obj.objects.get(id=pk)
        except first_lang_obj.DoesNotExist:
            raise serializers.ValidationError({'Error': 'There is no such object'})
    elif lan == 'en':
        try:
            post = second_lan_obj.objects.get(id=pk)
        except second_lan_obj.DoesNotExist:
            raise serializers.ValidationError({'Error': 'There is no such object'})
    return post