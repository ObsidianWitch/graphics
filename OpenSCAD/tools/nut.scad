include <../primitives/tube.scad>

module thread(dint = 12, oExt = 1, height = 10, pitch = 1, slices = 128) {
    twist = (-360 * height) / pitch;

    linear_extrude(
        height = height, center = true, convexity = 10,
        twist = twist, slices = slices
    ) translate([dint/2 + oExt/2, 0, 0]) {
        circle(r = oExt/2);
    }
}

union() {
    tube(h = 5, dint = 13, dext = 15, center = true, $fn = 16);
    thread(dint = 12, oExt = 1, height = 5, pitch = 1, slices = 128);
}
