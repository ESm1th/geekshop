from social_core.exceptions import AuthForbidden


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == "google-oauth2":
        if 'gender' in response.keys():
            if response['gender'] == 'male':
                user.userprofile.gender = 'M'
            else:
                user.userprofile.gender = 'W'
            if 'tagline' in response.keys():
                user.userprofile.tag = response['tagline']
            if 'url' in response.keys():
                user.userprofile.about = response['url']
            if 'language' in response.keys():
                if user.userprofile.about:
                    user.userprofile.about += ('\n' + response['language'])
                else:
                    user.userprofile.about = response['language']
            if 'ageRange' in response.keys():
                minAge = response['ageRange']['min']
                print(minAge)
                if int(minAge) < 18:
                    user.delete()
                    raise AuthForbidden(
                        'social_core.backends.google.GoogleOAuth2')
        user.save()
    return
