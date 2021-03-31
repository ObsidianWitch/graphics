module hull_pairs() {
    if ($children <= 1) {
        children();
    }
    else {
        for (i = [0 : $children - 2]) {
            hull() {
                children(i);
                children(i + 1);
            }
        }
    }
}
