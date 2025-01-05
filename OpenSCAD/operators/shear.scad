module shearx(y=0, z=0) {
    M = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [y, 0, 1, 0],
        [z, 0, 0, 1]
    ];

    multmatrix(M) children();
}

module sheary(x=0, z=0) {
    M = [
        [1, x, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, z, 0, 1]
    ];

    multmatrix(M) children();
}

module shearz(x=0, y=0) {
    M = [
        [1, 0, x, 0],
        [0, 1, y, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ];

    multmatrix(M) children();
}
