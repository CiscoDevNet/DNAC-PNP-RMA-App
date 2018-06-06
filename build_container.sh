_build_container(){
    docker build -f Dockerfile -t "pnp-rma-new" . || _fatal "Docker failed to build PNP BATS container"
}

_build_container