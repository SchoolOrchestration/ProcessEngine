from processengine.models import Process

def create_fake_process(name=None, context={}):

    data = {
        "name": "foo.bar",
        "context": context
    }
    return Process.objects.create(**data)
