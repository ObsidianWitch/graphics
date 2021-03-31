include <../operators/shortcuts.scad>
include <../primitives/tube.scad>

module base() {
    dext = 82;
    difference() {
        union() {
            tube(h = 25, dint = 78, dext = dext);
            tube(h = 24, dint = 76, dext = dext);
            tube(h = 10, dint = 70, dext = dext);
            cylinder(h = 2, d = dext, center = false);
        }
        traz(2) tube(h = 4, dint = 77, dext = dext + 1);
    }
}

module pillars() {
    dext = 4;
    dint = 2;
    module short() { tube(h = 24, dint = dint, dext = dext); }
    module tall() { tube(h = 26, dint = dint, dext = dext); }

    tra([-21, -17, 0]) short();
    tra([-21, +17, 0]) short();
    tra([+21, -17, 0]) short();
    tra([+21, +17, 0]) short();
    tra([-27, +15, 0]) tall();
    tra([+27, +15, 0]) tall();
    tray(-31) tall();
}

module battery_holder() {
    difference() {
        cube(size = [68, 22, 8], center = true);
        traz(6) roty(90) cylinder(h = 66, d = 20, center = true);
    }
}

module holes_pos() {
    module pillar() { tube(h = 8, dint = 2, dext = 4); }
    trax(-10) pillar();
    trax(-2) {
        tube(h = 4, dint = 9, dext = 10);
        traz(1) tube(h = 1, dint = 8, dext = 9);
    }
    tra([6, 0, 1.5]) difference() {
        cube(size = [5, 9, 3], center = true);
        cube(size = [3, 8, 3], center = true);
    }
    trax(+10) pillar();
}

module holes_neg() {
    tra([-2, 0, 1]) cylinder(h = 2, d = 9, center = true);
    tra([6, 0, 1.5]) cube(size = [3, 8, 3], center = true);
}

module nightlight() {
    difference() {
        base();
        tray(25) holes_neg();
    }
    tray(25) holes_pos();
    traz(6) battery_holder();
    pillars();
}

nightlight($fn = 32);
