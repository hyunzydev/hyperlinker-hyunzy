# core/context_processors.py

from django.contrib import messages


def lazy_messages_list(request):

    def inner():
        message_list = messages.get_messages(request)

        return [
            {
                "level_tag": message.level_tag,
                "message": message.message,
            }
            for message in message_list
        ]

    return inner


def messages_list(request):
    return {
        "messages_list": lazy_messages_list(request),
    }
