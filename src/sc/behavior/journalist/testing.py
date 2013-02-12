from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import sc.behavior.journalist


SC_BEHAVIOR_JOURNALIST = PloneWithPackageLayer(
    zcml_package=sc.behavior.journalist,
    zcml_filename='testing.zcml',
    gs_profile_id='sc.behavior.journalist:testing',
    name="SC_BEHAVIOR_JOURNALIST")

SC_BEHAVIOR_JOURNALIST_INTEGRATION = IntegrationTesting(
    bases=(SC_BEHAVIOR_JOURNALIST, ),
    name="SC_BEHAVIOR_JOURNALIST_INTEGRATION")

SC_BEHAVIOR_JOURNALIST_FUNCTIONAL = FunctionalTesting(
    bases=(SC_BEHAVIOR_JOURNALIST, ),
    name="SC_BEHAVIOR_JOURNALIST_FUNCTIONAL")
