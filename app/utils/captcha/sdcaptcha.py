import random
import string


class Captcha(object):
    number = 6
    SOURCE = list(string.digits)

    @classmethod
    def gene_text(cls):
        return ''.join(random.sample(cls.SOURCE, cls.number))
