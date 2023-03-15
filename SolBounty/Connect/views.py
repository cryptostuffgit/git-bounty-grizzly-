from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import  Response
from rest_framework.views import APIView
from .utils import get_tokens_for_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer
from django.conf import settings
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from requests.exceptions import HTTPError
from social_django.utils import psa
import requests
from django.conf import settings
from .utils import get_user_repositories, get_open_issues, create_issue, apply_issue
from rest_framework.authentication import TokenAuthentication
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json 
from .models import GitWebhook, GitIssue, BountyPayment, BountyHunter
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from .solana import payout_bounty
import asyncio
from asgiref.sync import async_to_sync, sync_to_async

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      
class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

      
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


      
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True) #Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """
    access_code = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )

@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):
    """
    Exchange an OAuth2 access token for one for this site.
    This simply defers the entire OAuth2 process to the front end.
    The front end becomes responsible for handling the entirety of the
    OAuth2 process; we just step in at the end and use the access token
    to populate some user identity.
    The URL at which this view lives must include a backend field, like:
        url(API_ROOT + r'social/(?P<backend>[^/]+)/$', exchange_token),
    Using that example, you could call this endpoint using i.e.
        POST API_ROOT + 'social/facebook/'
        POST API_ROOT + 'social/google-oauth2/'
    Note that those endpoint examples are verbatim according to the
    PSA backends which we configured in settings.py. If you wish to enable
    other social authentication backends, they'll get their own endpoints
    automatically according to PSA.
    ## Request format
    Requests must include the following field
    - `access_token`: The OAuth2 access token provided by the provider
    """
    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # set up non-field errors key
        # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'

        try:
            # this line, plus the psa decorator above, are all that's necessary to
            # get and populate a user object for any properly enabled/configured backend
            # which python-social-auth can handle.
            url = 'https://github.com/login/oauth/access_token'
            body = {
                'client_id': settings.SOCIAL_AUTH_GITHUB_KEY,
                'client_secret': settings.SOCIAL_AUTH_GITHUB_SECRET,
                'code': request.data['access_code']
            }
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            response = requests.post(url, json=body, headers=headers)
            data = response.json()
            print(data)
            user = request.backend.do_auth(data['access_token'])
        except HTTPError as e:
            # An HTTPError bubbled up from the request to the social auth provider.
            # This happens, at least in Google's case, every time you send a malformed
            # or incorrect access key.
            return Response(
                {'errors': {
                    'token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            if user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                # user is not active; at some point they deleted their account,
                # or were banned by a superuser. They can't just log in with their
                # normal credentials anymore, so they can't log in with social
                # credentials either.
                return Response(
                    {'errors': {nfe: 'This user account is inactive'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Unfortunately, PSA swallows any information the backend provider
            # generated as to why specifically the authentication failed;
            # this makes it tough to debug except by examining the server logs.
            return Response(
                {'errors': {nfe: "Authentication Failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

class RSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """
    access_code = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )

@api_view(http_method_names=['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def link_repository(request):
    repositories = get_user_repositories(request.user)
    if request.method == 'GET':
        print(repositories)
        return Response(repositories)
    if request.method == 'POST':
        pass

@api_view(http_method_names=['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_issues(request):
    issues = get_open_issues(request.user,request.GET['repository'])
    if request.method == 'GET':
        print(issues)
        return Response({
            'issues': issues
        })
    if request.method == 'POST':
        pass

@api_view(http_method_names=['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes((JSONParser,)) 
def create_issue_api(request):
    if request.method == 'POST':
        issue = create_issue(request.user,request.data)
        return Response(issue)

@api_view(http_method_names=['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes((JSONParser,)) 
def apply_issue_api(request):
    if request.method == 'POST':
        issue = apply_issue(request.user,request.data)
        return Response({'wallet': issue.wallet})

@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_user(request):
    if request.method == 'GET':
        return Response({'username':request.user.username})

@csrf_exempt
def github_webhook(request):
    print("wehook")
    # signature = request.headers['X-Hub-Signature']
    # TO DO : Verifiy this against our secret code

    json_data = json.loads(request.body)

    try:
        issue = GitIssue.objects.get(github_id=json_data['ref'].split('-')[-1])
        user = User.objects.get(username=json_data['commits'][0]['author']['name'])
        print(issue,"Solved by",user)
        BountyPayment.objects.create(
            user=user,
            issue=issue
        )
        print(user, issue)
        bounty_hunter = BountyHunter.objects.get(user=user, issue=issue)
        print(bounty_hunter.wallet, issue.pda, issue.github_id)
        payout_bounty_sync = async_to_sync(payout_bounty)
        result = payout_bounty_sync(bounty_hunter.wallet, issue.pda, issue.github_id)
        issue.is_active = False
        issue.save()
    except:
        pass

    try:
        GitWebhook.objects.create(
            data=json_data
        )
    except Exception as e:
        print(e)

    return JsonResponse({
        'message':'success'
    })

@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_bounties(request):
    if request.method == 'GET':
        bounties = list()
        for issue in GitIssue.objects.filter(is_active=True):
            bounties.append({
                "title": str(issue.title),
                "body": str(issue.body),
                "lamports": str(issue.lamports),
                "minimum_date": str(issue.minimum_date),
                "branch_name": str(issue.branch_name),
                "repository": str(issue.repository.name),
                "user": str(issue.repository.user),
                "issue_id":str(issue.github_id),
                "pda": issue.pda_link
            })
        return Response(bounties)