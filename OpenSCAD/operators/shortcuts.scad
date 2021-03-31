// Translate
module tra(v) { translate(v) children(); }
module trax(x) { translate([x, 0, 0]) children(); }
module tray(y) { translate([0, y, 0]) children(); }
module traz(z) { translate([0, 0, z]) children(); }

// Scale
module sca(v) { scale(v) children(); }
module scax(x) { scale([x, 1, 1]) children(); }
module scay(y) { scale([1, y, 1]) children(); }
module scaz(z) { scale([1, 1, z]) children(); }

// Rotate
module rot(a, v) { rotate(a, v) children(); }
module rotx(x) { rotate([x, 0, 0]) children(); }
module roty(y) { rotate([0, y, 0]) children(); }
module rotz(z) { rotate([0, 0, z]) children(); }

// Symmetry
module sym(v) { mirror(v) children(); }
module symx() { mirror([1, 0, 0]) children(); }
module symy() { mirror([0, 1, 0]) children(); }
module symz() { mirror([0, 0, 1]) children(); }

// Mirror
module mir(v) { children(); mirror(v) children(); }
module mirx() { children(); mirror([1, 0, 0]) children(); }
module miry() { children(); mirror([0, 1, 0]) children(); }
module mirz() { children(); mirror([0, 0, 1]) children(); }
