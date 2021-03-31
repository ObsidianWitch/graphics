module doorStop() {
    union() {
        cube([10, 14, 2]);
        cube([10, 1.6, 5.4]);
        translate([0, 0, 5.4 - 1.5]) cube([10, 9.5, 1.5]);
    }
}

doorStop();
