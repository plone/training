class packages {

  package { "build-essential":
      ensure => present,
  }
  package { "python-dev":
      ensure => present,
  }
  package { "libjpeg-dev":
      ensure => present,
  }
  package { "libxml2-dev":
      ensure => present,
  }
  package { "libxslt-dev":
      ensure => present,
  }
  package { "git":
      ensure => present,
  }
  package { "libz-dev":
      ensure => present,
  }
  package { "libssl-dev":
      ensure => present,
  }
  package { "subversion":
      ensure => present,
  }
  package { "wget":
      ensure => present,
  }
  package { "curl":
      ensure => present,
  }
  package { "elinks":
      ensure => present,
  }
  package { "vim":
      ensure => present,
  }
  package { "gettext":
      ensure => present,
  }
  package { "python-virtualenv":
      ensure => present,
  }
  package { "unzip":
      ensure => present,
  }
  package { "libpcre3-dev":
      ensure => present,
  }
  package { "libedit-dev":
      ensure => present,
  }
  package { "python-tk":
      ensure => present,
  }
  package { "libyaml-dev":
      ensure => present,
  }
  # Optional packages to enable indexing of office/pdf docs
  # package { "wv":                ensure => present, }
  # package { "poppler-utils":     ensure => present, }

  # used for creating a PuTTy-compatible key file
  package { "putty-tools":       ensure => present, }

}

include packages
