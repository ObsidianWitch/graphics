include <../primitives/tube.scad>

module beam(
    h = 8, dint = 4.8, dMid = 6.4, dext = 7.2, pitch = 0.8, holes = [1, 1],
    crossThickness = 2.4, zMid = 0.8
) {
    module hole() {
        module innerHole(up) {
            z = up ? h/2 - zMid/2 : -h/2 + zMid/2;

            translate([0, 0, z]) {
                cylinder(h = zMid, d = dMid, center = true);
            }
        }

        difference() {
            tube(h, dint, dext, center = true);
            innerHole(up = true);
            innerHole(up = false);
        }
    }

    module holeCross() {
        module crossPart() {
            cube([dMid, crossThickness, h], center = true);
        }

        difference() {
            cylinder(d = dext, h = h, center = true);
            crossPart();
            rotate([0, 0, 90]) crossPart();
        }
    }

    module holeCylinder() {
        cylinder(d = dext, h = h, center = true);
    }

    module selectHole(type) {
        if (type == 1) {
            hole();
        }
        else if (type == 2) {
            holeCross();
        }
        else if (type == 3) {
            holeCylinder();
        }
    }

    module plate(up) {
        size = [
            (len(holes) - 1) * (pitch + dext),
            dext/2 - dMid/2,
            h
        ];

        pos = [
            0,
            up ? dMid/2 : -size.y - dMid/2,
            -size.z/2
        ];

        translate(pos) cube(size);
    }

    union() {
        delta = dext + pitch;
        for (i = [0 : len(holes) - 1]) {
            translate([i * delta, 0, 0]) {
                selectHole(holes[i]);
            }
        }

        plate(up = true);
        plate(up = false);
    }
}

module invertedBeam(
    h = 8, dint = 4.8, dMid = 6.4, dext = 7.2, pitch = 0.8, holes = [1, 1],
    crossThickness = 2.4, zMid = 0.8
) {
    module hole() {
        module innerHole(up) {
            z = up ? h/2 - zMid/2 : -h/2 + zMid/2;

            translate([0, 0, z]) {
                cylinder(h = zMid, d = dMid, center = true);
            }
        }

        union() {
            cylinder(h = h, d = dint, center = true);
            innerHole(up = true);
            innerHole(up = false);
        }
    }

    module holeCross() {
        module crossPart() {
            cube([dMid, crossThickness, h], center = true);
        }

        union() {
            crossPart();
            rotate([0, 0, 90]) crossPart();
        }
    }

    module selectHole(type) {
        if (type == 1) {
            hole();
        }
        else if (type == 2) {
            holeCross();
        }
    }

    union() {
        delta = dext + pitch;
        for (i = [0 : len(holes) - 1]) {
            translate([i * delta, 0, 0]) {
                selectHole(holes[i]);
            }
        }
    }
}

beam(holes = [1, 1, 1, 1, 1]);
