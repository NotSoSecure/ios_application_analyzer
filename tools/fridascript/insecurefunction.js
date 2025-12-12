(function() {
    var funcs = ["malloc", "snprintf", "printf", "memcpy", "strncpy", "sscanf", "fopen", "strlen"];
    var prefixes = ["", "_"];
    var target = "Zinc Alpha";
    var mods = Process.enumerateModulesSync();
    var mod = null;
    for (var i = 0; i < mods.length; i++) {
        if (mods[i].name.indexOf(target) !== -1) {
            mod = mods[i];
            break;
        }
    }
    if (!mod) {
        console.log("Module not found: " + target);
        return;
    }
    console.log("Using module: " + mod.name + " (" + mod.base + ")");
    funcs.forEach(function(func) {
        var hits = [];
        prefixes.forEach(function(p) {
            try {
                var addr = Module.findExportByName(mod.name, p + func);
                if (addr) hits.push(mod.name + " -> " + p + func + " @ " + addr);
            } catch (e) {}
        });
        if (hits.length) {
            console.log(func + " FOUND:");
            hits.forEach(function(h) {
                console.log("  " + h);
            });
        } else {
            console.log(func + " not found in " + mod.name);
        }
    });
})()