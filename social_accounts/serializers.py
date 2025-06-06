from rest_framework import serializers
from .utils import Google, register_social_user
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .models import GitHubUser
import requests
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length=6)

    def validate_access_token(self, access_token):
        try:
            # Log the token for debugging (remove in production)
            logger.debug(f"Processing Google sign-in with token: {access_token[:10]}...")
            
            # Validate the Google token
            google_user_data = Google.validate(access_token)
            
            # Extract user data with fallbacks
            email = google_user_data.get('email')
            if not email:
                raise AuthenticationFailed('Email not provided by Google')
                
            first_name = google_user_data.get('given_name', '')
            last_name = google_user_data.get('family_name', '')
            
            # Log successful data extraction (remove in production)
            logger.debug(f"Successfully extracted user data for email: {email}")
            
            # Register or login the user
            return register_social_user('google', email, first_name, last_name)
            
        except AuthenticationFailed as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error during Google sign-in: {str(e)}")
            raise AuthenticationFailed('Google authentication failed')

class GitHubSignInSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, code):
        # Exchange code for access token
        token_url = 'https://github.com/login/oauth/access_token'
        data = {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'code': code
        }
        headers = {'Accept': 'application/json'}
        
        response = requests.post(token_url, data=data, headers=headers)
        if response.status_code != 200:
            raise serializers.ValidationError('Failed to get access token from GitHub')
        
        access_token = response.json().get('access_token')
        if not access_token:
            raise serializers.ValidationError('No access token received from GitHub')

        # Get user info from GitHub
        user_url = 'https://api.github.com/user'
        headers = {'Authorization': f'token {access_token}'}
        response = requests.get(user_url, headers=headers)
        
        if response.status_code != 200:
            raise serializers.ValidationError('Failed to get user info from GitHub')
        
        user_data = response.json()
        
        # Get user's email from GitHub
        email = user_data.get('email')
        if not email:
            # If email is not public, try to get it from GitHub API
            email_url = 'https://api.github.com/user/emails'
            email_response = requests.get(email_url, headers=headers)
            if email_response.status_code == 200:
                emails = email_response.json()
                primary_email = next((e['email'] for e in emails if e['primary']), None)
                email = primary_email or f"{user_data['login']}@github.com"
            else:
                email = f"{user_data['login']}@github.com"

        try:
            # First try to find an existing GitHub user
            github_user = GitHubUser.objects.get(github_id=user_data['id'])
            user = github_user.user
            github_user.github_access_token = access_token
            github_user.save()
        except GitHubUser.DoesNotExist:
            try:
                # Try to find a user with the same email
                user = User.objects.get(email=email)
                # If user exists but doesn't have a GitHub account, create one
                if not hasattr(user, 'githubuser'):
                    GitHubUser.objects.create(
                        user=user,
                        github_id=user_data['id'],
                        github_login=user_data['login'],
                        github_access_token=access_token
                    )
                    # Update auth provider if it was email
                    if user.auth_provider == 'email':
                        user.auth_provider = 'github'
                        user.save()
            except User.DoesNotExist:
                # Get user's name from GitHub
                name = user_data.get('name', '').split(' ', 1)
                first_name = name[0] if name else user_data['login']
                last_name = name[1] if len(name) > 1 else ''

                # Create new user
                user = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=settings.SOCIAL_AUTH_PASSWORD,
                    auth_provider='github',
                    is_verified=True  # GitHub users are pre-verified
                )
                GitHubUser.objects.create(
                    user=user,
                    github_id=user_data['id'],
                    github_login=user_data['login'],
                    github_access_token=access_token
                )

        # Generate JWT tokens
        tokens = user.tokens()

        return {
            'access_token': tokens.get('access'),
            'refresh_token': tokens.get('refresh'),
            'user': {
                'id': str(user.public_id),
                'email': user.email,
                'full_name': user.get_full_name,
                'is_verified': user.is_verified,
                'auth_provider': user.auth_provider
            }
        }