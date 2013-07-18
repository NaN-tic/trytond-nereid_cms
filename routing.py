#This file is part nereid_cms module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

__all__ = ['WebSite']
__metaclass__ = PoolMeta


class WebSite:
    'WebSite'
    __name__ = "nereid.website"

    @staticmethod
    def menu(code=None):
        """
        Return the obj menu by code
        
        HTML usage in template:

        {% set menu=request.nereid_website.menu('code') %}
        {% if menu %}
            {% set menus=menu.childs %}{% for menu in menus %}
                <a href="{{ menu.uri }}" alt="{{ menu.title }}">{{ menu.title }}</a>
            {% endfor %}
        {% endif %}
        """
        if not code:
            return []

        Menu = Pool().get('nereid.cms.menu')

        # Search by code
        menus = Menu.search([('code', '=', code)])
        if not menus:
            return []
        menus = Menu.browse([menus[0]])[0]
        return menus

    @staticmethod
    def banner(code=None):
        """
        Return the HTML content

        HTML usage in template:

        {% set image=request.nereid_website.banner('code') %}{{ image|safe }}
        {% set remote_image=request.nereid_website.banner('code') %}{{ remote_image|safe }}
        {% set custom_code=request.nereid_website.banner('code') %}{{ custom_code|safe }}
        """
        if not code:
            return ''

        StaticFile = Pool().get('nereid.static.file')
        Banner = Pool().get('nereid.cms.banner')

        # Search by code
        banners = Banner.search([('code', '=', code)])
        if not banners:
            return ''

        banner = Banner.read([banners[0]], ['type', 'click_url', 'file',
            'remote_image_url', 'custom_code', 'height', 'width',
            'alternative_text', 'click_url'])[0]

        if banner['type'] == 'image':
            file = StaticFile(banner['file'])
            banner['file'] = file.url

            if not banner.get('alternative_text'):
                banner['alternative_text'] = ''
            if not banner.get('width'):
                banner['width'] = ''
            if not banner.get('height'):
                banner['height'] = ''

            image = u'<img src="%(file)s" alt="%(alternative_text)s"' \
                    u' width="%(width)s" height="%(height)s"/>' % {
                        'file': banner['file'],
                        'alternative_text': banner['alternative_text'],
                        'width': banner['width'],
                        'height': banner['height'],
                        }
            if banner.get('click_url'):
                image = u'<a href="%(click_url)s">%(image)s</a>' % {
                        'click_url': banner['click_url'],
                        'image': image,
                        }
            return image

        elif banner['type'] == 'remote_image':
            if not banner.get('alternative_text'):
                banner['alternative_text'] = ''
            if not banner.get('width'):
                banner['width'] = ''
            if not banner.get('height'):
                banner['height'] = ''

            image = u'<img src="%(remote_image_url)s" alt="%(alternative_text)s"' \
                    u' width="%(width)s" height="%(height)s"/>' % {
                        'remote_image_url': banner['remote_image_url'],
                        'alternative_text': banner['alternative_text'],
                        'width': banner['width'],
                        'height': banner['height'],
                        }
            if banner.get('click_url'):
                image = u'<a href="%(click_url)s">%(image)s</a>' % {
                        'click_url': banner['click_url'],
                        'image': image,
                        }
            return image

        elif banner['type'] == 'custom_code':
            return banner['custom_code']
