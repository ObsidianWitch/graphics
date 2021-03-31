include <../operators/shortcuts.scad>

module spoolHolder() {
    module holes() {
        miry() tray(-15) cylinder(h = 12, d = 4, center = true);

        miry() tray(-30) {
            roty(90) cylinder(h = 12, d = 4, center = true);
            traz(2) cylinder(h = 12, d = 9, center = true);
        }

        trax(2) roty(90) cylinder(h = 12, d = 9, center = true);
    }

    difference() {
        cube([12, 80, 12], center = true);
        holes();
    }
}

spoolHolder($fn = 16);
