import random
import string

def create_blog_slug(title):

    title = title.split(' ')
    if len(title) < 3:
        return False, "Oops! blog title must be greater than 3 words"
    slug = '-'.join(title)
    return True, slug

def create_draft_reference():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))