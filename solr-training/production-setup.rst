Production Setup
==================
TBD:
 - multi core
 - mointoring

different host setup
--------------------

One use case in a production setup might be the split between the Plone server
runs on and the Solr server(s).
To make this happen you have to consider a couple of things:

 - configure host of Solr in c.solr  - Can be done TTW, via ZCML or via /etc/hosts
 - make sure the blobstorage directory of Plone is available via a network drive
   to the Solr host. You need to make sure Solr has read permissions which
   usually means it has the *SAME* User ID than the user which runs the Zope
   server.


 - analyzing (GA, banana?)
