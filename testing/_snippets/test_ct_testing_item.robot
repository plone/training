# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s plonetraining.testing -t test_ct_testing_item.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src plonetraining.testing.testing.PLONETRAINING_TESTING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/plonetraining/testing/tests/robot/test_test_type.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a TestingItem
  Given a logged-in manager
    and an add TestingItem form
   When I type 'My TestingItem' into the title field
    and I submit the form
   Then a TestingItem with the title 'My TestingItem' has been created

Scenario: As a site administrator I can view a TestingItem
  Given a logged-in manager
    and a TestingItem 'Foo'
   When I go to the TestingItem view
   Then I can see the TestingItem title 'Foo'

Scenario: I can pass a custom message and see it in the page
  Given a logged-in manager
    and a TestingItem 'Foo'
   When I go to the testing-item-view view with a custom message 'Hello trainers'
   Then I can see my message 'Hello trainers' in the page

*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in manager
  Enable autologin as  Manager

an add TestingItem form
  Go To  ${PLONE_URL}/++add++TestingItem

a TestingItem '${id}'
  Create content  type=TestingItem  id=${id}  title=${id}

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the TestingItem view
  Go To  ${PLONE_URL}/foo
  Wait until page contains  Site Map

I go to the testing-item-view view with a custom message '${message}'
  Go To  ${PLONE_URL}/foo/testing-item-view?message=${message}
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a TestingItem with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the TestingItem title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

I can see my message '${message}' in the page
  Wait until page contains  Site Map
  Page should contain  ${message}
