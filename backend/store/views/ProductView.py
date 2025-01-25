# Create your views here.
from gc import get_objects

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
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
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = request.FILES.get('image')
        if image:
            image = compress_convert_image(image)
            serializer.validated_data['image'] = image

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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






