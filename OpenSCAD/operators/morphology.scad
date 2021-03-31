include <shortcuts.scad>

// erosion

module erode() {
    difference() {
        minkowski() {
            children(0);
            children([1 : $children - 1]);
        }
        
        children([1 : $children - 1]);
    }
}

module erodeSph(r) {
    erode() {
        sphere(r);
        children();
    }
}

module erodeCirc(r, a) {
    erode() {
        rot(a) cylinder(r = r, h = 1e-308);
        children();
    }
}

module erodeSq(size, a) {
    erode() {
        rot(a) cube([size, size, 1e-308], center = true);
        children();
    }
}


// Dilatation

module dilate() {
    minkowski() children();
}

module dilateSph(r) {
    minkowski() {
        sphere(r);
        children();
    }
}

module dilateCyl(r, a) {
    minkowski() {
        rot(a) cylinder(r = r, h = 1e-308);
        children();
    }
}

module dilateSq(size, a) {
    minkowski() {
        rot(a) cube([size, size, 1e-308], center = true);
        children();
    }
}
