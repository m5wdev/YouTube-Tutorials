from rest_framework import serializers

from apps.company.models.company import Company
# from apps.company.models.point import Point
from apps.company.models.brand import Brand
from apps.company.models.category import Category

from apps.company.serializers import brand, point, category, company_image, often_repair
# from apps.services.serializers import CategoryServicesSerializer
# from apps.cities.serializers.city import CitySerializer

from classes.utils.transliterate import transliterate


def constructor_slug(name):
    slug = ''
    for el in name:
        slug += transliterate(el) + '-'
        slug = slug[:-1].lower()
    if Company.objects.filter(slug=slug).first():
        return constructor_slug(name+'c')
    else:
        return slug


class CompanySerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="get_city_name", read_only=True)
    author = serializers.CharField(source="get_author_name", read_only=True, required=False)
    brands = serializers.SerializerMethodField(source="get_brands", read_only=True)
    subcategories = serializers.SerializerMethodField(source="get_subcategories", read_only=True)
    brands_list_id = serializers.ListField(child=serializers.DictField(), write_only=True)
    categories_list_id = serializers.ListField(child=serializers.DictField(), write_only=True)
    author_id = serializers.IntegerField(min_value=1, max_value=100000, write_only=True, required=False)
    points = point.PointSerializer(many=True, read_only=True)
    images = company_image.CompanyImageSerializer(many=True, read_only=True)

    # categoryservice = CategoryServicesSerializer(many=True, read_only=True)
    often_repair = often_repair.OftenRepairSerializer(many=True, read_only=True)

    def create(self, validated_data):
        author_id = validated_data.pop('author_id')
        brands_list_id = validated_data.pop('brands_list_id')
        categories_list_id = validated_data.pop('categories_list_id')
        slug = constructor_slug(validated_data['name'])
        company = Company.objects.create(**validated_data, author_id=author_id, slug=slug)
        for item in brands_list_id:
            brand = Brand.objects.get(id=item['id'])
            company.brands.add(brand)
        for item in categories_list_id:
            category = Category.objects.get(id=item['id'])
            company.categories.add(category)
        company.save()
        return company

    def update(self, instanse, validated_data):
        if validated_data.get('brands_list_id'):
            brands_list_id = validated_data.pop('brands_list_id')
            categories_list_id = validated_data.pop('categories_list_id')
            if validated_data.get('points'):
                points = validated_data.pop('points')
            instanse.brands.clear()
            instanse.categories.clear()
            for item in brands_list_id:
                brand = Brand.objects.get(id=item['id'])
                instanse.brands.add(brand)
            for item in categories_list_id:
                category = Category.objects.get(id=item['id'])
                instanse.categories.add(category)
            for key, value in validated_data.items():
                setattr(instanse, key, value)
            instanse.save()
            return instanse
        else:
            return super().update(instanse, validated_data)

    def get_subcategories(self, obj):
        subcategory = [category['name'] for category in list(obj.categories.all().values())]
        return subcategory

    def get_brands(self, obj):
        brands = [{'name': brand['name'], 'slug': brand['slug']} for brand in list(obj.brands.all().values())]
        return brands

    class Meta:
        model = Company
        # fields = '__all__'
        exclude = ('categories',)


class CompanySearchSerializer(CompanySerializer):
    categories = category.CategorySerializer(many=True)
    class Meta:
        model = Company
        fields = ('id', 'name','categories', 'slug', 'brands', 'subcategories',)


class CompanyUserSerializer(CompanySerializer):
    points = point.PointUserSerializer(many=True, read_only=True)

    def get_subcategories(self, obj):
        subcategory = [{'id': category['id'], 'name': category['name']} for category in list(obj.categories.all().values())]
        return subcategory

    def get_brands(self, obj):
        brands = [{'id': brand['id'], 'name': brand['name'], 'slug': brand['slug']} for brand in list(obj.brands.all().values())]
        return brands
