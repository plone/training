class plone {

    file { ['/home/vagrant/tmp',
            '/home/vagrant/.buildout',
            '/home/vagrant/buildout-cache',
            '/home/vagrant/buildout-cache/eggs',
            '/home/vagrant/buildout-cache/downloads',
            '/home/vagrant/buildout-cache/extends',
            '/home/vagrant/buildout-cache/Plone',]:
        ensure => directory,
        owner => 'vagrant',
        group => 'vagrant',
        mode => '0755',
    }

    file { '/home/vagrant/.buildout/default.cfg':
        ensure => present,
        content => inline_template('[buildout]
eggs-directory = /home/vagrant/buildout-cache/eggs
download-cache = /home/vagrant/buildout-cache/downloads
extends-cache = /home/vagrant/buildout-cache/extends'),
        owner => 'vagrant',
        group => 'vagrant',
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

    # Get the unified installer
    exec {'wget https://launchpad.net/plone/4.3/4.3.4/+download/Plone-4.3.4-UnifiedInstaller.tgz':
        alias => "download_installer",
        creates => '/home/vagrant/tmp/Plone-4.3.4-UnifiedInstaller.tgz',
        cwd => '/home/vagrant/tmp',
        user => 'vagrant',
        group => 'vagrant',
        before => Exec["untar_installer"],
        timeout => 600,
    }

    # Unpack unified installer
    exec {'tar xzf Plone-4.3.4-UnifiedInstaller.tgz':
        alias => "untar_installer",
        creates => '/home/vagrant/tmp/Plone-4.3.4-UnifiedInstaller',
        cwd => '/home/vagrant/tmp',
        user => 'vagrant',
        before => Exec["virtualenv"],
        timeout => 300,
    }

    # Create virtualenv
    exec {'virtualenv py27':
        alias => "virtualenv",
        creates => '/home/vagrant/py27',
        user => 'vagrant',
        cwd => '/home/vagrant',
        before => Exec["install_plone"],
        timeout => 300,
    }

    # Run unified installer
    exec {'/home/vagrant/tmp/Plone-4.3.4-UnifiedInstaller/install.sh standalone --with-python=/home/vagrant/py27/bin/python --password=admin --instance=zinstance --target=/home/vagrant/Plone':
        alias => "install_plone",
        creates => '/home/vagrant/Plone/zinstance/bin/buildout',
        user => 'vagrant',
        cwd => '/home/vagrant',
        before => Exec["copy_cache"],
        timeout => 0,
    }

    # Copy buildout-cache
    exec {'cp -Rf /home/vagrant/Plone/buildout-cache/* /home/vagrant/buildout-cache/':
        alias => "copy_cache",
        creates => '/home/vagrant/buildout-cache/eggs/Products.CMFPlone-4.3.4-py2.7.egg/',
        user => 'vagrant',
        cwd => '/home/vagrant',
        before => Exec["checkout_training"],
        timeout => 0,
    }

    # get training buildout
    exec {'git clone https://github.com/collective/training_buildout.git buildout':
        alias => "checkout_training",
        creates => '/vagrant/buildout',
        user => 'vagrant',
        cwd => '/vagrant',
        before => Exec["install_setuptools"],
        timeout => 0,
    }


    # we skip this step since the virtualenv would add symlinks to the shared folder
    # # create virtualenv for training
    # exec {'virtualenv --no-site-packages /vagrant/buildout/py27':
    #     alias => "virtualenv_training",
    #     creates => '/vagrant/buildout/py27/bin/python',
    #     user => 'vagrant',
    #     cwd => '/vagrant/buildout',
    #     before => Exec["bootstrap_training"],
    #     timeout => 0,
    # }

    # install setuptools
    exec {'/home/vagrant/py27/bin/pip install -U setuptools==12.2':
        alias => "install_setuptools",
        user => 'vagrant',
        cwd => '/vagrant/buildout',
        before => Exec["bootstrap_training"],
        timeout => 0,
    }

    # bootstrap training buildout
    exec {'/home/vagrant/py27/bin/python bootstrap.py':
        alias => "bootstrap_training",
        creates => '/vagrant/buildout/bin/buildout',
        user => 'vagrant',
        cwd => '/vagrant/buildout',
        before => Exec["buildout_training"],
        timeout => 0,
    }

    # run training buildout
    exec {'/vagrant/buildout/bin/buildout':
        alias => "buildout_training",
        creates => '/vagrant/buildout/bin/instance',
        user => 'vagrant',
        cwd => '/vagrant/buildout',
        # before => Exec["buildout_final"],
        timeout => 0,
    }


}

include plone
