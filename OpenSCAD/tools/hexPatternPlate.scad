module hexPatternPlate() {
    module hexagon() {
        translate([5, 5, 0]) {
            cylinder(d = 10, h = 10, center = true, $fn = 6);
        }
    }
    
    module hexagonPattern(cubeSize) {
        for (i = [10 : 10 : cubeSize.x - 20]) {
            jStart = i % 20 ? 10 : 20;
            
            for (j = [jStart : 20 : cubeSize.y - 20]) {
                translate([j, i, 0]) hexagon();
            }
        }
    }
    
    difference() {
        cubeSize = [150, 150, 2];
        
        cube(cubeSize);
        hexagonPattern(cubeSize);
    }
}

hexPatternPlate();
