include <../operators/shortcuts.scad>

module loop() {
    difference() {
        cube([4, 5, 17], center = true);
        cube([4, 2, 15], center = true);
    }
}

module claspClaw() {
    loop();

    tray(-4) difference() {
        cube([4, 5, 15], center = true);
        cylinder(h = 15, d = 3, center = true);
        trax(1) cube([2, 2.5, 15], center = true);
    }
}

module claspCyl() {
    loop();

    tray(-5) union() {
        cylinder(h = 17, d = 2, center = true);
        traz(-16/2) cube([4, 5, 1], center = true);
        traz(16/2) cube([4, 5, 1], center = true);
    }
}

claspClaw();
trax(5) claspCyl();
