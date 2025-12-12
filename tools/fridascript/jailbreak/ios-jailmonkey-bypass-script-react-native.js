/*
 * @incogbyte
 * iOS Jailmonkey Bypass Script React Native
 * 
 * @author incogbyte
 * @version 1.0.0
 * @license MIT
 * @copyright 2025 incogbyte
 *  based on https://github.com/GantMan/jail-monkey/blob/master/JailMonkey/JailMonkey.m
 */

if (!ObjC.available) {
    console.warn('[!] Objective‑C runtime cannot be loaded.');
} else {
    ObjC.schedule(ObjC.mainQueue, function() {

        /* ---------- Patch 1 : Catalyst  ---------- */
        try {
            const procInfo = ObjC.classes.NSProcessInfo;
            if (!procInfo) {
                console.log('[i] NSProcessInfo not found – image not loaded?');
            } else {
                const sel = '- isiOSAppOnMac';
                const meth = procInfo[sel];

                if (!meth) {
                    console.log('[i] Selector isiOSAppOnMac does not exist in this version.');
                } else {
                    const alwaysNo = new NativeCallback(function(_self, _cmd) {
                        return 1; // YES (makes the app think it's on macOS) 👀
                    }, 'bool', ['pointer', 'pointer']);

                    Interceptor.replace(meth.implementation, alwaysNo);
                    console.log('[+] Patch applied: isiOSAppOnMac → YES');
                }
            }
        } catch (e) {
            console.log('[!] Failed to apply Catalyst patch:', e);
        }

        /* ---------- Patch 2 : JailMonkey ---------- */
        try {
            const className = 'JailMonkey';
            const selector = '- isJailBroken';

            const clazz = ObjC.classes[className];
            if (!clazz) {
                console.log(`[i] Class ${className} not found – JailMonkey missing.`);
            } else {
                const method = clazz[selector];
                if (!method) {
                    console.log(`[i] Method ${selector} does not exist in this version.`);
                } else {
                    Interceptor.attach(method.implementation, {
                        onLeave(retval) {
                            console.log(`[+] Intercepted ${className} ${selector} – forcing FALSE`);
                            retval.replace(ptr('0x0')); // returns NO / false
                        }
                    });
                    console.log('[+] Patch applied: JailMonkey isJailBroken → false');
                }
            }
        } catch (e) {
            console.log('[!] Failed to apply JailMonkey patch:', e);
        }

        console.warn('[+] All patches active ✅');
    });
}

(function(){
var funcs = ["malloc","snprintf","printf","memcpy","strncpy","sscanf","fopen","strlen"];
var prefixes = ["","_"];
var target = "Zinc Alpha";
var mods = Process.enumerateModulesSync();
var mod = null;
for (var i = 0; i < mods.length; i++) {
if (mods[i].name.indexOf(target) !== -1) { mod = mods[i]; break; }
}
if (!mod) { console.log("Module not found: " + target); return; }
console.log("Using module: " + mod.name + " (" + mod.base + ")");
funcs.forEach(function(func){
var hits = [];
prefixes.forEach(function(p){
try {
var addr = Module.findExportByName(mod.name, p + func);
if (addr) hits.push(mod.name + " -> " + p + func + " @ " + addr);
} catch (e) {}
});
if (hits.length) {
console.log(func + " FOUND:");
hits.forEach(function(h){ console.log("  " + h); });
} else {
console.log(func + " not found in " + mod.name);
}
});
})()