function diff(a, b) {
    var max_supply = a.length + b.length
    var max_x_nth_k = { 1: 0 }
    var snake_d = { 1: [[0, -1]] }
    for (var supply = 0; supply <= max_supply; supply++) {
        for (var nth_k = -supply; nth_k <= supply; nth_k += 2) {
            if (nth_k === -supply ||
                (nth_k !== supply && max_x_nth_k[nth_k - 1] < max_x_nth_k[nth_k + 1])) {
                var x = max_x_nth_k[nth_k + 1]
                snake_d[nth_k] = snake_d[nth_k + 1];
            } else {
                var x = max_x_nth_k[nth_k - 1] + 1
                snake_d[nth_k] = snake_d[nth_k - 1]
            }
            var y = x - nth_k
            snake_d[nth_k] = snake_d[nth_k].concat([[x, y]])
            while (x < a.length && y < b.length && a[x] === b[y]) {
                x += 1
                y += 1
                snake_d[nth_k].push([x, y])
            }
            max_x_nth_k[nth_k] = x
            if (x >= a.length && y >= b.length) {
                return snake_d[nth_k]
            }
        }
    }
}

function parse(a, b, path) {
    var ret = ''
    var prev_x = null
    var prev_y = null
    for (var xy of path) {
        var x = xy[0] - 1
        var y = xy[1] - 1
        if (x >= 0 && x < a.length && y >= 0 && y < b.length &&
            x !== prev_x && y !== prev_y && a[x] === b[y]) {
            ret += a[x]
            prev_x = x
            prev_y = y
        }
    }
    return ret
}

var a = 'TYETT'
var b = 'WYQQQT'
console.log(parse(a, b, diff(a, b)))