from collections import OrderedDict
from logging import getLogger

from rest_framework import status, filters, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes

from launcher_service.pagination import ResultsSetPagination
from launcher_service.authentication import AdminAuthentication
from launcher_service.serializers import *
from launcher_service.models import Currency

logger = getLogger('django')


@api_view(['GET'])
@permission_classes([AllowAny, ])
def root(request, format=None):
    return Response(
        [
            {'Public': OrderedDict([
                ('Activate', reverse('launcher_service:activate',
                    request=request,
                    format=format)),
                ('Deactivate', reverse('launcher_service:deactivate',
                    request=request,
                    format=format))
            ])},
            {'Admins': OrderedDict([
                ('Company', reverse('launcher_service:admin-company',
                    request=request,
                    format=format)),
                ('Currencies', reverse('launcher_service:admin-currencies',
                    request=request,
                    format=format))
            ])},
        ])


class ListModelMixin(object):
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': 'success', 'data': serializer.data})


class ListAPIView(ListModelMixin,
                  GenericAPIView):
    """
    Concrete view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ActivateView(GenericAPIView):
    allowed_methods = ('POST',)
    permission_classes = (AllowAny, )
    serializer_class = ActivateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'status': 'success', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )


class DeactivateView(GenericAPIView):
    allowed_methods = ('POST',)
    permission_classes = (AllowAny, )
    serializer_class = DeactivateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response({'status': 'success'})


class JoinView(GenericAPIView):
    allowed_methods = ('POST',)
    permission_classes = (AllowAny, )
    serializer_class = JoinSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'status': 'success', 'data': serializer.data},
            status=status.HTTP_201_CREATED)


class AdminCompanyView(GenericAPIView):
    allowed_methods = ('GET', 'PATCH',)
    serializer_class = AdminCompanySerializer
    authentication_classes = (AdminAuthentication,)

    def get(self, request, *args, **kwargs):
        company = request.user.company
        serializer = self.get_serializer(company)
        return Response({'status': 'success', 'data': serializer.data})


class AdminCurrencyListView(ListAPIView):
    allowed_methods = ('GET',)
    pagination_class = ResultsSetPagination
    serializer_class = CurrencySerializer
    authentication_classes = (AdminAuthentication,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('code',)

    def get_queryset(self):
        company = self.request.user.company
        return Currency.objects.filter(company=company)


class AdminCurrencyView(GenericAPIView):
    allowed_methods = ('GET',)
    serializer_class = CurrencySerializer
    authentication_classes = (AdminAuthentication,)

    def get(self, request, *args, **kwargs):
        company = request.user.company
        code = kwargs['code']

        try:
            currency = Currency.objects.get(company=company, code__iexact=code)
        except Currency.DoesNotExist:
            raise exceptions.NotFound()

        serializer = self.get_serializer(currency)
        return Response({'status': 'success', 'data': serializer.data})


class AdminCampaignView(GenericAPIView):
    allowed_methods = ('GET', 'POST',)
    authentication_classes = (AdminAuthentication,)
    serializer_class = CampaignSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'status': 'success', 'data': serializer.data},
            status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):

        try:
            currency = Campaign.objects.filter()
        except Campaign.DoesNotExist:
            raise exceptions.NotFound()

        serializer = self.get_serializer(currency)
        return Response({'status': 'success', 'data': serializer.data})
