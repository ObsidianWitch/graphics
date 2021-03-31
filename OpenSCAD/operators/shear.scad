module shearAlongX(Y = 0, Z = 0) {
    M = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [Y, 0, 1, 0],
        [Z, 0, 0, 1]
    ];
    
    multmatrix(M) children();
}

module shearAlongY(X = 0, Z = 0) {
    M = [
        [1, X, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, Z, 0, 1]
    ];
    
    multmatrix(M) children();
}

module shearAlongZ(X = 0, Y = 0) {
    M = [
        [1, 0, X, 0],
        [0, 1, Y, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ];
    
    multmatrix(M) children();
}
