# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s plonetraining.testing -t test_autotoc.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src plonetraining.testing.testing.PLONETRAINING_TESTING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/plonetraining/testing/tests/robot/test_autotoc.robot
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

Scenario: I can see toc in testing-item-view
  Given a logged-in manager
    and a TestingItem 'Foo'
   When I go to the testing-item-view
   Then I can see the table of contents

Scenario: I see Tab 1 value by default in testing-item-view
  Given a logged-in manager
    and a TestingItem 'Foo'
   When I go to the testing-item-view
   Then I can see the content of tab ('Foo') and not 'Bar'

Scenario: I see Tab " value when i select it in testing-item-view
  Given a logged-in manager
    and a TestingItem 'Foo'
   When I go to the testing-item-view
    and I click 'Tab 2'
   Then I can see the content of tab ('Bar') and not 'Foo'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in manager
  Enable autologin as  Manager

an add TestingItem form
  Go To  ${PLONE_URL}/++add++TestingItem

a TestingItem '${id}'
  Create content  type=TestingItem  id=${id}  title=${id}

# --- WHEN -------------------------------------------------------------------

I go to the testing-item-view
  Go To  ${PLONE_URL}/foo/testing-item-view
  Wait until page contains  Site Map

I click '${tab}'
  Click Link  xpath=//a[contains(text(), "${tab}")]

# --- THEN -------------------------------------------------------------------

I can see the table of contents
  Wait until page contains  Site Map
  Page Should Contain Element  css=.autotoc-nav

I can see the content of tab ('${visible}') and not '${invisible}'
  Wait until page contains  Site Map
  Element Should Be Visible  xpath: //div[contains(text(), "${visible}")]
  Element Should Not Be Visible  xpath: //div[contains(text(), "${invisible}")]
