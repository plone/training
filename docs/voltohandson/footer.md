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

Then, we replace the `Footer` component content to match the one from `plone.org`.

```jsx
<>
  <Segment
    role="contentinfo"
    vertical
    padded
    inverted
    textAlign="center"
    id="footer"
  >
    <Container>
      <Grid textAlign="left" columns={6}>
        <Grid.Column>
          <List inverted>
            <List.Header>
              <UniversalLink href="/about-plone">
                Plone Foundation
              </UniversalLink>
            </List.Header>
            <List.Content>
              <List.Item>
                <UniversalLink href="/donate">Donate & Sponsors</UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="/meeting">Meeting minutes</UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="/board">Current board</UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="/board">Foundation members</UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="/coc">Code of Conduct</UniversalLink>
              </List.Item>
            </List.Content>
          </List>
        </Grid.Column>
        <Grid.Column>
          <List inverted>
            <List.Header>
              <UniversalLink href="/support">Support</UniversalLink>
            </List.Header>
            <List.Content>
              <List.Item>
                <UniversalLink href="/community/chat">Chat room</UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="https://community.plone.org/">
                  Forums
                </UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="/locals">Local user groups</UniversalLink>
              </List.Item>
            </List.Content>
          </List>
        </Grid.Column>
        <Grid.Column>
          <List inverted>
            <List.Header>
              <UniversalLink href="/downloads">Downloads</UniversalLink>
            </List.Header>
            <List.Content>
              <List.Item>
                <UniversalLink href="/get-plone">Get Plone</UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="/addons">All add-ons</UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="/security">Security</UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="/hotfixes">Check hotfixes</UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="https://github.com/plone">
                  Browse source
                </UniversalLink>
              </List.Item>
            </List.Content>
          </List>
        </Grid.Column>
        <Grid.Column>
          <List inverted>
            <List.Header>
              <UniversalLink href="https://docs.plone.org/">
                Documentation
              </UniversalLink>
            </List.Header>
            <List.Content>
              <List.Item>
                <UniversalLink href="https://docs.plone.org/">
                  Full documentation
                </UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="https://training.plone.org/">
                  Training
                </UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="http://docs.plone.org/manage/installing/">
                  Installation
                </UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="https://www.youtube.com/c/PloneCMS">
                  YouTube
                </UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="https://www.linkedin.com/company/plone-foundation/">
                  Linkedin
                </UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="/about">About this site</UniversalLink>
              </List.Item>
            </List.Content>
          </List>
        </Grid.Column>
        <Grid.Column>
          <List inverted>
            <List.Header>
              <UniversalLink href="/contribute">Contribute</UniversalLink>
            </List.Header>
            <List.Content>
              <List.Item>
                <UniversalLink href="/roadmap">Roadmap</UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="/report-bugs">
                  Report bugs in Plone
                </UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="/security">
                  Report website issues
                </UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="/skills">Contribute skills</UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="https://github.com/plone">
                  Contribute code
                </UniversalLink>
              </List.Item>
            </List.Content>
          </List>
        </Grid.Column>
        <Grid.Column>
          <List inverted>
            <List.Header>
              <UniversalLink href="/contribute">Stay up to date</UniversalLink>
            </List.Header>
            <List.Content>
              <List.Item>
                <UniversalLink href="/newsletter">
                  Newsletter signup
                </UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="http://planet.plone.org/">
                  Planet Plone (blogs)
                </UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="https://twitter.com/plone">
                  @plone on Twitter
                </UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="https://www.facebook.com/plonecms/">
                  PloneCMS on Facebook
                </UniversalLink>
              </List.Item>
              <List.Item>
                <UniversalLink href="https://www.linkedin.com/groups/2300">
                  Plone LinkedIn group
                </UniversalLink>
              </List.Item>
            </List.Content>
          </List>
        </Grid.Column>
      </Grid>
    </Container>
  </Segment>
  <Segment id="sub-footer">
    <Container>
      <Grid columns={4}>
        <Grid.Column>
          <Logo />
        </Grid.Column>
        <Grid.Column>
          <p>
            The text and illustrations in this website are licensed by the Plone
            Foundation under a Creative Commons Attribution-ShareAlike 4.0
            International license.
          </p>
        </Grid.Column>
        <Grid.Column>
          <p>
            Plone and the Plone® logo are registered trademarks of the Plone
            Foundation, registered in the United States and other countries. For
            guidelines on the permitted uses of the Plone trademarks, see{' '}
            <UniversalLink href="https://plone.org/foundation/logo">
              https://plone.org/foundation/logo
            </UniversalLink>
          </p>
        </Grid.Column>
        <Grid.Column>
          <p>All other trademarks are owned by their respective owners.</p>
        </Grid.Column>
      </Grid>
    </Container>
  </Segment>
</>
```

and add this styling to the `custom.overrides` file:

```less
//Footer
#footer {
  background-color: #113156;
  color: #dfe6ec;
  padding-top: 55px;
  .ui.grid {
    .ui.list {
      a:hover {
        text-decoration: underline;
      }
      .header {
        margin-bottom: 19px;

        a {
          font-size: 15px;
          color: #dfe6ec;
        }
      }
      .item {
        margin-bottom: 6px;
        a {
          font-size: 12.5px;
        }
      }
    }
  }
}

#sub-footer {
  background: #1f1238;
  margin-top: 0;
  border: none;
  padding-top: 36px;
  padding-bottom: 54px;
  p,
  a {
    color: @white;
    font-size: 11.5px;
    font-weight: bold;
  }
}
```
