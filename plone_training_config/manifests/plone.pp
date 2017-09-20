class plone {

    $plone_version = "5.0.7"

    file { ['/home/ubuntu/tmp',
            '/home/ubuntu/.buildout',
            '/home/ubuntu/buildout-cache',
            '/home/ubuntu/buildout-cache/eggs',
            '/home/ubuntu/buildout-cache/downloads',
            '/home/ubuntu/buildout-cache/extends',
            ]:
        ensure => directory,
        owner => 'ubuntu',
        group => 'ubuntu',
        mode => '0755',
    }

    file { '/home/ubuntu/.buildout/default.cfg':
        ensure => present,
        content => inline_template('[buildout]
eggs-directory = /home/ubuntu/buildout-cache/eggs
download-cache = /home/ubuntu/buildout-cache/downloads
extends-cache = /home/ubuntu/buildout-cache/extends'),
        owner => 'ubuntu',
        group => 'ubuntu',
        mode => '0664',
    }

    Exec {
        path => [
           '/usr/local/bin',
           '/opt/local/bin',
           '/usr/bin',
           '/usr/sbin',
           '/bin',
           '/sbin'],
        logoutput => true,
    }

    # Create virtualenv
    exec {'virtualenv --no-site-packages py27':
        alias => "virtualenv",
        creates => '/home/ubuntu/py27',
        user => 'ubuntu',
        cwd => '/home/ubuntu',
        before => Exec["install_buildout_setuptools"],
        timeout => 300,
    }

    # Install zc.buildout, setuptools
    exec {'/home/ubuntu/py27/bin/pip install -U zc.buildout==2.5.3 setuptools==26.1.1':
        alias => "install_buildout_setuptools",
        creates => '/home/ubuntu/py27/bin/buildout',
        user => 'ubuntu',
        cwd => '/home/ubuntu',
        before => Exec["checkout_training"],
        timeout => 0,
    }

    ## Download the buildout-cache from dist.plone.org - XXX training_buildout now uses 5.0.7 but there is no buildout cache dl for this release
    #exec {"wget http://dist.plone.org/release/${plone_version}/buildout-cache.tar.bz2":
    #    alias => "download_buildout_cache",
    #    creates => "/home/ubuntu/buildout-cache.tar.bz2",
    #    cwd => '/home/ubuntu',
    #    user => 'ubuntu',
    #    group => 'ubuntu',
    #    before => Exec["unpack_buildout_cache"],
    #    timeout => 600,
    #}

    ## Unpack the buildout-cache to /home/ubuntu/buildout-cache/
    #exec {"tar xjf /home/ubuntu/buildout-cache.tar.bz2":
    #    alias => "unpack_buildout_cache",
    #    creates => "/home/ubuntu/buildout-cache/eggs/Products.CMFPlone-${plone_version}-py2.7.egg/",
    #    user => 'ubuntu',
    #    cwd => '/home/ubuntu',
    #    before => Exec["checkout_training"],
    #    timeout => 0,
    #}

    # get training buildout, xenial branch
    exec {'git clone https://github.com/collective/training_buildout.git buildout && cd buildout && git checkout vagrant_xenial_update && cd ..':
        alias => "checkout_training",
        creates => '/vagrant/buildout',
        user => 'ubuntu',
        cwd => '/vagrant',
        before => Exec["buildout_training"],
        timeout => 0,
    }

    # run training buildout
    exec {'/home/ubuntu/py27/bin/buildout -c vagrant_provisioning.cfg':
        alias => "buildout_training",
        creates => '/vagrant/buildout/bin/instance',
        user => 'ubuntu',
        cwd => '/vagrant/buildout',
        # before => Exec["buildout_final"],
        timeout => 0,
    }

}

include plone
