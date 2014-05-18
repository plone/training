class aptgetupdate {

    exec { "aptitude update --quiet --assume-yes":
        path => "/usr/bin",
        user => "root",
        timeout => 0,
    }

}

include aptgetupdate
