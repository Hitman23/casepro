from __future__ import unicode_literals

import datetime
import pytz

from casepro.cases.models import Label, Partner
from casepro.contacts.models import Contact, Group, Field
from casepro.profiles import ROLE_ANALYST, ROLE_MANAGER
from dash.test import DashTest
from django.contrib.auth.models import User


class BaseCasesTest(DashTest):
    """
    Base class for all test cases
    """
    def setUp(self):
        # some orgs
        self.unicef = self.create_org("UNICEF", timezone="Africa/Kampala", subdomain="unicef")
        self.nyaruka = self.create_org("Nyaruka", timezone="Africa/Kigali", subdomain="nyaruka")

        # some admins for those orgs
        self.admin = self.create_admin(self.unicef, "Kidus", "kidus@unicef.org")
        self.norbert = self.create_admin(self.nyaruka, "Norbert Kwizera", "norbert@nyaruka.com")

        # some partners
        self.moh = self.create_partner(self.unicef, "MOH")
        self.who = self.create_partner(self.unicef, "WHO")
        self.klab = self.create_partner(self.nyaruka, "kLab")

        # some users in those partners
        self.user1 = self.create_user(self.unicef, self.moh, ROLE_MANAGER, "Evan", "evan@unicef.org")
        self.user2 = self.create_user(self.unicef, self.moh, ROLE_ANALYST, "Bob", "bob@unicef.org")
        self.user3 = self.create_user(self.unicef, self.who, ROLE_MANAGER, "Carol", "carol@unicef.org")
        self.user4 = self.create_user(self.nyaruka, self.klab, ROLE_ANALYST, "Bosco", "bosco@klab.rw")

        # some message labels
        self.aids = self.create_label(self.unicef, "AIDS", 'Messages about AIDS',
                                      ['aids', 'hiv'], [self.moh, self.who], 'L-001')
        self.pregnancy = self.create_label(self.unicef, "Pregnancy", 'Messages about pregnancy',
                                           ['pregnant', 'pregnancy'], [self.moh], 'L-002')
        self.code = self.create_label(self.nyaruka, "Code", 'Messages about code',
                                      ['java', 'python', 'go'], [self.klab], 'L-003')

        # some groups
        self.males = self.create_group(self.unicef, 'G-001', 'Males')
        self.females = self.create_group(self.unicef, 'G-002', 'Females')
        self.reporters = self.create_group(self.unicef, 'G-003', 'Reporters', suspend_from=True)
        self.coders = self.create_group(self.nyaruka, 'G-004', 'Coders')

        # some fields
        self.nickname = self.create_field(self.unicef, 'nickname', "Nickname", value_type='T')
        self.age = self.create_field(self.unicef, 'age', "Age", value_type='N')
        self.state = self.create_field(self.unicef, 'state', "State", value_type='S', is_visible=False)
        self.motorbike = self.create_field(self.nyaruka, 'motorbike', "Moto", value_type='T')

    def create_partner(self, org, name):
        return Partner.create(org, name, None)

    def create_admin(self, org, full_name, email):
        user = User.create(None, None, None, full_name, email, password=email, change_password=False)
        org.administrators.add(user)
        return user

    def create_user(self, org, partner, role, full_name, email):
        return User.create(org, partner, role, full_name, email, password=email, change_password=False)

    def create_label(self, org, name, description, words, partners, uuid):
        return Label.create(org, name, description, words, partners, uuid)

    def create_contact(self, org, uuid, name, groups=(), fields=None):
        contact = Contact.objects.create(org=org, uuid=uuid, name=name, is_stub=False, fields=fields)

        for group in groups:
            contact.groups.add(group)

        return contact

    def create_group(self, org, uuid, name, is_visible=True, suspend_from=False):
        return Group.objects.create(org=org, uuid=uuid, name=name, is_visible=is_visible, suspend_from=suspend_from)

    def create_field(self, org, key, label, value_type='T', is_visible=True):
        return Field.objects.create(org=org, key=key, label=label, value_type=value_type, is_visible=is_visible)

    def datetime(self, year, month, day, hour=0, minute=0, second=0, microsecond=0, tz=pytz.UTC):
        return datetime.datetime(year, month, day, hour, minute, second, microsecond, tz)

