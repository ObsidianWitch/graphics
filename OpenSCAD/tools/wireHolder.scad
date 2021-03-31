include <../operators/shortcuts.scad>

module wireHolder() {
    module hole(d) { cylinder(d = d, h = 6, center = true, $fn = 32); }
    module screwBase(x) { tray(-4.5) cube([x, 2, 6], center = true); }

    module arch(d) {
        hull() {
            hole(d);
            screwBase(d);
        }
    }

    module base() {
        union() {
            arch(d = 11);
            screwBase(x = 20);
        }
    }

    module holes() {
        arch(d = 10);
        tra([-7.5, -4.5, 0]) rotx(90) hole(d = 3);
        tra([7.5, -4.5, 0]) rotx(90) hole(d = 3);
    }

    difference() {
        base();
        holes();
    }
}

wireHolder();
