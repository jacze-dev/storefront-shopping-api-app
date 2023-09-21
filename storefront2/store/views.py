from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from .filters import ProductFilter
from .pagination import DefaultPagination
from .models import CartItem, Product,Collection,OrderItem,Review,Cart
from .serializers import AddCartItemSerializer, CartItemSerializaer, ProductSerializers,CollectionSerializer,ReviewSerializer,CartSerializer, UpdateCarItemSerializer


class ProductVewSet(ModelViewSet):
   queryset = Product.objects.all()
   serializer_class = ProductSerializers
   filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
   filterset_class = ProductFilter
   pagination_class = DefaultPagination
   search_fields = ['title','description']
   ordering_fields = ['unit_price','last_updated']

   def get_serializer_context(self):
       return {'request':self.request}
   

   # def get_queryset(self):
   #     queryset = Product.objects.all()
   #     collection_id = self.request.query_params.get('collection_id')
   #     if collection_id is not None:
   #         queryset = queryset.filter(collection_id=collection_id)
   #     return queryset
   

   def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
             return Response({'error:this can not be deleted because it is refferenced to ther items.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

   # def delete(self,request,pk):
   #    product = get_object_or_404(Product, pk=pk)
   #    if product.orderitems.count() > 0:
   #          return Response({'error:this can not be deleted because it is refferenced to ther items.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
   #    product.delete()
   #    return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductsList(ListCreateAPIView):

#    queryset = Product.objects.all()
#    serializer_class = ProductSerializers
#    # def get_queryset(self):
#    #     return Product.objects.select_related('collection').all()
#    # def get_serializer_class(self, *args, **kwargs):
#    #     return ProductSerializers

   

   # def get(self,request):
   #    queryset = Product.objects.select_related('collection').all()
   #    serializer = ProductSerializers(queryset,many=True)
   #    return Response(serializer.data)
   
   # def post(self,request):
   #    serializer = ProductSerializers(data=request.data)
   #    serializer.is_valid(raise_exception=True)
   #    serializer.save()
   #    return Response(serializer.data,status=status.HTTP_201_CREATED)

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#    queryset =  Product.objects.all()
#    serializer_class = ProductSerializers


#    # def get(self,request,id):
#    #    product = get_object_or_404(Product, pk=id)
#    #    serializer = ProductSerializers(product)
#    #    return Response(serializer.data)
#    # def put(self,request):
#    #    product = get_object_or_404(Product, pk=id)
#    #    serialzer = ProductSerializers(instance=product,data=request.data)
#    #    return Response(serialzer.data)
#    def delete(self,request,pk):
#       product = get_object_or_404(Product, pk=pk)
#       if product.orderitems.count() > 0:
#           return Response({'error:this can not be deleted because it is refferenced to ther items.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#       product.delete()
#       return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionViewSet(ModelViewSet):
      queryset = Collection.objects.annotate(products_count = Count('product')).all()
      serializer_class = CollectionSerializer
      def get_serializer_context(self):
         return {'request':self.request}
      def destroy(self, request, *args, **kwargs):
          if Product.objects.filter(collection = kwargs['collection']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
          return super().destroy(request, *args, **kwargs)

      # def delete(self,request,pk):
      #    collection = get_object_or_404(Collection, pk=pk)
      #    if collection.product.count() > 0:
      #       return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
      #    collection.delete()
      #    return Response(status=status.HTTP_204_NO_CONTENT)   
      
# class CollectionList(ListCreateAPIView):
#       queryset = Collection.objects.annotate(products_count = Count('product')).all()
#       serializer_class = CollectionSerializer

#       # def get_queryset(self):
#       #    return  Collection.objects.annotate(products_count = Count('product')).all()
#       # def get_serializer_class(self):
#       #     return CollectionSerializer
#       def get_serializer_context(self):
#           return {'request':self.request}
#       # def get(self,request):
#       #    queryset = Collection.objects.annotate(products_count = Count('product')).all()
#       #    serializer = CollectionSerializer(queryset,many = True)   
#       #    return Response(serializer.data)
#       # def post(self,request,pk):
#       #    serializer = CollectionSerializer(data=request.data)
#       #    serializer.is_valid(raise_exception=True)
#       #    serializer.save()
#       #    return Response(serializer.data,status=status.HTTP_201_CREATED)
      
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#          queryset = Collection.objects.annotate(products_count = Count('product')).all()
#          serializer_class = CollectionSerializer

#          # def get(self,request,pk):
#          #    collection = get_object_or_404(Collection.objects.annotate(products_count = Count('product')),pk=pk)
#          #    serializer = CollectionSerializer(collection)
#          #    return Response(serializer.data)
#          # def post(self,request,pk):
#          #    collection = get_object_or_404(Collection.objects.annotate(products_count = Count('product')),pk=pk)
#          #    serializer = CollectionSerializer(collection,data=request.data)
#          #    serializer.is_valid(raise_exception=True)
#          #    serializer.save()
#          #    return Response(serializer.data)
#          def delete(self,request,pk):
#             collection = get_object_or_404(Collection, pk=pk)
#             if collection.product.count() > 0:
#                return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#             collection.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)   



# @api_view(['GET','POSt'])
# def product_list(request):
#    if request.method == 'GET':
#       queryset = Product.objects.select_related('collection').all()
#       serializer = ProductSerializers(queryset,many = True,context={'request':request})
#       return Response(serializer.data)
#    elif request.method == 'POST':
#        serializer = ProductSerializers(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(serializer.data,status=status.HTTP_201_CREATED)


# @api_view(['GET','PUT','DELETE'])
# def product_detail(request,id):
#    product = get_object_or_404(Product, pk=id)
#    if request.method == 'GET':
#       serializer = ProductSerializers(product)
#       return Response(serializer.data)
#    elif request.method == 'PUT':
#       serializer = ProductSerializers(instance=product,data=request.data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response(serializer.data)
#    if request.method == 'DELETE':
#       if product.orderitems.count() > 0:
#          return Response({'error:this can not be deleted because it is refferenced to ther items.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#       product.delete()
#       return Response(status=status.HTTP_204_NO_CONTENT)
   
# @api_view(['GET','POST'])
# def collection_list(request):
#       if request.method == 'GET':
#          queryset = Collection.objects.annotate(products_count = Count('product')).all()
#          serializer = CollectionSerializer(queryset,many = True)   
#          return Response(serializer.data)
#       elif request.method == 'POST':
#          serializer = CollectionSerializer(data=request.data)
#          serializer.is_valid(raise_exception=True)
#          serializer.save()
#          return Response(serializer.data,status=status.HTTP_201_CREATED)
      
# @api_view(['GET','PUT','DELETE'])
# def collection_detail(request,pk):
#    collection = get_object_or_404(Collection.objects.annotate(products_count = Count('product')),pk=pk)
#    if request.method == 'GET':
#       serializer = CollectionSerializer(collection)
#       return Response(serializer.data)
#    elif request.method == 'PUT':
#       serializer = CollectionSerializer(collection,data=request.data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response(serializer.data)
#    elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
         

      

class ReviewViewSet(ModelViewSet):
 
   serializer_class = ReviewSerializer

   def get_queryset(self):
       return Review.objects.filter(product_id = self.kwargs['product_pk'])
   
   def get_serializer_context(self):
       return {'product_id':self.kwargs['product_pk']}

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CartItemViewSet(ModelViewSet):

    http_method_names = ['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCarItemSerializer
        return CartItemSerializaer

    def get_queryset(self):
        return CartItem.objects\
                .filter(cart_id = self.kwargs['cart_pk'])\
                .select_related('product')
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


