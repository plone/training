class buildout {

    exec { "aptitude update --quiet --assume-yes":
        path => "/usr/bin",
        user => "root",
        timeout => 0,
        before => Package['python-virtualenv'],
    }

    package { 'python-virtualenv':
        ensure => installed,
        before => Exec["virtualenv"],
    }

    package { ['build-essential',
               'python-dev',
               'libjpeg62-dev',
               'libxslt1-dev',
               'git-core',
               'subversion',
               'zlib1g-dev',
               'libbz2-dev',
               'wget',
               'curl',
               'elinks',
               'gettext']:
        ensure => installed,
        before => Exec["virtualenv"],
    }

    file { ['/home/vagrant/tmp',
            '/home/vagrant/.buildout',
            '/home/vagrant/buildout-cache',
            '/home/vagrant/buildout-cache/eggs',
            '/home/vagrant/buildout-cache/downloads',
            '/home/vagrant/buildout-cache/extends',]:
        ensure => directory,
        owner => 'vagrant',
        group => 'vagrant',
        mode => '0755',
    }

    file { '/home/vagrant/.buildout/default.cfg':
        ensure => present,
        content => template('buildout/default.cfg'),
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

    # Get the unified installer and unpack the buildout-cache
    exec {'wget https://launchpad.net/plone/4.3/4.3.2/+download/Plone-4.3.2-UnifiedInstaller.tgz':
        creates => '/home/vagrant/tmp/Plone-4.3.2-UnifiedInstaller.tgz',
        cwd => '/home/vagrant/tmp',
        user => 'vagrant',
        group => 'vagrant',
        before => Exec["untar_installer"],
        timeout => 600,
    }

    exec {'tar xzf Plone-4.3.2-UnifiedInstaller.tgz':
        alias => "untar_installer",
        creates => '/home/vagrant/tmp/Plone-4.3.2-UnifiedInstaller',
        cwd => '/home/vagrant/tmp',
        user => 'vagrant',
        before => Exec["virtualenv"],
        timeout => 300,
    }

    exec {'virtualenv --no-site-packages py27':
        alias => "virtualenv",
        creates => '/home/vagrant/py27',
        user => 'vagrant',
        cwd => '/home/vagrant',
        before => Exec["install_plone"],
        timeout => 300,
    }

    exec {'/home/vagrant/tmp/Plone-4.3.2-UnifiedInstaller/install.sh standalone --with-python=/home/vagrant/py27/bin/python --password=admin --instance=zinstance --target=/home/vagrant/training':
        alias => "install_plone",
        creates => '/home/vagrant/training/zinstance/bin/buildout',
        user => 'vagrant',
        cwd => '/home/vagrant',
        timeout => 0,
    }

}