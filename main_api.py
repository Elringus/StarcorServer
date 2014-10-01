import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

UNITY_CLIENT_ID = 'unity-starcor'

package = 'Test'


class Phrase(messages.Message):
    message = messages.StringField(1)


class PhrasesCollection(messages.Message):
    items = messages.MessageField(Phrase, 1, repeated=True)


STORED_PHRASES = PhrasesCollection(items=[
    Phrase(message='Hello World!'),
    Phrase(message='Goodbye World!'),
])


@endpoints.api(name='main', version='v1', description='Test API', allowed_client_ids=[UNITY_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID], scopes=[endpoints.EMAIL_SCOPE])
class MainApi(remote.Service):
    @endpoints.method(message_types.VoidMessage, PhrasesCollection, path='phrases', http_method='GET', name='main.listPhrases')
    def phrases_list(self, request):
        return STORED_PHRASES

    MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(Phrase, times=messages.IntegerField(1, variant=messages.Variant.INT32, required=True))

    @endpoints.method(MULTIPLY_METHOD_RESOURCE, Phrase, path='phrases/{times}', http_method='POST', name='main.multiplyPhrase')
    def phrases_multiply(self, request):
        return Phrase(message=request.message * request.times)

    ID_RESOURCE = endpoints.ResourceContainer(message_types.VoidMessage, id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Phrase, path='phrases/{id}', http_method='GET', name='main.getPhrase')
    def phrases_get(self, request):
        try:
            return STORED_PHRASES.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Phrase %s not found.' % (request.id,))

    @endpoints.method(message_types.VoidMessage, Phrase, path='phrases/authed', http_method='POST', name='main.authed')
    def phrases_authed(self, request):
        current_user = endpoints.get_current_user()
        email = current_user.email() if current_user is not None else 'Anonymous'
        return Phrase(message='Hello, %s!' % (email,))


APPLICATION = endpoints.api_server([MainApi])
