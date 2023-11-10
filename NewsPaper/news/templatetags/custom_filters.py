from django import template


register = template.Library()

badwords = {
    'ni***': 'nigga',
    'ni****': 'nigger'
}


@register.filter()
def censor(post_content):
    for badword in badwords:
        if badwords[badword] in post_content:
            post_content = post_content.replace(badwords[badword], badword, 1000)
            return post_content
        else:
            return post_content
    return post_content

