import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

package = 'Test'


class Phrase(messages.Message):
    message = messages.StringField(1)


class PhrasesCollection(messages.Message):
    items = messages.MessageField(Phrase, 1, repeated=True)


STORED_PHRASES = PhrasesCollection(items=[
    Phrase(message='Hello World!'),
    Phrase(message='Goodbye World!'),
])


@endpoints.api(name='main', version='v1', description='!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
class MainApi(remote.Service):
    @endpoints.method(message_types.VoidMessage, PhrasesCollection, path='phrases', http_method='GET', name='main.listPhrases')
    def phrases_list(self, unused_request):
        return STORED_PHRASES

    ID_RESOURCE = endpoints.ResourceContainer(message_types.VoidMessage, id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Phrase, path='phrases/{id}', http_method='GET', name='main.getPhrase')
    def greeting_get(self, request):
        try:
            return STORED_PHRASES.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Phrase %s not found.' % (request.id,))


APPLICATION = endpoints.api_server([MainApi])
