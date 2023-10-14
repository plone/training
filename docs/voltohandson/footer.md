---
myst:
  html_meta:
    'description': 'Learn How to customize the Footer of the page'
    'property=og:description': 'Learn How to customize the Footer of the page'
    'property=og:title': 'Footer customization'
    'keywords': 'Plone, Volto, Training, Theme, Footer'
---

(voltohandson-footer-label)=

# Footer

We customize the footer using component shadowing as well, by copying the original Volto `Footer` component from the `omelette` folder (`omelette/src/components/theme/Footer/Footer.jsx`) into the `customizations/components/theme/Footer/Footer.jsx` file.

Since we need the Logo component in the Footer, we import it from Volto as we did in the Header:

```jsx
import { Logo } from '@plone/volto/components';
```
We also need the `Grid` component from Semantic UI:

```jsx
import { Container, List, Grid } from 'semantic-ui-react';
```

Then, we replace the `Footer` component content to match the one from plone.org.

```jsx
<div id="footer">
      <Container>
        <div id="footer-main">
          <Grid textAlign="left" columns={4}>
            <Grid.Column>
              <List>
                <List.Header>
                  <a href="https://plone.org/why-plone">About Plone</a>
                </List.Header>
                <List.Content>
                  <List.Item>
                    <a href="https://plone.org/try-plone">Try Plone</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://plone.org/download">Download Plone</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://6.docs.plone.org">Documentation</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://training.plone.org">Training</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://plone.org/security">Security</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://plone.org/roadmap">Roadmap</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://github.com/plone">Github</a>
                  </List.Item>
                </List.Content>
              </List>
            </Grid.Column>
            <Grid.Column>
              <List>
                <List.Header>
                  <a href="https://plone.org/community">Community</a>
                </List.Header>
                <List.Content>
                  <List.Item>
                    <a href="https://community.plone.org/">Forum</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://plone.org/community/chat">Chat</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://plone.org/contribute">Contribute code</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://plone.org/community/bugs">Report an issue</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://plone.org/news-and-events">News and events</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://ploneconf.org">Conference</a>
                  </List.Item>
                </List.Content>
              </List>
            </Grid.Column>
            <Grid.Column>
              <List>
                <List.Header>
                  <a href="https://plone.org/foundation">Foundation</a>
                </List.Header>
                <List.Content>
                  <List.Item>
                    <a href="https://plone.org/foundation/members/application-procedure">
                      Join the foundation
                    </a>
                  </List.Item>
                  <List.Item>
                    <a href="https://plone.org/foundation/board">Board</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://github.com/sponsors/plone">Donate</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://plone.org/foundation/sponsorship">Sponsors</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://plone.org/foundation/materials/foundation-resolutions/code-of-conduct">
                      Code of conduct
                    </a>
                  </List.Item>
                  <List.Item>
                    <a href="https://plone.org/foundation/members">Foundation members</a>
                  </List.Item>
                  <List.Item>
                    <a href="https://plone.teemill.com/">Shop</a>
                  </List.Item>
                </List.Content>
              </List>
            </Grid.Column>
            <Grid.Column className="separated">
              <List>
                <List.Header>
                  <a href="https://plone.org/news-and-events/plone-in-social-media">
                    Follow us
                  </a>
                </List.Header>
                <List.Content>
                  <Grid textAlign="left" columns={2}>
                    <Grid.Column>
                      <List>
                        <List.Content>
                          <List.Item>
                            <a href="https://plone.social/@plone" rel="me">
                              Mastodon
                            </a>
                          </List.Item>
                          <List.Item>
                            <a href="https://twitter.com/plone">Twitter</a>
                          </List.Item>
                          <List.Item>
                            <a href="https://www.instagram.com/plonecms/">
                              Instagram
                            </a>
                          </List.Item>
                        </List.Content>
                      </List>
                    </Grid.Column>
                    <Grid.Column>
                      <List>
                        <List.Content>
                          <List.Item>
                            <a href="https://www.youtube.com/@plonecms">
                              YouTube
                            </a>
                          </List.Item>
                          <List.Item>
                            <a href="https://www.linkedin.com/company/plone-foundation/">
                              Linkedin
                            </a>
                          </List.Item>
                          <List.Item>
                            <a href="https://www.facebook.com/plonecms">
                              Facebook
                            </a>
                          </List.Item>
                        </List.Content>
                      </List>
                    </Grid.Column>
                  </Grid>
                </List.Content>
              </List>
              <List>
                <List.Header>
                  <List.Item>
                    <a href="https://plone.org/privacy-policy">Privacy Policy</a>
                  </List.Item>
                </List.Header>
                <List.Content>
                  <List.Item>Cookie Settings</List.Item>
                </List.Content>
              </List>
            </Grid.Column>
          </Grid>
        </div>
      </Container>
      <div id="footer-small-wrapper">
        <Container>
          <div id="footer-small">
            <div className="logo">
              <Logo />
            </div>
            <div className="address">
              The text and illustrations in this website are licensed by the
              Plone Foundation under a Creative Commons Attribution-ShareAlike
              4.0 International license. Plone and the Plone® logo are
              registered trademarks of the Plone Foundation, registered in the
              United States and other countries. For guidelines on the permitted
              uses of the Plone trademarks, see
              https://plone.org/foundation/logo. All other trademarks are owned
              by their respective owners.
            </div>
          </div>
        </Container>
      </div>
    </div>
```

And we Add this styling to the `custom.overrides` file:

```less
//Footer
#footer {
  padding: 2rem 0 0 0;
  margin: 1rem 0 0 0;
  box-shadow: 0px 5px 7px 5px rgba(119, 119, 119, 0.1);

  #footer-main {
    display: flex;
    /*
     *margin-right: -15px;
     *margin-left: -15px;
     */
    .ui {
      width: 100%;

      .column {
        flex: 1 1 25%;

        &.separated {
          border-left: 1px solid @black;
        }

        .list {
          padding: 0;
          font-size: 0.8rem;
          list-style-type: none;

          .header {
            display: flex;
            margin-bottom: 0.5rem;
            font-size: 1rem;
            font-weight: normal;

            a {
              &:hover,
              &:active,
              &:focus {
                color: @primaryColor;
                text-decoration: underline;
              }
            }
          }

          .content {
            .item {
              margin-bottom: 0.7em;
              color: @black;
              line-height: 1.5;

              a {
                color: @black !important;

                &:hover,
                &:active,
                &:focus {
                  color: @primaryColor;
                  text-decoration: underline;
                }
              }
            }
          }
        }
      }
    }
  }

  #footer-small-wrapper {
    padding: 1.5rem;
    margin-top: 1.5rem;
    background-color: #f9f9f9;

    #footer-small {
      display: flex;
      align-items: center;
      font-size: 0.7rem;

      .logo {
        flex: 0 0 auto;
      }

      .address {
        padding: 0 0.5rem;
      }

      .logo {
        padding-right: 1.5rem;
      }

      .address {
        color: @black;
        line-height: 1.3;
      }
    }
  }
}
```
