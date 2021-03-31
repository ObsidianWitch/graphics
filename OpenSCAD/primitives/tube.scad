module tube(h, dint, dext, center = false) {
    difference() {
        cylinder(h = h, d = dext, center = center);
        cylinder(h = h + 0.1, d = dint, center = center);
    }
}
