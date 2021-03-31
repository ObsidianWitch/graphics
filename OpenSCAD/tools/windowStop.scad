module windowStop() {
    module slope() {
        translate([0, 0, 3]) hull() {
            cube([3, 18, 19]);
            cube([30, 18, 2]);
        }
    }
    
    module base() {
        difference() {
            hull() {
                cube([30, 18, 5]);
                translate([40, 9, 0]) cylinder(d = 18, h = 5);
            }
            
            translate([0, 0, 0]) hull() {
                translate([7, 1, 0]) cube([1, 16, 3]);
                translate([40, 9, 0]) cylinder(d = 16, h = 3);
            }
        }
    }
    
    module details() {
        difference() {
            translate([0, 7, -1.5]) cube([9, 4, 1.5]);
            translate([6, 9, -1.5]) cylinder(d = 2, h = 2, $fn = 16);
        }
        
        translate([7, 7, 0]) cube([21, 4, 3]);
        translate([30.5, 9, 0]) cylinder(d = 3, h = 3, $fn = 16);
    }
    
    union() {
        slope();
        base();
        details();
    }
}

windowStop();
