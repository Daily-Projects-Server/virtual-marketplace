from django.shortcuts import render
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import *
from .serializers import *


@extend_schema_view(
    list=extend_schema(
        summary="List all transactions",
        description="Returns a list of all transactions in the system.",
        responses={200: TransactionSerializer(many=True)},
        tags=["Transactions"]
    ),
    create=extend_schema(
        summary="Create a new transaction",
        description="Create a new transaction(order)",
        request=TransactionSerializer,
        responses={201: TransactionSerializer},
        tags=["Transactions"]
    ),
    retrieve=extend_schema(
        summary="Get a transaction by ID",
        description="Retrieve a transaction by its ID.",
        responses={200: TransactionSerializer},
        tags=["Transactions"]
    ),
    update=extend_schema(
        summary="Update a transaction",
        description="Update a transaction by its ID.",
        request=TransactionSerializer,
        responses={200: TransactionSerializer},
        tags=["Transactions"]
    ),
    partial_update=extend_schema(
        summary="Partially update a transaction",
        description="Partially update a transaction by its ID.",
        request=TransactionSerializer,
        responses={200: TransactionSerializer},
        tags=["Transactions"]
    ),
    destroy=extend_schema(
        summary="Delete a transaction",
        description="Delete a transaction by its ID.",
        responses={204: None},
        tags=["Transactions"]
    )
)
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all carts",
        description="Returns a list of all carts in the system.",
        responses={200: CartSerializer(many=True)},
        tags=["Carts"]
    ),
    create=extend_schema(
        summary="Create a new cart",
        description="Create a new cart for a user.",
        request=CartSerializer,
        responses={201: CartSerializer},
        tags=["Carts"]
    ),
    retrieve=extend_schema(
        summary="Get a cart by ID",
        description="Retrieve a cart by its ID.",
        responses={200: CartSerializer},
        tags=["Carts"]
    ),
    update=extend_schema(
        summary="Update a cart",
        description="Update a cart by its ID.",
        request=CartSerializer,
        responses={200: CartSerializer},
        tags=["Carts"]
    ),
    partial_update=extend_schema(
        summary="Partially update a cart",
        description="Partially update a cart by its ID.",
        request=CartSerializer,
        responses={200: CartSerializer},
        tags=["Carts"]
    ),
    destroy=extend_schema(
        summary="Delete a cart",
        description="Delete a cart by its ID.",
        responses={204: None},
        tags=["Carts"]
    )
)
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all cart items",
        description="Returns a list of all cart items in the system.",
        responses={200: CartItemSerializer(many=True)},
        tags=["Cart Items"]
    ),
    create=extend_schema(
        summary="Create a new cart item",
        description="Create a new cart item for a cart.",
        request=CartItemSerializer,
        responses={201: CartItemSerializer},
        tags=["Cart Items"]
    ),
    retrieve=extend_schema(
        summary="Get a cart item by ID",
        description="Retrieve a cart item by its ID.",
        responses={200: CartItemSerializer},
        tags=["Cart Items"]
    ),
    update=extend_schema(
        summary="Update a cart item",
        description="Update a cart item by its ID.",
        request=CartItemSerializer,
        responses={200: CartItemSerializer},
        tags=["Cart Items"]
    ),
    partial_update=extend_schema(
        summary="Partially update a cart item",
        description="Partially update a cart item by its ID.",
        request=CartItemSerializer,
        responses={200: CartItemSerializer},
        tags=["Cart Items"]
    ),
    destroy=extend_schema(
        summary="Delete a cart item",
        description="Delete a cart item by its ID.",
        responses={204: None},
        tags=["Cart Items"]
    )
)
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all coupons",
        description="Returns a list of all coupons in the system.",
        responses={200: CouponSerializer(many=True)},
        tags=["Coupons"]
    ),
    create=extend_schema(   
        summary="Create a new coupon",
        description="Create a new coupon.",
        request=CouponSerializer,
        responses={201: CouponSerializer},
        tags=["Coupons"]
    ),
    retrieve=extend_schema(
        summary="Get a coupon by ID",
        description="Retrieve a coupon by its ID.",
        responses={200: CouponSerializer},
        tags=["Coupons"]
    ),
    update=extend_schema(
        summary="Update a coupon",
        description="Update a coupon by its ID.",
        request=CouponSerializer,
        responses={200: CouponSerializer},
        tags=["Coupons"]
    ),
    partial_update=extend_schema(
        summary="Partially update a coupon",
        description="Partially update a coupon by its ID.",
        request=CouponSerializer,
        responses={200: CouponSerializer},
        tags=["Coupons"]
    ),
    destroy=extend_schema(
        summary="Delete a coupon",
        description="Delete a coupon by its ID.",
        responses={204: None},
        tags=["Coupons"]
    )
)
class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
