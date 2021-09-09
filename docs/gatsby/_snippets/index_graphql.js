import React from 'react'
import { Link } from 'gatsby'
import { graphql } from 'gatsby'

import Layout from '../components/layout'

const IndexPage = ({data}) => (
  <Layout>
    <h1>Hi Plone people</h1>
    <h4>This is the site title: {data.site.siteMetadata.title}</h4>
    <p>Welcome to your new Gatsby site.</p>
    <p>Now go build something great.</p>
    <Link to="/page-2/">Go to page 2</Link>
  </Layout>
)

export const query = graphql`
    query {
        site {
            siteMetadata {
                title
            }
        }
    }
`

export default IndexPage
