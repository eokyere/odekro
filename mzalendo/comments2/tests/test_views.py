from django.conf import settings

from django_webtest import WebTest
from django.test.client import Client
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.db import IntegrityError

import pprint

from comments2.models import Comment
from comments2.tests.models import RockStar

class CommentsViews(WebTest):
    urls = 'comments2.urls'
    fixtures = ['comments2-test-data.json']
    
    def setUp(self):
    
        self.test_object  = RockStar.objects.get(name='Slash')
        self.test_user    = User.objects.get(username = 'test-user')
        self.trusted_user = User.objects.get(username = 'trusted-user')

        # check that the trusted user has the correct permissions - don't trust
        # that the permission id listed in the fixture won't change
        self.assertFalse( self.test_user.has_perm('comments2.can_post_without_moderation') )
        self.assertTrue( self.trusted_user.has_perm('comments2.can_post_without_moderation') )

        # Useful to spit out the database setup
        # from django.core.management import call_command
        # call_command(
        #     'dumpdata',
        #     'auth.User', 'comments2.RockStar',
        #     indent=4, natural=True
        # )

    # def get_comments(self, test_object, user=None):
    #     return (
    #         self
    #           .app
    #           .get( test_object.get_absolute_url(), user=user )
    #           .click(description=r'^\d+ comments?$')
    #     )
    # 
    # def get_comments_add(self, test_object, user=None):
    #     return (
    #         self
    #           .get_comments( test_object, user )
    #           .click( description='Add your own comment' )
    #     )
    # 
    # def test_leaving_comment(self):
    #     # go to the test_object and check that there are no comments
    #     test_object = self.test_object
    #     app = self.app
    #     response = self.get_comments( test_object )
    #     
    #     # check that anon can't leave comments
    #     self.assertTemplateNotUsed( response, 'comments/form.html' )
    #     self.assertContains( response, "login to add your own comment" )
    #     
    #     # check that there is now a comment form
    #     response = self.get_comments_add( test_object, user=self.test_user  )
    #     
    #     self.assertTemplateUsed( response, 'comments/form.html' )
    #     
    #     # leave a comment
    #     form = response.forms['comment_form']
    #     form['title']   = 'Test Title'
    #     form['comment'] = 'Test comment'
    #     form_response = form.submit()
    #     self.assertEqual(response.context['user'].username, 'test-user')
    # 
    #     # check that the comment is correct and pending review
    #     comment = mz_comments.models.CommentWithTitle.objects.filter(
    #         content_type = ContentTypeManager().get_for_model(self.test_object),
    #         object_pk    = self.test_object.id,
    #     )[0]
    #     self.assertEqual( comment.title, 'Test Title' )
    #     self.assertEqual( comment.comment, 'Test comment' )
    #     self.assertEqual( comment.name, 'test-user' )
    #     self.assertEqual( comment.is_public, False )
    #     self.assertEqual( comment.is_removed, False )
    #     
    #     # check it is not visible on site
    #     res = self.get_comments( test_object )
    #     self.assertNotContains( res, comment.title )
    #             
    #     # approve the comment
    #     comment.is_public = True
    #     comment.save()
    #     
    #     # check that it is shown on site
    #     self.assertContains( self.get_comments( test_object ), comment.title )
    #     
    #     # flag the comment
    #     comment.is_removed = True
    #     comment.save()
    #     self.assertNotContains( self.get_comments( test_object ), comment.title )
    #     
    #     # delete the comment
    #     comment.delete()
    #     # check that comment not shown
    #     res =  self.get_comments( test_object )
    #     self.assertNotContains( res, comment.title )
    #     self.assertNotContains( res, 'comment removed' )
    # 
    # def test_trusted_users(self):
    #     """Test that users in the 'trusted' group have their comments posted at once"""
    # 
    #     app = self.app
    # 
    #     test_object = self.test_object
    #     trusted_user = self.trusted_user
    #     comment_title = "Trusted user comment"
    #     
    #     # get the test_object page with comment form on it
    #     res = self.get_comments_add( test_object, trusted_user )
    # 
    #     # leave a comment
    #     form = res.forms['comment_form']
    #     form['title']   = comment_title
    #     form['comment'] = 'Test comment'
    #     form_response = form.submit()
    # 
    #     # check that the comment is correct and public
    #     comment = mz_comments.models.CommentWithTitle.objects.filter(
    #         content_type = ContentTypeManager().get_for_model(self.test_object),
    #         object_pk    = self.test_object.id,
    #     )[0]
    #     self.assertEqual( comment.title, comment_title )
    #     self.assertEqual( comment.is_public, True )
    #     self.assertEqual( comment.is_removed, False )
    #     
    #     # check that it is shown on site
    #     self.assertContains( self.get_comments( test_object ), comment_title )
    #     
