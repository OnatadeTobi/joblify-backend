from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from userauth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
import logging
import json
import requests  # Add standard requests library

logger = logging.getLogger(__name__)

class Google:
    @staticmethod
    def validate(access_token):
        try:
            # Log the token for debugging (remove in production)
            logger.debug(f"Validating Google token: {access_token[:10]}...")
            
            # First try to validate as ID token
            try:
                request = google_requests.Request()
                id_info = id_token.verify_oauth2_token(
                    access_token, 
                    request,
                    settings.GOOGLE_CLIENT_ID
                )
                if "accounts.google.com" in id_info['iss']:
                    return id_info
            except ValueError:
                # If ID token validation fails, try to get user info using access token
                pass

            # If not an ID token, try to get user info using the access token
            userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(userinfo_url, headers=headers)
            
            if response.status_code != 200:
                logger.error(f"Failed to get user info: {response.status_code}")
                raise AuthenticationFailed("Failed to get user info from Google")
            
            user_info = response.json()
            
            # Verify the email is verified
            if not user_info.get('email_verified', False):
                raise AuthenticationFailed("Email not verified with Google")
            
            # Get name information
            name = user_info.get('name', '').split(' ', 1)
            first_name = user_info.get('given_name', name[0] if name else 'User')
            last_name = user_info.get('family_name', name[1] if len(name) > 1 else 'User')
            
            # Format the response to match ID token format
            return {
                'sub': user_info.get('sub'),
                'email': user_info.get('email'),
                'email_verified': user_info.get('email_verified'),
                'name': user_info.get('name'),
                'given_name': first_name,
                'family_name': last_name,
                'picture': user_info.get('picture'),
                'iss': 'accounts.google.com'
            }
            
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            raise AuthenticationFailed("Token is invalid or has expired")

def get_user_tokens(user):
    try:
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
    except Exception as e:
        logger.error(f"Error generating tokens: {str(e)}")
        raise AuthenticationFailed("Error generating authentication tokens")

def register_social_user(provider, email, first_name, last_name):
    try:
        # Ensure we have valid first and last names
        if not first_name:
            first_name = 'User'
        if not last_name:
            last_name = 'User'
            
        # Try to find existing user
        user = User.objects.get(email=email)
        
        # If user exists with same provider, update their info
        if user.auth_provider == provider:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return get_user_tokens(user)
        
        # If user exists with different provider, raise error
        raise AuthenticationFailed(
            detail=f"Please continue your login with {user.auth_provider}"
        )
    
    except User.DoesNotExist:
        # Create new user
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=settings.SOCIAL_AUTH_PASSWORD,
            auth_provider=provider,
            is_verified=True  # Social auth users are pre-verified
        )
        return get_user_tokens(user)
    except Exception as e:
        logger.error(f"Error in register_social_user: {str(e)}")
        raise AuthenticationFailed("Error during user registration")

        
