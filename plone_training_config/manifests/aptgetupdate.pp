class aptgetupdate {

    exec { "apt-get update -q --assume-yes --fix-missing":
        path => "/usr/bin",
        user => "root",
        timeout => 0,
    }

}

include aptgetupdate
