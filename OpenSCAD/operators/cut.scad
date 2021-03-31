module cut(cuts = [0, 0, 0], limit = 1e3) {
    intersection() {
        children();
        translate(cuts * limit/2) {
            cube([limit, limit, limit], center = true);
        }
    }
}
module cutx(x = 1, limit = 1e3) { cut([x, 0, 0], limit) children(); }
module cuty(y = 1, limit = 1e3) { cut([0, y, 0], limit) children(); }
module cutz(z = 1, limit = 1e3) { cut([0, 0, z], limit) children(); }

module cutRot(cuts = [0, 0, 0], angle = [0, 0, 0], limit = 1e3) {
    rotate(-angle) cut(cuts, limit) rotate(angle) children();
}
