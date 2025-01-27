# Create your views here.
import json
from gc import get_objects

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from store.models.ProductModel import Product
from store.serializers.ProductSerializer import ProductSerializer

def compress_convert_image(image):
    img = Image.open(image)
    img = img.convert("RGB")
    img_io = BytesIO()
    img.save(img_io, format="WEBP", quality=80)
    img_io.seek(0)
    new_image_name = f"{image.name.rsplit('.', 1)[0]}.webp"
    return InMemoryUploadedFile(
        img_io, None, new_image_name, 'image/webp', img_io.tell(), None
    )

class ProductListView(APIView):

    def get(self, request):
        items_per_page = request.query_params.get("itemsPerPage", 10)
        page = request.query_params.get("page", 1)
        search = request.query_params.get("search", "")
        try:
            items_per_page = int(items_per_page)
        except ValueError:
            raise ValidationError("itemsPerPage must be an integer.")

        products = Product.objects.all()

        if search:
            products = products.filter(name__icontains=search)

        sort_by = request.query_params.get("sortBy", "[]")
        try:
            sort_by = json.loads(sort_by)

        except json.JSONDecodeError:
            sort_by = []

        for sort_item in sort_by:
            field = sort_item.get("key")
            order = sort_item.get("order", "asc")
            if field in ["id", "price", "name"]:
                if order == "desc":
                    field = f"-{field}"
                products = products.order_by(field)

        paginator = PageNumberPagination()
        paginator.page_size = items_per_page
        paginated_products = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = request.FILES.get('image')
        if image:
            image = compress_convert_image(image)
            serializer.validated_data['image'] = image

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        product_ids = request.data.get('product_ids', [])

        if not product_ids:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            products_to_delete = Product.objects.filter(id__in=product_ids)
            if len(products_to_delete) != len(product_ids):
                invalid_ids = set(product_ids) - set(products_to_delete.values_list('id', flat=True))
                return Response(
                    {'error': f'IDs inválidos: {invalid_ids}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            deleted_count, _ = products_to_delete.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductDetailView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
