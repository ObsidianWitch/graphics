module frame2D(size = [5, 10], borderOut = 1, borderIn = 0, center = true) {
    module sq() { square([size.x, size.y], center = center); }

    difference() {
        offset(delta = borderOut) sq();
        offset(delta = -borderIn) sq();
    }
}

module frame(size = [5, 10, 15], borderOut = 1, borderIn = 0, center = true) {
    linear_extrude(height = size.z, center = center) {
        frame2D(
            size      = [size.x, size.y],
            borderOut = borderOut,
            borderIn  = borderIn,
            center    = center
        );
    }
}
