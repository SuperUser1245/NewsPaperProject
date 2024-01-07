from django import template


register = template.Library()

badwords = {'Elon',}


@register.filter
def censor(post_content):
    result = []
    for badword in badwords:
        if badword in post_content:
            vad = badword[0] + "*" * (len(badword) - 2) + badword[-1]
            post_content = post_content.replace(badword, vad)
            result = post_content
        else:
            result = post_content
    return result

