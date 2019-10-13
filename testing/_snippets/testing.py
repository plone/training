# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import plonetraining.testing


class PlonetrainingTestingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=plonetraining.testing)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plonetraining.testing:default')


PLONETRAINING_TESTING_FIXTURE = PlonetrainingTestingLayer()


PLONETRAINING_TESTING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONETRAINING_TESTING_FIXTURE,),
    name='PlonetrainingTestingLayer:IntegrationTesting',
)


PLONETRAINING_TESTING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONETRAINING_TESTING_FIXTURE,),
    name='PlonetrainingTestingLayer:FunctionalTesting',
)


PLONETRAINING_TESTING_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONETRAINING_TESTING_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='PlonetrainingTestingLayer:AcceptanceTesting',
)
