import os
from django.core.management.base import BaseCommand, CommandError

from odekro.management.hansard_parser import parse
from odekro.management.commands import add_infopage

class Command(BaseCommand):
    """Import Hansard"""

    help = 'Import Hansard'

    def handle(self, *args, **options):
        PAGES = (
            # About
            ('odekro-overview.md', 'Odekro Overview'),
            ('faqs.md', 'FAQs'),
            ('policies.md', 'Policies'),
            ('partners.md', 'Partners'),
            # Places
            ('places-overview.md', 'Overview'),
            # Parliament
            ('bills-overview.md', 'Bills overview'),
            # ??
            # ??

        )

        basedir = os.path.abspath(os.path.dirname( __file__ ))
        datadir = os.path.join(basedir, '..', '..', 'data')

        print '>>>>>>>>> DATA: ', datadir

        cmd = add_infopage.Command()

        for fname, title in PAGES:
            cmd.handle(*(os.path.join(datadir, fname), title))

