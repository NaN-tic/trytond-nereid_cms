#This file is part nereid_cms module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from string import Template

from nereid import render_template, current_app, cache, request
from nereid.helpers import slugify, url_for, key_from_list
from nereid.contrib.pagination import Pagination
from nereid.contrib.sitemap import SitemapIndex, SitemapSection
from werkzeug.exceptions import NotFound, InternalServerError

from trytond.pyson import Eval, Not, Equal, Bool, In
from trytond.model import ModelSQL, ModelView, fields
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.backend import TableHandler

__all__ = ['Menu', 'Article', 'Banner']


class Menu(ModelSQL, ModelView):
    "Menu CMS"
    __name__ = 'nereid.cms.menu'
    _rec_name = 'title'
    title = fields.Char('Title', translate=True,
        required=True, on_change=['title', 'code'])
    code = fields.Char('Code', required=True,
        help='Internal code.')
    uri = fields.Char('URI', translate=True, required=True,
        help='Uri menu.')
    active = fields.Boolean('Active', select=True)
    parent = fields.Many2One("nereid.cms.menu", "Parent", select=True)
    left = fields.Integer('Left', required=True, select=True)
    right = fields.Integer('Right', required=True, select=True)
    childs = fields.One2Many('nereid.cms.menu', 'parent', 'Children')
    sequence = fields.Integer('Sequence',
        order_field='(%(table)s.sequence IS NULL) %(order)s, '
        '%(table)s.sequence %(order)s')

    @staticmethod
    def default_active():
        'Return True'
        return True

    @staticmethod
    def default_left():
        return 0

    @staticmethod
    def default_right():
        return 0

    @classmethod
    def __setup__(cls):
        super(Menu, cls).__setup__()
        cls._order.insert(0, ('sequence', 'ASC'))
        cls._order.insert(1, ('id', 'ASC'))

    @classmethod
    def __register__(cls, module_name):
        super(Menu, cls).__register__(module_name)
        cursor = Transaction().cursor

        table = TableHandler(cursor, cls, module_name)
        table.index_action(['left', 'right'], 'add')

    def on_change_title(self):
        res = {}
        if self.title and not self.code:
            res['code'] = slugify(self.title)
        return res

    @classmethod
    def validate(cls, menus):
        super(Menu, cls).validate(menus)
        cls.check_recursion(menus)

    @classmethod
    def copy(cls, menus, default=None):
        if default is None:
            default = {}

        default['left'] = 0
        default['right'] = 0

        new_menus = super(Menu, cls).copy(menus, default=default)
        return new_menus


class Article(ModelSQL, ModelView):
    "Article CMS"
    __name__ = 'nereid.cms.article'
    _rec_name = 'uri'
    _order_name = 'uri'
    title = fields.Char('Title', translate=True,
        required=True, on_change=['title', 'uri'])
    uri = fields.Char('URI', required=True,
        help='Unique Name is used as the uri.')
    description = fields.Text('Description', required=True, translate=True)
    metadescription = fields.Char('Meta Description', translate=True, 
        help='Almost all search engines recommend it to be shorter ' \
        'than 155 characters of plain text')
    metakeywords = fields.Char('Meta Keywords',  translate=True,
        help='Separated by comma')
    metatitle = fields.Char('Meta Title',  translate=True)
    template = fields.Char('Template', required=True)
    status = fields.Boolean('Status',
        help='Dissable to not show content article')

    @staticmethod
    def default_status():
        return True

    @staticmethod
    def default_template():
        return 'cms-article.jinja'

    @classmethod
    def __setup__(cls):
        super(Article, cls).__setup__()
        cls._order.insert(0, ('uri', 'DESC'))
        cls._order.insert(1, ('id', 'DESC'))
        cls._sql_constraints += [
            ('uri', 'UNIQUE(uri)',
                'The Unique Name of the Article must be unique.'),
            ]
        cls._error_messages.update({
            'delete_articles': ('You can not delete '
                'articles because you will get error 404 NOT Found. '
                'Dissable active field.'),
            })

    def on_change_title(self):
        res = {}
        if self.title and not self.uri:
            res['uri'] = slugify(self.title)
        return res

    @classmethod
    def copy(cls, posts, default=None):
        new_posts = []
        for post in posts:
            default['uri'] = '%s-copy' % post.uri
            new_post, = super(Post, cls).copy([post], default=default)
            new_posts.append(new_post)
        return new_posts

    @classmethod
    def delete(cls, posts):
        cls.raise_user_error('delete_articles')

    @classmethod
    def render(cls, uri):
        """
        Renders the template
        """
        try:
            article, = cls.search([('uri', '=', uri)])
        except ValueError:
            return NotFound()
        return render_template(article.template, article=article)

    def get_absolute_url(self, **kwargs):
        return url_for(
            'nereid.cms.article.render', uri=self.uri, **kwargs
        )


class Banner(ModelSQL, ModelView):
    "Banner CMS"
    __name__ = 'nereid.cms.banner'
    name = fields.Char('Name', required=True, on_change=['name', 'code'])
    code = fields.Char('Code', required=True, help='Internal code.')
    type = fields.Selection([
        ('image', 'Image'),
        ('remote_image', 'Remote Image'),
        ('custom_code', 'Custom Code'),
        ], 'Type', required=True)
    file = fields.Many2One('nereid.static.file', 'File',
        states = {
            'required': Equal(Eval('type'), 'image'),
            'invisible': Not(Equal(Eval('type'), 'image'))
            })
    remote_image_url = fields.Char('Remote Image URL',
        states = {
            'required': Equal(Eval('type'), 'remote_image'),
            'invisible': Not(Equal(Eval('type'), 'remote_image'))
            })
    custom_code = fields.Text('Custom Code', translate=True,
        states={
            'required': Equal(Eval('type'), 'custom_code'),
            'invisible': Not(Equal(Eval('type'), 'custom_code'))
            })
    height = fields.Integer('Height',
        states = {
            'invisible': Not(In(Eval('type'), ['image', 'remote_image']))
            })
    width = fields.Integer('Width',
        states = {
            'invisible': Not(In(Eval('type'), ['image', 'remote_image']))
            })
    alternative_text = fields.Char('Alternative Text',
        states = {
            'invisible': Not(In(Eval('type'), ['image', 'remote_image']))
            })
    click_url = fields.Char('Click URL', translate=True,
        states = {
            'invisible': Not(In(Eval('type'), ['image', 'remote_image']))
            })
    active = fields.Boolean('Active', select=True)

    @staticmethod
    def default_active():
        'Return True'
        return True

    @staticmethod
    def default_type():
        'Return Image'
        return 'image'

    def on_change_name(self):
        res = {}
        if self.name and not self.code:
            res['code'] = slugify(self.name)
        return res
