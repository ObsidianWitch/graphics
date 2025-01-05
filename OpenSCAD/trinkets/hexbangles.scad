include <../operators/shortcuts.scad>
include <../operators/shear.scad>

module pipe(h, r, b) {
    difference() {
        cylinder(h=h, r=r + b, center=true);
        cylinder(h=h+0.5, r=r, center=true);
    }
}

module pattern_hex(cyl_r, cyl_a=360, cyl_b, hex_r, hex_off=0, n, m) {
    dphi = cyl_a / n;
    for(j=[0 : m - 1]) {
        z = j*sqrt(3)/2*(hex_r + hex_off);
        for(i=[0 : n - 1]) {
            phi = (j % 2 == 0) ? dphi * i : dphi * i + dphi/2;
            rotz(phi) tra([0, cyl_r, z]) rotx(-90) {
                cylinder(h=cyl_b, r=hex_r, $fn=6);
            }
        }
    }
}

module pattern_stripe(cyl_r, cyl_a=360, cyl_b, stripe_l, n, m) {
    dphi = cyl_a / n;
    for(j=[0 : m - 1]) {
        for(i=[0 : n - 1]) {
            rotz(dphi*i) tra([0, cyl_r, stripe_l*j]) shearz(x=-1/2, y=0) {
                cube(size=[stripe_l/2, cyl_b, stripe_l], center=true);
            }
        }
    }
}

module pipe_stripe(cyl_r, cyl_b, stripe_l, n, m) {
     difference() {
        pipe(h=stripe_l + cyl_b, r=cyl_r, b=cyl_b);
        pattern_stripe(cyl_r=cyl_r, cyl_b=cyl_b*2, stripe_l=stripe_l, n=n, m=m);
    }
}

module pipe_hex0(cyl_r=35, cyl_a=300, cyl_b=2, hex_r=4, n=16, m=5) {
    difference() {
        pattern_hex(cyl_r=cyl_r, cyl_a=cyl_a, cyl_b=cyl_b, hex_r=hex_r, n=n, m=m);
        traz(sqrt(3)*hex_r) {
            pattern_hex(cyl_r=cyl_r - 0.5, cyl_a=cyl_a, cyl_b=cyl_b + 1, hex_r=hex_r, n=n, m=1);
        }
    }
}

module pipe_hex1(cyl_r=35, cyl_b=2, hex_r=5, hex_b=2, n=16, m=5) {
    difference() {
        pattern_hex(cyl_r=cyl_r, cyl_b=cyl_b, hex_r=hex_r, hex_off=0, n=n, m=m);
        pattern_hex(cyl_r=cyl_r - 0.5, cyl_b=cyl_b + 1, hex_r=hex_r - hex_b, hex_off=hex_b, n=n, m=m);
    }
}

module pipe_hex2($fn=128) {
    cyl_r = 35;
    cyl_b = 2;
    traz(20.3) pipe_stripe(cyl_r=cyl_r, cyl_b=cyl_b+0.5, stripe_l=4, n=70, m=1);
    pipe_hex1(cyl_r=cyl_r, cyl_b=cyl_b, hex_r=4, hex_b=1, n=20, m=5);
    traz(-6.45) pipe_stripe(cyl_r=cyl_r, cyl_b=cyl_b+0.5, stripe_l=4, n=70, m=1);
}

module pipe_hex3(cyl_r=35, cyl_b=2, hex_r=4, hex_b=1, n=20, m=3, $fn=128) {
    traz(m*sqrt(3)*hex_r/2 + hex_b/2) pipe(hex_b, cyl_r, cyl_b);
    pipe_hex1(cyl_r, cyl_b, hex_r, hex_b, n, m);
    traz(-sqrt(3)*hex_r/2 - hex_b/2) pipe(hex_b, cyl_r, cyl_b);
}

pipe_hex0();
tray(80) pipe_hex1();
tray(160) pipe_hex2();
trax(80) pipe_hex3();
