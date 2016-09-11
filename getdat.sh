#!/bin/bash/expect
set pass = "Ca$$y123"

scp petermcgill94@glamdring.physics.ox.ac.uk:/users/petermcgill94/reduction/out.npy /users/petermcgill/desktop/oxford/starpy-data-reduction/

<<<<<<< Updated upstream
=======
expect "petermcgill94@glamdring.physics.ox.ac.uk's password: "
send "$pass"
>>>>>>> Stashed changes
