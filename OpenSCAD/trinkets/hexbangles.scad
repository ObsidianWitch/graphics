include <../operators/shortcuts.scad>
include <../operators/shear.scad>

// Hollow cylinder
module pipe(h, r, b) {
    difference() {
        cylinder(h=h, r=r + b, center=true);
        cylinder(h=h + 0.5, r=r, center=true);
    }
}

// ---

// Generates a pattern of stripes arranged in a circular manner and forming a pipe.
module pipe_pattern_stripe(pipe_r, pipe_b, stripe_l, stripe_n) {
    a = 360/stripe_n;
    for(i=[0 : stripe_n - 1]) {
        rotz(a*i) tra([0, pipe_r, stripe_l]) shearz(x=-1/2, y=0) {
            cube(size=[stripe_l/2, pipe_b, stripe_l], center=true);
        }
    }
}

module bangle_stripe0(pipe_r, pipe_b, stripe_l, stripe_n) {
    difference() {
        pipe(h=stripe_l + pipe_b, r=pipe_r, b=pipe_b);
        traz(-stripe_l) pipe_pattern_stripe(pipe_r, pipe_b*2, stripe_l, stripe_n);
    }
}

// ---

// Generates a pattern of hexagons arranged in a circular manner and forming a pipe.
// * pipe_r: pipe radius
// * pipe_b: pipe border
// * hex_n & hex_m: horizontal & vertical number of elements of the hexagonal grid
// * hex_r: hexagon tile radius
// * hex_zoffset: z offset between hexagon tiles
module pipe_pattern_hex(pipe_r, pipe_b, hex_n, hex_m, hex_r, hex_zoffset=0) {
    a = 360/hex_n; // angle offset between each hexagon tile
    for(j=[0 : hex_m - 1]) {
        z = j*sqrt(3)*(hex_r + hex_zoffset)/2;
        for(i=[0 : hex_n - 1]) {
            sum_a = (j % 2 == 0) ? a*i : a*i + a/2;
            rotz(sum_a) tra([0, pipe_r, z]) rotx(-90) {
                cylinder(h=pipe_b, r=hex_r, $fn=6);
            }
        }
    }
}

module bangle_hex0(pipe_r=35, pipe_b=2, hex_r=4, hex_n=20, hex_m=5) {
    difference() {
        pipe_pattern_hex(pipe_r, pipe_b, hex_n, hex_m, hex_r);
        traz(sqrt(3)*hex_r) pipe_pattern_hex(
            pipe_r=pipe_r - 0.5, pipe_b=pipe_b + 1,
            hex_n=hex_n, hex_m=1, hex_r=hex_r
        );
    }
}

module bangle_hex1(pipe_r=35, pipe_b=2, hex_r=4, hex_b=1, hex_n=22, hex_m=5) {
    difference() {
        pipe_pattern_hex(pipe_r, pipe_b, hex_n, hex_m, hex_r, hex_zoffset=-hex_b/2);
        pipe_pattern_hex(
            pipe_r=pipe_r - 0.5, pipe_b=pipe_b + 1,
            hex_n=hex_n, hex_m=hex_m, hex_r=hex_r - hex_b, hex_zoffset=hex_b/2
        );
    }
}

module bangle_hex2(
    pipe_r=35, pipe_b=2,
    hex_r=4, hex_b=1, hex_n=22, hex_m=3,
    stripe_l=4, stripe_n=70,
    $fn=128,
) {
    traz(hex_m*sqrt(3)*hex_r/2 - hex_b/2 + stripe_l/2 + 0.5)
        bangle_stripe0(pipe_r, pipe_b, stripe_l, stripe_n);

    bangle_hex1(pipe_r, pipe_b, hex_r, hex_b, hex_n, hex_m);

    traz(-sqrt(3)*hex_r/2 - hex_b/2 - stripe_l/2 - 0.5)
        bangle_stripe0(pipe_r, pipe_b, stripe_l, stripe_n);
}

module bangle_hex3(
    pipe_r=35, pipe_b=2,
    hex_r=4, hex_b=1, hex_n=22, hex_m=3,
    $fn=128
) {
    traz(hex_m*sqrt(3)*hex_r/2 - hex_b/2)
        pipe(hex_b, pipe_r, pipe_b);

    bangle_hex1(pipe_r, pipe_b, hex_r, hex_b, hex_n, hex_m);

    traz(-sqrt(3)*hex_r/2 - hex_b/2)
        pipe(hex_b, pipe_r, pipe_b);
}

translate([ 0,  0]) bangle_hex0();
translate([ 0, 80]) bangle_hex1();
translate([80,  0]) bangle_hex2();
translate([80, 80]) bangle_hex3();
